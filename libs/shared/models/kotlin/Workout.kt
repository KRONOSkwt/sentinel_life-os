package com.sentinel.shared.models

import java.time.Instant

/**
 * Shared Kotlin data classes for workout routines and exercises.
 */

data class ExerciseBase(
    val name: String,
    val category: String, // strength|cardio|flexibility
    val muscle_groups: List<String>,
    val equipment: String? = null
)

data class ExerciseCreate(
    val name: String,
    val category: String,
    val muscle_groups: List<String>,
    val equipment: String? = null
)

data class ExerciseResponse(
    val id: Int,
    val name: String,
    val category: String,
    val muscle_groups: List<String>,
    val equipment: String?,
    val is_custom: Boolean,
    val created_at: Instant
)

data class RoutineExerciseBase(
    val exercise_id: Int,
    val target_sets: Int,
    val target_reps: Int,
    val order: Int
)

data class RoutineExerciseCreate(
    val exercise_id: Int,
    val target_sets: Int,
    val target_reps: Int,
    val order: Int
)

data class RoutineExerciseResponse(
    val id: Int,
    val exercise_id: Int,
    val exercise: ExerciseResponse,
    val target_sets: Int,
    val target_reps: Int,
    val order: Int
)

data class RoutineBase(
    val name: String,
    val description: String? = null
)

data class RoutineCreate(
    val name: String,
    val description: String? = null,
    val exercises: List<RoutineExerciseCreate> = emptyList()
)

data class RoutineUpdate(
    val name: String? = null,
    val description: String? = null,
    val exercises: List<RoutineExerciseCreate>? = null
)

data class RoutineResponse(
    val id: Int,
    val name: String,
    val description: String?,
    val created_at: Instant,
    val updated_at: Instant
)

data class RoutineDetailResponse(
    val id: Int,
    val name: String,
    val description: String?,
    val created_at: Instant,
    val updated_at: Instant,
    val exercises: List<RoutineExerciseResponse> = emptyList()
)
