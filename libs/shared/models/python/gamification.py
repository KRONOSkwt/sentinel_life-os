"""Shared Python models for gamification stats and achievements."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class GamificationStatsBase(BaseModel):
    """Base gamification stats model."""

    total_points: int = 0
    current_streak: int = 0
    longest_streak: int = 0
    level: int = 1


class GamificationStatsResponse(GamificationStatsBase):
    """User gamification stats."""

    last_workout_date: Optional[datetime] = None


class AchievementBase(BaseModel):
    """Base achievement model."""

    achievement_key: str


class AchievementResponse(AchievementBase):
    """Unlocked achievement."""

    id: int
    unlocked_at: datetime

    class Config:
        from_attributes = True
