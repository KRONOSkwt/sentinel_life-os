package com.sentinel.lifeos.shared.models

data class Activity(
    val id: Int,
    val module_id: Int,
    val type: String,
    val value: Double,
    val metadata: Map<String, Any>? = null,
    val created_at: String
)

data class ActivityCreate(
    val module_id: Int,
    val type: String,
    val value: Double,
    val metadata: Map<String, Any>? = null
)