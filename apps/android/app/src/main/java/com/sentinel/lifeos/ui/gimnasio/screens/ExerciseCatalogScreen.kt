package com.sentinel.lifeos.ui.gimnasio.screens

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.FilterChipDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.sentinel.lifeos.ui.theme.TokenColors

private data class ExerciseItem(
    val id: Int,
    val name: String,
    val category: String,
    val muscleGroups: List<String>,
)

private val categories = listOf("All", "Strength", "Cardio", "Flexibility")

private val mockExercises = listOf(
    ExerciseItem(1, "Bench Press", "strength", listOf("chest", "triceps")),
    ExerciseItem(2, "Squat", "strength", listOf("quads", "glutes")),
    ExerciseItem(3, "Deadlift", "strength", listOf("back", "hamstrings")),
    ExerciseItem(4, "Overhead Press", "strength", listOf("shoulders", "triceps")),
    ExerciseItem(5, "Barbell Row", "strength", listOf("back", "biceps")),
    ExerciseItem(6, "Pull-ups", "strength", listOf("back", "biceps")),
    ExerciseItem(7, "Treadmill Run", "cardio", listOf("legs", "cardio")),
    ExerciseItem(8, "Cycling", "cardio", listOf("legs", "cardio")),
    ExerciseItem(9, "Jump Rope", "cardio", listOf("cardio", "calves")),
    ExerciseItem(10, "Hamstring Stretch", "flexibility", listOf("hamstrings")),
    ExerciseItem(11, "Hip Flexor Stretch", "flexibility", listOf("hip flexors")),
    ExerciseItem(12, "Lateral Raises", "strength", listOf("shoulders")),
)

/**
 * Exercise catalog screen with search and category filter chips.
 * Displays exercises in a filterable list.
 */
@OptIn(ExperimentalMaterial3Api::class, ExperimentalLayoutApi::class)
@Composable
fun ExerciseCatalogScreen(
    onBack: () -> Unit,
) {
    var searchQuery by remember { mutableStateOf("") }
    var selectedCategory by remember { mutableStateOf("All") }

    val filteredExercises = mockExercises.filter { exercise ->
        val matchesSearch = searchQuery.isBlank() ||
            exercise.name.contains(searchQuery, ignoreCase = true) ||
            exercise.muscleGroups.any { it.contains(searchQuery, ignoreCase = true) }
        val matchesCategory = selectedCategory == "All" ||
            exercise.category.equals(selectedCategory, ignoreCase = true)
        matchesSearch && matchesCategory
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Exercises") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(
                            Icons.AutoMirrored.Filled.ArrowBack,
                            contentDescription = "Back",
                            tint = TokenColors.TextPrimary,
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = TokenColors.SurfaceBackground,
                    titleContentColor = TokenColors.TextPrimary,
                ),
            )
        },
        containerColor = TokenColors.SurfaceBackground,
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(horizontal = 16.dp),
        ) {
            // Search bar
            OutlinedTextField(
                value = searchQuery,
                onValueChange = { searchQuery = it },
                modifier = Modifier.fillMaxWidth(),
                placeholder = { Text("Search exercises...", color = TokenColors.TextSecondary) },
                colors = OutlinedTextFieldDefaults.colors(
                    focusedBorderColor = TokenColors.AccentPrimary,
                    unfocusedBorderColor = TokenColors.GlassBorder,
                    focusedContainerColor = TokenColors.GlassCardBackground,
                    unfocusedContainerColor = TokenColors.GlassCardBackground,
                ),
                singleLine = true,
            )

            // Category chips
            FlowRow(
                modifier = Modifier.padding(vertical = 8.dp),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                categories.forEach { category ->
                    FilterChip(
                        selected = selectedCategory == category,
                        onClick = { selectedCategory = category },
                        label = { Text(category) },
                        colors = FilterChipDefaults.filterChipColors(
                            selectedContainerColor = TokenColors.AccentPrimary,
                            selectedLabelColor = TokenColors.TextPrimary,
                            containerColor = TokenColors.GlassCardBackground,
                            labelColor = TokenColors.TextSecondary,
                        ),
                    )
                }
            }

            // Exercise list
            LazyColumn(
                verticalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                item { Spacer(modifier = Modifier.height(4.dp)) }
                items(filteredExercises) { exercise ->
                    ExerciseCard(exercise)
                }
            }
        }
    }
}

@Composable
private fun ExerciseCard(exercise: ExerciseItem) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = TokenColors.GlassCardBackground,
        ),
        shape = MaterialTheme.shapes.medium,
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = exercise.name,
                style = MaterialTheme.typography.bodyLarge,
                fontWeight = FontWeight.Medium,
                color = TokenColors.TextPrimary,
            )
            Text(
                text = exercise.muscleGroups.joinToString(", ") {
                    it.replaceFirstChar { c -> c.uppercase() }
                },
                style = MaterialTheme.typography.bodySmall,
                color = TokenColors.TextSecondary,
                modifier = Modifier.padding(top = 4.dp),
            )
            Text(
                text = exercise.category.replaceFirstChar { it.uppercase() },
                style = MaterialTheme.typography.labelSmall,
                color = TokenColors.AccentPrimary,
                modifier = Modifier.padding(top = 4.dp),
            )
        }
    }
}
