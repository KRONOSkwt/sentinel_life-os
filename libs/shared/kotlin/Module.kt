package com.sentinel.lifeos.shared.models

data class Module(
    val id: Int,
    val name: String,
    val description: String,
    val enabled: Boolean,
    val created_at: String
)

data class ModuleCreate(
    val name: String,
    val description: String
)