"""Workout service — session lifecycle, set logging, PR detection, weight tracking.

Session lifecycle: start → log sets → complete.
PR detection: weight-first, then reps at same weight.
Duration auto-calculated from started_at/completed_at.
"""

from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from src.models.db import WorkoutSession, WorkoutSet
from src.models.schemas import (
    SetCreate,
    SetResponse,
    SessionComplete,
    SessionCreate,
    SessionResponse,
    WeightChartEntry,
    WeightChartResponse,
)


def start_session(db: Session, user_id: int, data: SessionCreate) -> SessionResponse:
    """Start a new workout session."""
    session = WorkoutSession(
        user_id=user_id,
        routine_id=data.routine_id,
        started_at=datetime.now(timezone.utc),
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return SessionResponse(
        id=session.id,
        user_id=session.user_id,
        routine_id=session.routine_id,
        started_at=session.started_at,
        completed_at=session.completed_at,
        duration_seconds=session.duration_seconds,
        notes=session.notes,
        sets=[],
        created_at=session.created_at,
    )


def log_set(db: Session, session_id: int, user_id: int, data: SetCreate) -> SetResponse:
    """Log a set within a session. Detects PRs automatically."""
    # Verify session exists and belongs to user
    session = (
        db.query(WorkoutSession)
        .filter(WorkoutSession.id == session_id, WorkoutSession.user_id == user_id)
        .first()
    )
    if not session:
        raise ValueError("Session not found")
    if session.completed_at is not None:
        raise ValueError("Session is already completed")

    is_pr = _detect_pr(db, user_id, data.exercise_id, data.weight, data.reps)

    workout_set = WorkoutSet(
        session_id=session_id,
        exercise_id=data.exercise_id,
        set_number=data.set_number,
        weight=data.weight,
        reps=data.reps,
        rpe=data.rpe,
        is_pr=is_pr,
    )
    db.add(workout_set)
    db.commit()
    db.refresh(workout_set)

    return SetResponse(
        id=workout_set.id,
        session_id=workout_set.session_id,
        exercise_id=workout_set.exercise_id,
        set_number=workout_set.set_number,
        weight=workout_set.weight,
        reps=workout_set.reps,
        rpe=workout_set.rpe,
        is_pr=workout_set.is_pr,
        created_at=workout_set.created_at,
    )


def complete_session(
    db: Session, session_id: int, user_id: int, data: SessionComplete
) -> Optional[SessionResponse]:
    """Complete a workout session. Auto-calculates duration."""
    session = (
        db.query(WorkoutSession)
        .filter(WorkoutSession.id == session_id, WorkoutSession.user_id == user_id)
        .first()
    )
    if not session:
        return None
    if session.completed_at is not None:
        raise ValueError("Session is already completed")

    now = datetime.now(timezone.utc)
    session.completed_at = now
    session.duration_seconds = int((now - session.started_at).total_seconds())
    session.notes = data.notes

    db.commit()
    return get_session(db, session_id, user_id)


def get_session(db: Session, session_id: int, user_id: int) -> Optional[SessionResponse]:
    """Get a session with its sets."""
    session = (
        db.query(WorkoutSession)
        .options(joinedload(WorkoutSession.workout_sets))
        .filter(WorkoutSession.id == session_id, WorkoutSession.user_id == user_id)
        .first()
    )
    if not session:
        return None

    sets = sorted(session.workout_sets, key=lambda s: (s.exercise_id, s.set_number))
    return SessionResponse(
        id=session.id,
        user_id=session.user_id,
        routine_id=session.routine_id,
        started_at=session.started_at,
        completed_at=session.completed_at,
        duration_seconds=session.duration_seconds,
        notes=session.notes,
        sets=[
            SetResponse(
                id=s.id,
                session_id=s.session_id,
                exercise_id=s.exercise_id,
                set_number=s.set_number,
                weight=s.weight,
                reps=s.reps,
                rpe=s.rpe,
                is_pr=s.is_pr,
                created_at=s.created_at,
            )
            for s in sets
        ],
        created_at=session.created_at,
    )


def list_sessions(
    db: Session,
    user_id: int,
    *,
    limit: int = 20,
    offset: int = 0,
    completed_only: bool = True,
) -> list[SessionResponse]:
    """List workout sessions for a user."""
    stmt = db.query(WorkoutSession).filter(WorkoutSession.user_id == user_id)
    if completed_only:
        stmt = stmt.filter(WorkoutSession.completed_at.isnot(None))

    sessions = stmt.order_by(WorkoutSession.started_at.desc()).offset(offset).limit(limit).all()

    return [
        SessionResponse(
            id=s.id,
            user_id=s.user_id,
            routine_id=s.routine_id,
            started_at=s.started_at,
            completed_at=s.completed_at,
            duration_seconds=s.duration_seconds,
            notes=s.notes,
            sets=[],
            created_at=s.created_at,
        )
        for s in sessions
    ]


def get_weight_chart(
    db: Session, user_id: int, exercise_id: int
) -> WeightChartResponse:
    """Get weight progression data for a specific exercise."""
    # Get exercise name
    from src.models.db import Exercise

    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    exercise_name = exercise.name if exercise else f"Exercise #{exercise_id}"

    # Get all sets for this exercise across all user sessions
    rows = (
        db.query(WorkoutSet, WorkoutSession.started_at)
        .join(WorkoutSession, WorkoutSet.session_id == WorkoutSession.id)
        .filter(
            WorkoutSession.user_id == user_id,
            WorkoutSet.exercise_id == exercise_id,
            WorkoutSession.completed_at.isnot(None),
        )
        .order_by(WorkoutSession.started_at)
        .all()
    )

    data = [
        WeightChartEntry(
            date=started_at,
            weight=ws.weight,
            reps=ws.reps,
            set_number=ws.set_number,
        )
        for ws, started_at in rows
    ]

    return WeightChartResponse(
        exercise_id=exercise_id,
        exercise_name=exercise_name,
        data=data,
    )


# ---------------------------------------------------------------------------
# PR detection
# ---------------------------------------------------------------------------


def _detect_pr(
    db: Session, user_id: int, exercise_id: int, weight: float, reps: int
) -> bool:
    """Detect if a set is a personal record.

    Logic (in priority order):
    1. Higher weight than any previous set for this exercise → PR
    2. Same weight but more reps than any previous set at that weight → PR
    3. Otherwise → not PR
    """
    # Get the best previous performance for this exercise
    best = (
        db.query(
            func.max(WorkoutSet.weight).label("max_weight"),
        )
        .join(WorkoutSession, WorkoutSet.session_id == WorkoutSession.id)
        .filter(
            WorkoutSession.user_id == user_id,
            WorkoutSet.exercise_id == exercise_id,
            WorkoutSession.completed_at.isnot(None),
        )
        .first()
    )

    if best is None or best.max_weight is None:
        # First ever set for this exercise → PR
        return True

    if weight > best.max_weight:
        return True

    if weight == best.max_weight:
        # Check reps at this weight
        max_reps_at_weight = (
            db.query(func.max(WorkoutSet.reps))
            .join(WorkoutSession, WorkoutSet.session_id == WorkoutSession.id)
            .filter(
                WorkoutSession.user_id == user_id,
                WorkoutSet.exercise_id == exercise_id,
                WorkoutSet.weight == weight,
                WorkoutSession.completed_at.isnot(None),
            )
            .scalar()
        )
        if max_reps_at_weight is None or reps > max_reps_at_weight:
            return True

    return False
