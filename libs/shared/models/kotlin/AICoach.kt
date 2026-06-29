package com.sentinel.shared.models

/**
 * Shared Kotlin data classes for AI coach suggestions.
 */

data class AISuggestionBase(
    val exercise_id: Int,
    val exercise_name: String,
    val current_weight: Double,
    val suggested_weight: Double,
    val reason: String,
    val confidence: Double
)

data class AISuggestionResponse(
    val exercise_id: Int,
    val exercise_name: String,
    val current_weight: Double,
    val suggested_weight: Double,
    val reason: String,
    val confidence: Double
)
