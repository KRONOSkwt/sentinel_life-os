"""Shared Python models for workout sessions and sets."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SetBase(BaseModel):
    """Base set model."""

    exercise_id: int
    set_number: int = Field(..., ge=1)
    weight: float = Field(..., ge=0)
    reps: int = Field(..., ge=1)
    rpe: Optional[float] = Field(None, ge=1, le=10)


class SetCreate(SetBase):
    """Request body for logging a set within a session."""

    pass


class SetResponse(SetBase):
    """Public set representation."""

    id: int
    session_id: int
    is_pr: bool
    created_at: datetime

    class Config:
        from_attributes = True


class SessionBase(BaseModel):
    """Base session model."""

    routine_id: Optional[int] = None


class SessionCreate(SessionBase):
    """Request body for starting a workout session."""

    pass


class SessionComplete(BaseModel):
    """Request body for completing a session."""

    notes: Optional[str] = None


class SessionResponse(BaseModel):
    """Public session representation."""

    id: int
    user_id: int
    routine_id: Optional[int]
    started_at: datetime
    completed_at: Optional[datetime]
    duration_seconds: Optional[int]
    notes: Optional[str]
    sets: list[SetResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True


class WeightChartEntry(BaseModel):
    """Single data point for weight progression chart."""

    date: datetime
    weight: float
    reps: int
    set_number: int


class WeightChartResponse(BaseModel):
    """Weight progression data for a specific exercise."""

    exercise_id: int
    exercise_name: str
    data: list[WeightChartEntry]
