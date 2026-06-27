package com.sentinel.lifeos.shared.models

data class User(
    val id: Int,
    val email: String,
    val display_name: String,
    val created_at: String
)

data class UserCreate(
    val email: String,
    val password: String,
    val display_name: String
)