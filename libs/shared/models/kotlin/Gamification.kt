package com.sentinel.shared.models

import java.time.Instant

/**
 * Shared Kotlin data classes for gamification stats and achievements.
 */

data class GamificationStatsBase(
    val total_points: Int = 0,
    val current_streak: Int = 0,
    val longest_streak: Int = 0,
    val level: Int = 1
)

data class GamificationStatsResponse(
    val total_points: Int,
    val current_streak: Int,
    val longest_streak: Int,
    val level: Int,
    val last_workout_date: Instant? = null
)

data class AchievementBase(
    val achievement_key: String
)

data class AchievementResponse(
    val id: Int,
    val achievement_key: String,
    val unlocked_at: Instant
)
