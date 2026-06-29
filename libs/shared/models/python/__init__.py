"""Shared Python models — re-export public API."""

from .activity import ActivityBase, ActivityCreate, ActivityResponse
from .module import ModuleBase, ModuleCreate, ModuleResponse
from .user import UserBase, UserCreate, UserResponse
from .workout import (
    ExerciseBase,
    ExerciseCreate,
    ExerciseResponse,
    RoutineBase,
    RoutineCreate,
    RoutineDetailResponse,
    RoutineExerciseBase,
    RoutineExerciseCreate,
    RoutineExerciseResponse,
    RoutineResponse,
    RoutineUpdate,
)
from .workout_log import (
    SessionComplete,
    SessionCreate,
    SessionResponse,
    SetCreate,
    SetResponse,
    WeightChartEntry,
    WeightChartResponse,
)
from .gamification import (
    AchievementBase,
    AchievementResponse,
    GamificationStatsBase,
    GamificationStatsResponse,
)
from .ai_coach import AISuggestionBase, AISuggestionResponse

__all__ = [
    "ActivityBase", "ActivityCreate", "ActivityResponse",
    "ModuleBase", "ModuleCreate", "ModuleResponse",
    "UserBase", "UserCreate", "UserResponse",
    "ExerciseBase", "ExerciseCreate", "ExerciseResponse",
    "RoutineBase", "RoutineCreate", "RoutineDetailResponse",
    "RoutineExerciseBase", "RoutineExerciseCreate", "RoutineExerciseResponse",
    "RoutineResponse", "RoutineUpdate",
    "SessionComplete", "SessionCreate", "SessionResponse",
    "SetCreate", "SetResponse",
    "WeightChartEntry", "WeightChartResponse",
    "AchievementBase", "AchievementResponse",
    "GamificationStatsBase", "GamificationStatsResponse",
    "AISuggestionBase", "AISuggestionResponse",
]
