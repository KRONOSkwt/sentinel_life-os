"""Shared Python models for AI coach suggestions."""

from pydantic import BaseModel, Field


class AISuggestionBase(BaseModel):
    """Base AI suggestion model."""

    exercise_id: int
    exercise_name: str
    current_weight: float
    suggested_weight: float
    reason: str
    confidence: float = Field(..., ge=0, le=1)


class AISuggestionResponse(AISuggestionBase):
    """AI coach suggestion for progressive overload."""

    pass
