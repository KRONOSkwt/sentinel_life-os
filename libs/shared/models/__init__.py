"""Shared models package — aggregates Python and (future) Kotlin/WASM models."""

from .python import (
    ActivityBase, ActivityCreate, ActivityResponse,
    ModuleBase, ModuleCreate, ModuleResponse,
    UserBase, UserCreate, UserResponse,
    ExerciseBase, ExerciseCreate, ExerciseResponse,
    RoutineBase, RoutineCreate, RoutineDetailResponse,
    RoutineExerciseBase, RoutineExerciseCreate, RoutineExerciseResponse,
    RoutineResponse, RoutineUpdate,
    SessionComplete, SessionCreate, SessionResponse,
    SetCreate, SetResponse,
    WeightChartEntry, WeightChartResponse,
    AchievementBase, AchievementResponse,
    GamificationStatsBase, GamificationStatsResponse,
    AISuggestionBase, AISuggestionResponse,
)

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
