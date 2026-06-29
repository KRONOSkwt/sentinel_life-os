package com.sentinel.shared.models

import java.time.Instant

/**
 * Shared Kotlin data classes for workout sessions and sets.
 */

data class SetBase(
    val exercise_id: Int,
    val set_number: Int,
    val weight: Double,
    val reps: Int,
    val rpe: Double? = null
)

data class SetCreate(
    val exercise_id: Int,
    val set_number: Int,
    val weight: Double,
    val reps: Int,
    val rpe: Double? = null
)

data class SetResponse(
    val id: Int,
    val session_id: Int,
    val exercise_id: Int,
    val set_number: Int,
    val weight: Double,
    val reps: Int,
    val rpe: Double?,
    val is_pr: Boolean,
    val created_at: Instant
)

data class SessionBase(
    val routine_id: Int? = null
)

data class SessionCreate(
    val routine_id: Int? = null
)

data class SessionComplete(
    val notes: String? = null
)

data class SessionResponse(
    val id: Int,
    val user_id: Int,
    val routine_id: Int?,
    val started_at: Instant,
    val completed_at: Instant?,
    val duration_seconds: Int?,
    val notes: String?,
    val sets: List<SetResponse> = emptyList(),
    val created_at: Instant
)

data class WeightChartEntry(
    val date: Instant,
    val weight: Double,
    val reps: Int,
    val set_number: Int
)

data class WeightChartResponse(
    val exercise_id: Int,
    val exercise_name: String,
    val data: List<WeightChartEntry>
)
