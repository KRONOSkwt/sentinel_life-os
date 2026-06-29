package com.sentinel.shared.models

import java.time.Instant

/**
 * Shared Kotlin data classes for the Deportes (Sports) module.
 * Mirrors backend Pydantic schemas in apps/backend/src/models/schemas.py.
 */

// ---------------------------------------------------------------------------
// Sport
// ---------------------------------------------------------------------------

data class SportBase(
    val name: String,
    val icon: String? = null
)

data class SportCreate(
    val name: String,
    val icon: String? = null
)

data class SportResponse(
    val id: Int,
    val name: String,
    val icon: String? = null,
    val is_custom: Boolean,
    val created_at: Instant
)

// ---------------------------------------------------------------------------
// Sport Activity
// ---------------------------------------------------------------------------

data class SportActivityBase(
    val sport_id: Int,
    val date: Instant,
    val duration_seconds: Int,
    val distance_km: Double? = null,
    val calories: Int? = null,
    val heart_rate_avg: Int? = null,
    val extra_data: Map<String, Any>? = null,
    val notes: String? = null
)

data class SportActivityCreate(
    val sport_id: Int,
    val date: Instant,
    val duration_seconds: Int,
    val distance_km: Double? = null,
    val calories: Int? = null,
    val heart_rate_avg: Int? = null,
    val extra_data: Map<String, Any>? = null,
    val notes: String? = null
)

data class SportActivityUpdate(
    val date: Instant? = null,
    val duration_seconds: Int? = null,
    val distance_km: Double? = null,
    val calories: Int? = null,
    val heart_rate_avg: Int? = null,
    val extra_data: Map<String, Any>? = null,
    val notes: String? = null
)

data class SportActivityResponse(
    val id: Int,
    val user_id: Int,
    val sport_id: Int,
    val date: Instant,
    val duration_seconds: Int,
    val distance_km: Double? = null,
    val calories: Int? = null,
    val heart_rate_avg: Int? = null,
    val extra_data: Map<String, Any>? = null,
    val notes: String? = null,
    val created_at: Instant
)

// ---------------------------------------------------------------------------
// Sport Stats & Personal Records
// ---------------------------------------------------------------------------

data class SportStatsResponse(
    val sport_id: Int,
    val sport_name: String,
    val total_activities: Int,
    val total_time_seconds: Int,
    val total_distance_km: Double? = null,
    val average_duration_seconds: Double? = null
)

data class PersonalRecordResponse(
    val sport_id: Int,
    val best_time_seconds: Int? = null,
    val best_distance_km: Double? = null,
    val best_pace_seconds_per_km: Int? = null,
    val best_time_date: Instant? = null,
    val best_distance_date: Instant? = null
)

// ---------------------------------------------------------------------------
// Training Plan
// ---------------------------------------------------------------------------

data class TrainingPlanWeekUpdate(
    val week_number: Int,
    val target_sessions: Int,
    val completed_sessions: Int = 0,
    val notes: String? = null
)

data class TrainingPlanBase(
    val name: String,
    val description: String? = null,
    val start_date: Instant,
    val end_date: Instant
)

data class TrainingPlanCreate(
    val name: String,
    val description: String? = null,
    val start_date: Instant,
    val end_date: Instant,
    val weeks: List<TrainingPlanWeekUpdate>? = null
)

data class TrainingPlanUpdate(
    val name: String? = null,
    val description: String? = null,
    val start_date: Instant? = null,
    val end_date: Instant? = null,
    val weeks: List<TrainingPlanWeekUpdate>? = null
)

data class TrainingPlanWeekResponse(
    val id: Int,
    val week_number: Int,
    val target_sessions: Int,
    val completed_sessions: Int,
    val notes: String? = null
)

data class TrainingPlanResponse(
    val id: Int,
    val name: String,
    val description: String? = null,
    val start_date: Instant,
    val end_date: Instant,
    val created_at: Instant,
    val updated_at: Instant
)

data class TrainingPlanDetailResponse(
    val id: Int,
    val name: String,
    val description: String? = null,
    val start_date: Instant,
    val end_date: Instant,
    val created_at: Instant,
    val updated_at: Instant,
    val weeks: List<TrainingPlanWeekResponse> = emptyList()
)

// ---------------------------------------------------------------------------
// Race Event
// ---------------------------------------------------------------------------

data class RaceEventBase(
    val name: String,
    val sport_id: Int,
    val event_date: Instant,
    val distance_km: Double? = null,
    val location: String? = null,
    val target_time_seconds: Int? = null,
    val notes: String? = null
)

data class RaceEventCreate(
    val name: String,
    val sport_id: Int,
    val event_date: Instant,
    val distance_km: Double? = null,
    val location: String? = null,
    val target_time_seconds: Int? = null,
    val notes: String? = null
)

data class RaceEventUpdate(
    val name: String? = null,
    val sport_id: Int? = null,
    val event_date: Instant? = null,
    val distance_km: Double? = null,
    val location: String? = null,
    val target_time_seconds: Int? = null,
    val notes: String? = null
)

data class RaceEventResponse(
    val id: Int,
    val user_id: Int,
    val name: String,
    val sport_id: Int,
    val event_date: Instant,
    val distance_km: Double? = null,
    val location: String? = null,
    val target_time_seconds: Int? = null,
    val notes: String? = null,
    val created_at: Instant
)
