"""Routine service — CRUD for routines and routine exercises.

Routine name uniqueness is enforced per user (case-insensitive).
Exercise catalog supports search/filter by category, muscle group, and name.
"""

import json
from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from src.models.db import Exercise, Routine, RoutineExercise
from src.models.schemas import (
    ExerciseCreate,
    ExerciseResponse,
    RoutineCreate,
    RoutineDetailResponse,
    RoutineExerciseCreate,
    RoutineExerciseResponse,
    RoutineResponse,
    RoutineUpdate,
)


# ---------------------------------------------------------------------------
# Exercise catalog
# ---------------------------------------------------------------------------


def search_exercises(
    db: Session,
    *,
    query: Optional[str] = None,
    category: Optional[str] = None,
    muscle_group: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
) -> list[ExerciseResponse]:
    """Search exercises with optional filters. Returns Pydantic response models."""
    stmt = db.query(Exercise)

    if query:
        stmt = stmt.filter(Exercise.name.ilike(f"%{query}%"))
    if category:
        stmt = stmt.filter(Exercise.category == category)
    if muscle_group:
        # muscle_groups is stored as JSON array string — use LIKE for broad match
        stmt = stmt.filter(Exercise.muscle_groups.ilike(f"%{muscle_group}%"))

    exercises = stmt.order_by(Exercise.name).offset(offset).limit(limit).all()

    return [
        ExerciseResponse(
            id=e.id,
            name=e.name,
            category=e.category,
            muscle_groups=json.loads(e.muscle_groups),
            equipment=e.equipment,
            is_custom=e.is_custom,
            created_at=e.created_at,
        )
        for e in exercises
    ]


def create_exercise(db: Session, user_id: int, data: ExerciseCreate) -> ExerciseResponse:
    """Create a custom exercise for a user."""
    exercise = Exercise(
        name=data.name,
        category=data.category,
        muscle_groups=json.dumps(data.muscle_groups),
        equipment=data.equipment,
        is_custom=True,
        user_id=user_id,
    )
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return ExerciseResponse(
        id=exercise.id,
        name=exercise.name,
        category=exercise.category,
        muscle_groups=data.muscle_groups,
        equipment=exercise.equipment,
        is_custom=True,
        created_at=exercise.created_at,
    )


# ---------------------------------------------------------------------------
# Routine CRUD
# ---------------------------------------------------------------------------


def list_routines(db: Session, user_id: int) -> list[RoutineResponse]:
    """List all routines for a user."""
    routines = (
        db.query(Routine)
        .filter(Routine.user_id == user_id)
        .order_by(Routine.updated_at.desc())
        .all()
    )
    return [
        RoutineResponse(
            id=r.id,
            name=r.name,
            description=r.description,
            created_at=r.created_at,
            updated_at=r.updated_at,
        )
        for r in routines
    ]


def get_routine(db: Session, routine_id: int, user_id: int) -> Optional[RoutineDetailResponse]:
    """Get a routine with its exercises. Returns None if not found or not owned by user."""
    routine = (
        db.query(Routine)
        .options(joinedload(Routine.routine_exercises).joinedload(RoutineExercise.exercise))
        .filter(Routine.id == routine_id, Routine.user_id == user_id)
        .first()
    )
    if not routine:
        return None

    exercises = sorted(routine.routine_exercises, key=lambda re: re.order)
    return RoutineDetailResponse(
        id=routine.id,
        name=routine.name,
        description=routine.description,
        created_at=routine.created_at,
        updated_at=routine.updated_at,
        exercises=[
            RoutineExerciseResponse(
                id=re.id,
                exercise_id=re.exercise_id,
                exercise=ExerciseResponse(
                    id=re.exercise.id,
                    name=re.exercise.name,
                    category=re.exercise.category,
                    muscle_groups=json.loads(re.exercise.muscle_groups),
                    equipment=re.exercise.equipment,
                    is_custom=re.exercise.is_custom,
                    created_at=re.exercise.created_at,
                ),
                target_sets=re.target_sets,
                target_reps=re.target_reps,
                order=re.order,
            )
            for re in exercises
        ],
    )


def _check_routine_name_unique(db: Session, user_id: int, name: str, exclude_id: Optional[int] = None) -> bool:
    """Check if routine name is unique for this user (case-insensitive)."""
    stmt = (
        db.query(Routine)
        .filter(Routine.user_id == user_id, func.lower(Routine.name) == name.lower())
    )
    if exclude_id:
        stmt = stmt.filter(Routine.id != exclude_id)
    return stmt.first() is None


def create_routine(db: Session, user_id: int, data: RoutineCreate) -> RoutineDetailResponse:
    """Create a routine with optional exercises."""
    if not _check_routine_name_unique(db, user_id, data.name):
        raise ValueError(f"Routine with name '{data.name}' already exists")

    routine = Routine(user_id=user_id, name=data.name, description=data.description)
    db.add(routine)
    db.flush()  # get routine.id

    for ex_data in data.exercises:
        re = RoutineExercise(
            routine_id=routine.id,
            exercise_id=ex_data.exercise_id,
            target_sets=ex_data.target_sets,
            target_reps=ex_data.target_reps,
            order=ex_data.order,
        )
        db.add(re)

    db.commit()
    result = get_routine(db, routine.id, user_id)
    assert result is not None
    return result


def update_routine(
    db: Session, routine_id: int, user_id: int, data: RoutineUpdate
) -> Optional[RoutineDetailResponse]:
    """Update a routine. If exercises are provided, replace them entirely."""
    routine = (
        db.query(Routine)
        .filter(Routine.id == routine_id, Routine.user_id == user_id)
        .first()
    )
    if not routine:
        return None

    if data.name is not None:
        if not _check_routine_name_unique(db, user_id, data.name, exclude_id=routine_id):
            raise ValueError(f"Routine with name '{data.name}' already exists")
        routine.name = data.name

    if data.description is not None:
        routine.description = data.description

    if data.exercises is not None:
        # Replace all routine exercises
        db.query(RoutineExercise).filter(RoutineExercise.routine_id == routine_id).delete()
        for ex_data in data.exercises:
            re = RoutineExercise(
                routine_id=routine_id,
                exercise_id=ex_data.exercise_id,
                target_sets=ex_data.target_sets,
                target_reps=ex_data.target_reps,
                order=ex_data.order,
            )
            db.add(re)

    db.commit()
    result = get_routine(db, routine_id, user_id)
    assert result is not None
    return result


def delete_routine(db: Session, routine_id: int, user_id: int) -> bool:
    """Delete a routine and its exercises. Returns True if deleted."""
    routine = (
        db.query(Routine)
        .filter(Routine.id == routine_id, Routine.user_id == user_id)
        .first()
    )
    if not routine:
        return False
    db.delete(routine)
    db.commit()
    return True
