"""Pydantic request/response schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------


class UserCreate(BaseModel):
    """Request body for user registration."""

    email: EmailStr
    password: str = Field(..., min_length=8)
    display_name: str = Field(..., min_length=1, max_length=50)


class UserLogin(BaseModel):
    """Request body for user login."""

    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Public user representation."""

    id: int
    email: str
    display_name: str
    created_at: datetime


class TokenResponse(BaseModel):
    """JWT token pair returned after login/register."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    """Request body for token refresh."""

    refresh_token: str


# ---------------------------------------------------------------------------
# Module
# ---------------------------------------------------------------------------


class ModuleCreate(BaseModel):
    """Request body for creating a module."""

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., max_length=500)


class ModuleUpdate(BaseModel):
    """Request body for updating a module (all optional)."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    enabled: Optional[bool] = None


class ModuleResponse(BaseModel):
    """Public module representation."""

    id: int
    name: str
    description: str
    enabled: bool
    created_at: datetime


# ---------------------------------------------------------------------------
# Activity
# ---------------------------------------------------------------------------


class ActivityCreate(BaseModel):
    """Request body for logging an activity."""

    module_id: int
    type: str = Field(..., min_length=1, max_length=50)
    value: float = Field(ge=0)
    extra_data: Optional[dict] = None


class ActivityResponse(BaseModel):
    """Public activity representation."""

    id: int
    module_id: int
    type: str
    value: float
    extra_data: Optional[dict]
    created_at: datetime


# ---------------------------------------------------------------------------
# Gimnasio — Exercise
# ---------------------------------------------------------------------------


class ExerciseCreate(BaseModel):
    """Request body for creating a custom exercise."""

    name: str = Field(..., min_length=1, max_length=150)
    category: str = Field(..., pattern=r"^(strength|cardio|flexibility)$")
    muscle_groups: list[str] = Field(..., min_length=1)
    equipment: Optional[str] = Field(None, max_length=100)


class ExerciseResponse(BaseModel):
    """Public exercise representation."""

    id: int
    name: str
    category: str
    muscle_groups: list[str]
    equipment: Optional[str]
    is_custom: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Gimnasio — Routine
# ---------------------------------------------------------------------------


class RoutineExerciseCreate(BaseModel):
    """Exercise entry within a routine."""

    exercise_id: int
    target_sets: int = Field(..., ge=1)
    target_reps: int = Field(..., ge=1)
    order: int = Field(..., ge=0)


class RoutineExerciseResponse(BaseModel):
    """Exercise entry within a routine (response)."""

    id: int
    exercise_id: int
    exercise: ExerciseResponse
    target_sets: int
    target_reps: int
    order: int

    class Config:
        from_attributes = True


class RoutineCreate(BaseModel):
    """Request body for creating a routine."""

    name: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = None
    exercises: list[RoutineExerciseCreate] = Field(default_factory=list)


class RoutineUpdate(BaseModel):
    """Request body for updating a routine (all optional)."""

    name: Optional[str] = Field(None, min_length=1, max_length=150)
    description: Optional[str] = None
    exercises: Optional[list[RoutineExerciseCreate]] = None


class RoutineResponse(BaseModel):
    """Public routine representation (list view — no exercises)."""

    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RoutineDetailResponse(RoutineResponse):
    """Routine detail — includes exercises."""

    exercises: list[RoutineExerciseResponse] = []


# ---------------------------------------------------------------------------
# Gimnasio — Workout Session
# ---------------------------------------------------------------------------


class SessionCreate(BaseModel):
    """Request body for starting a workout session."""

    routine_id: Optional[int] = None


class SetCreate(BaseModel):
    """Request body for logging a set within a session."""

    exercise_id: int
    set_number: int = Field(..., ge=1)
    weight: float = Field(..., ge=0)
    reps: int = Field(..., ge=1)
    rpe: Optional[float] = Field(None, ge=1, le=10)


class SetResponse(BaseModel):
    """Public set representation."""

    id: int
    session_id: int
    exercise_id: int
    set_number: int
    weight: float
    reps: int
    rpe: Optional[float]
    is_pr: bool
    created_at: datetime

    class Config:
        from_attributes = True


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


# ---------------------------------------------------------------------------
# Gimnasio — Weight Chart
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Gimnasio — AI Coach
# ---------------------------------------------------------------------------


class AISuggestionResponse(BaseModel):
    """AI coach suggestion for progressive overload."""

    exercise_id: int
    exercise_name: str
    current_weight: float
    suggested_weight: float
    reason: str
    confidence: float = Field(..., ge=0, le=1)


# ---------------------------------------------------------------------------
# Gimnasio — Gamification
# ---------------------------------------------------------------------------


class GamificationStatsResponse(BaseModel):
    """User gamification stats."""

    total_points: int
    current_streak: int
    longest_streak: int
    level: int
    last_workout_date: Optional[datetime]


class AchievementResponse(BaseModel):
    """Unlocked achievement."""

    id: int
    achievement_key: str
    unlocked_at: datetime

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Gimnasio — Heatmap
# ---------------------------------------------------------------------------


class HeatmapDay(BaseModel):
    """Single day in the heatmap grid."""

    date: str  # YYYY-MM-DD
    intensity: int  # 0 = no workout, 1–3 = increasing intensity
    workout_count: int


class HeatmapResponse(BaseModel):
    """Year heatmap data."""

    year: int
    days: list[HeatmapDay]


# ---------------------------------------------------------------------------
# Deportes — Sport
# ---------------------------------------------------------------------------


class SportCreate(BaseModel):
    """Request body for creating a custom sport."""

    name: str = Field(..., min_length=1, max_length=150)
    icon: Optional[str] = Field(None, max_length=50)


class SportResponse(BaseModel):
    """Public sport representation."""

    id: int
    name: str
    icon: Optional[str]
    is_custom: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Deportes — SportActivity
# ---------------------------------------------------------------------------


class SportActivityCreate(BaseModel):
    """Request body for logging a sport activity."""

    sport_id: int
    date: datetime
    duration_seconds: int = Field(..., gt=0)
    distance_km: Optional[float] = Field(None, ge=0)
    calories: Optional[int] = Field(None, ge=0)
    heart_rate_avg: Optional[int] = Field(None, ge=30, le=250)
    extra_data: Optional[dict] = None
    notes: Optional[str] = None


class SportActivityUpdate(BaseModel):
    """Request body for updating a sport activity (all optional)."""

    date: Optional[datetime] = None
    duration_seconds: Optional[int] = Field(None, gt=0)
    distance_km: Optional[float] = Field(None, ge=0)
    calories: Optional[int] = Field(None, ge=0)
    heart_rate_avg: Optional[int] = Field(None, ge=30, le=250)
    extra_data: Optional[dict] = None
    notes: Optional[str] = None


class SportActivityResponse(BaseModel):
    """Public sport activity representation."""

    id: int
    user_id: int
    sport_id: int
    date: datetime
    duration_seconds: int
    distance_km: Optional[float]
    calories: Optional[int]
    heart_rate_avg: Optional[int]
    extra_data: Optional[dict]
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Deportes — Stats & PRs
# ---------------------------------------------------------------------------


class SportStatsResponse(BaseModel):
    """Aggregated statistics for a sport."""

    sport_id: int
    sport_name: str
    total_activities: int
    total_time_seconds: int
    total_distance_km: Optional[float]
    average_duration_seconds: Optional[float]


class PersonalRecordResponse(BaseModel):
    """Personal record for a sport."""

    sport_id: int
    best_time_seconds: Optional[int]
    best_distance_km: Optional[float]
    best_pace_seconds_per_km: Optional[int]
    best_time_date: Optional[datetime]
    best_distance_date: Optional[datetime]


# ---------------------------------------------------------------------------
# Deportes — Training Plan
# ---------------------------------------------------------------------------


class TrainingPlanWeekUpdate(BaseModel):
    """Update for a single week in a plan."""

    week_number: int
    target_sessions: int = Field(..., ge=1)
    completed_sessions: int = Field(0, ge=0)
    notes: Optional[str] = None


class TrainingPlanCreate(BaseModel):
    """Request body for creating a training plan."""

    name: str = Field(..., min_length=1, max_length=150)
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    weeks: Optional[list[TrainingPlanWeekUpdate]] = None


class TrainingPlanUpdate(BaseModel):
    """Request body for updating a training plan (all optional)."""

    name: Optional[str] = Field(None, min_length=1, max_length=150)
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    weeks: Optional[list[TrainingPlanWeekUpdate]] = None


class TrainingPlanWeekResponse(BaseModel):
    """Single week in a training plan."""

    id: int
    week_number: int
    target_sessions: int
    completed_sessions: int
    notes: Optional[str]

    class Config:
        from_attributes = True


class TrainingPlanResponse(BaseModel):
    """Public training plan representation (list view — no weeks)."""

    id: int
    name: str
    description: Optional[str]
    start_date: datetime
    end_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TrainingPlanDetailResponse(TrainingPlanResponse):
    """Training plan detail — includes weeks."""

    weeks: list[TrainingPlanWeekResponse] = []


# ---------------------------------------------------------------------------
# Deportes — Race Event
# ---------------------------------------------------------------------------


class RaceEventCreate(BaseModel):
    """Request body for creating a race event."""

    name: str = Field(..., min_length=1, max_length=200)
    sport_id: int
    event_date: datetime
    distance_km: Optional[float] = Field(None, ge=0)
    location: Optional[str] = Field(None, max_length=300)
    target_time_seconds: Optional[int] = Field(None, ge=0)
    notes: Optional[str] = None


class RaceEventUpdate(BaseModel):
    """Request body for updating a race event (all optional)."""

    name: Optional[str] = Field(None, min_length=1, max_length=200)
    sport_id: Optional[int] = None
    event_date: Optional[datetime] = None
    distance_km: Optional[float] = Field(None, ge=0)
    location: Optional[str] = Field(None, max_length=300)
    target_time_seconds: Optional[int] = Field(None, ge=0)
    notes: Optional[str] = None


class RaceEventResponse(BaseModel):
    """Public race event representation."""

    id: int
    user_id: int
    name: str
    sport_id: int
    event_date: datetime
    distance_km: Optional[float]
    location: Optional[str]
    target_time_seconds: Optional[int]
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
