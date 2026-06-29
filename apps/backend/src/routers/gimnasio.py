"""Gimnasio module routes — routines, workouts, AI coach, gamification, calendar.

All endpoints require authentication via JWT Bearer token.
"""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.deps import get_current_user
from src.models.db import User
from src.models.schemas import (
    ExerciseCreate,
    ExerciseResponse,
    RoutineCreate,
    RoutineDetailResponse,
    RoutineResponse,
    RoutineUpdate,
    SessionComplete,
    SessionCreate,
    SessionResponse,
    SetCreate,
    SetResponse,
)
from src.services import (
    ai_coach,
    calendar_service,
    gamification_service,
    routine_service,
    workout_service,
)

router = APIRouter(prefix="/gimnasio", tags=["gimnasio"])


# ---------------------------------------------------------------------------
# Exercise catalog
# ---------------------------------------------------------------------------


@router.get("/exercises", response_model=list[ExerciseResponse])
def list_exercises(
    query: Optional[str] = Query(None, description="Search by name"),
    category: Optional[str] = Query(None, description="Filter: strength|cardio|flexibility"),
    muscle_group: Optional[str] = Query(None, description="Filter by muscle group"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Search and filter the exercise catalog."""
    return routine_service.search_exercises(
        db, query=query, category=category, muscle_group=muscle_group,
        limit=limit, offset=offset,
    )


@router.post("/exercises", response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
def create_exercise(
    body: ExerciseCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a custom exercise for the current user."""
    return routine_service.create_exercise(db, current_user.id, body)


# ---------------------------------------------------------------------------
# Routine CRUD
# ---------------------------------------------------------------------------


@router.get("/routines", response_model=list[RoutineResponse])
def list_routines(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all routines for the current user."""
    return routine_service.list_routines(db, current_user.id)


@router.get("/routines/{routine_id}", response_model=RoutineDetailResponse)
def get_routine(
    routine_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a routine with its exercises."""
    routine = routine_service.get_routine(db, routine_id, current_user.id)
    if not routine:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Routine not found",
        )
    return routine


@router.post("/routines", response_model=RoutineDetailResponse, status_code=status.HTTP_201_CREATED)
def create_routine(
    body: RoutineCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new routine with optional exercises."""
    try:
        return routine_service.create_routine(db, current_user.id, body)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )


@router.put("/routines/{routine_id}", response_model=RoutineDetailResponse)
def update_routine(
    routine_id: int,
    body: RoutineUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a routine. If exercises are provided, they replace all existing ones."""
    result = routine_service.update_routine(db, routine_id, current_user.id, body)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Routine not found",
        )
    return result


@router.delete("/routines/{routine_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_routine(
    routine_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a routine and its exercises."""
    deleted = routine_service.delete_routine(db, routine_id, current_user.id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Routine not found",
        )


# ---------------------------------------------------------------------------
# Workout sessions
# ---------------------------------------------------------------------------


@router.post("/sessions", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def start_session(
    body: SessionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Start a new workout session."""
    return workout_service.start_session(db, current_user.id, body)


@router.get("/sessions", response_model=list[SessionResponse])
def list_sessions(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    completed_only: bool = Query(True),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List workout sessions for the current user."""
    return workout_service.list_sessions(
        db, current_user.id, limit=limit, offset=offset,
        completed_only=completed_only,
    )


@router.get("/sessions/{session_id}", response_model=SessionResponse)
def get_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a session with its sets."""
    session = workout_service.get_session(db, session_id, current_user.id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )
    return session


@router.post("/sessions/{session_id}/complete", response_model=SessionResponse)
def complete_session(
    session_id: int,
    body: SessionComplete,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Complete a workout session. Triggers gamification updates."""
    try:
        result = workout_service.complete_session(db, session_id, current_user.id, body)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found",
        )

    # Process gamification after successful completion
    gamification_service.on_session_complete(db, current_user.id)

    return result


# ---------------------------------------------------------------------------
# Workout sets
# ---------------------------------------------------------------------------


@router.post("/sessions/{session_id}/sets", response_model=SetResponse, status_code=status.HTTP_201_CREATED)
def log_set(
    session_id: int,
    body: SetCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Log a set within a session. PRs are detected automatically."""
    try:
        return workout_service.log_set(db, session_id, current_user.id, body)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# ---------------------------------------------------------------------------
# Weight chart
# ---------------------------------------------------------------------------


@router.get("/weight-chart/{exercise_id}")
def get_weight_chart(
    exercise_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get weight progression data for a specific exercise."""
    return workout_service.get_weight_chart(db, current_user.id, exercise_id)


# ---------------------------------------------------------------------------
# AI Coach
# ---------------------------------------------------------------------------


@router.get("/ai-suggestions")
def get_ai_suggestions(
    use_ai: bool = Query(True, description="Try Hugging Face API first"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get progressive overload suggestions for recently trained exercises."""
    return ai_coach.get_all_suggestions(db, current_user.id, use_ai=use_ai)


@router.get("/ai-suggestions/{exercise_id}")
def get_ai_suggestion_for_exercise(
    exercise_id: int,
    use_ai: bool = Query(True),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a progressive overload suggestion for a specific exercise."""
    suggestion = ai_coach.get_suggestion(db, current_user.id, exercise_id, use_ai=use_ai)
    if not suggestion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No workout history found for this exercise",
        )
    return suggestion


# ---------------------------------------------------------------------------
# Gamification
# ---------------------------------------------------------------------------


@router.get("/gamification/stats")
def get_gamification_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get gamification stats (points, streak, level)."""
    return gamification_service.get_stats(db, current_user.id)


@router.get("/gamification/achievements")
def get_achievements(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get all unlocked achievements for the current user."""
    return gamification_service.get_achievements(db, current_user.id)


# ---------------------------------------------------------------------------
# Calendar heatmap
# ---------------------------------------------------------------------------


@router.get("/heatmap")
def get_heatmap(
    year: Optional[int] = Query(None, description="Year (default: current)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get year heatmap data for the current user."""
    return calendar_service.get_heatmap(db, current_user.id, year=year)
