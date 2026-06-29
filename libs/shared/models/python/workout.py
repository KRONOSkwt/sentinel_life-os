"""Shared Python models for workout routines and exercises."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ExerciseBase(BaseModel):
    """Base exercise model."""

    name: str = Field(..., min_length=1, max_length=150)
    category: str = Field(..., pattern=r"^(strength|cardio|flexibility)$")
    muscle_groups: list[str] = Field(..., min_length=1)
    equipment: Optional[str] = Field(None, max_length=100)


class ExerciseCreate(ExerciseBase):
    """Request body for creating a custom exercise."""

    pass


class ExerciseResponse(ExerciseBase):
    """Public exercise representation."""

    id: int
    is_custom: bool
    created_at: datetime

    class Config:
        from_attributes = True


class RoutineExerciseBase(BaseModel):
    """Exercise entry within a routine."""

    exercise_id: int
    target_sets: int = Field(..., ge=1)
    target_reps: int = Field(..., ge=1)
    order: int = Field(..., ge=0)


class RoutineExerciseCreate(RoutineExerciseBase):
    """Request body for adding exercise to routine."""

    pass


class RoutineExerciseResponse(RoutineExerciseBase):
    """Exercise entry within a routine (response)."""

    id: int
    exercise: ExerciseResponse

    class Config:
        from_attributes = True


class RoutineBase(BaseModel):
    """Base routine model."""

    name: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = None


class RoutineCreate(RoutineBase):
    """Request body for creating a routine."""

    exercises: list[RoutineExerciseCreate] = Field(default_factory=list)


class RoutineUpdate(BaseModel):
    """Request body for updating a routine (all optional)."""

    name: Optional[str] = Field(None, min_length=1, max_length=150)
    description: Optional[str] = None
    exercises: Optional[list[RoutineExerciseCreate]] = None


class RoutineResponse(RoutineBase):
    """Public routine representation (list view — no exercises)."""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RoutineDetailResponse(RoutineResponse):
    """Routine detail — includes exercises."""

    exercises: list[RoutineExerciseResponse] = []
