package com.sentinel.lifeos.ui.gimnasio.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.sentinel.lifeos.ui.theme.TokenColors

/**
 * Mock data for routine detail — will be replaced with API call.
 */
private data class RoutineExerciseItem(
    val exerciseName: String,
    val category: String,
    val targetSets: Int,
    val targetReps: Int,
    val order: Int,
)

private val mockExercises = listOf(
    RoutineExerciseItem("Bench Press", "strength", 4, 8, 1),
    RoutineExerciseItem("Overhead Press", "strength", 3, 10, 2),
    RoutineExerciseItem("Incline Dumbbell Press", "strength", 3, 12, 3),
    RoutineExerciseItem("Lateral Raises", "strength", 3, 15, 4),
    RoutineExerciseItem("Tricep Pushdowns", "strength", 3, 12, 5),
    RoutineExerciseItem("Chest Flyes", "strength", 3, 15, 6),
)

/**
 * Screen showing routine details with its ordered exercises.
 * Displays target sets/reps per exercise and a "Start Workout" FAB.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RoutineDetailScreen(
    routineId: Int,
    onBack: () -> Unit,
    onStartWorkout: (Int) -> Unit,
) {
    val routineName = "Push Day" // TODO: fetch from API
    val exercises = mockExercises // TODO: fetch from API

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(routineName) },
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
        floatingActionButton = {
            FloatingActionButton(
                onClick = { onStartWorkout(routineId) },
                containerColor = TokenColors.AccentPrimary,
            ) {
                Icon(Icons.Default.PlayArrow, contentDescription = "Start workout")
            }
        },
        containerColor = TokenColors.SurfaceBackground,
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(horizontal = 16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            item { Spacer(modifier = Modifier.height(8.dp)) }
            itemsIndexed(exercises) { index, exercise ->
                ExerciseItemCard(
                    order = index + 1,
                    exercise = exercise,
                )
            }
            item { Spacer(modifier = Modifier.height(80.dp)) }
        }
    }
}

@Composable
private fun ExerciseItemCard(
    order: Int,
    exercise: RoutineExerciseItem,
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = TokenColors.GlassCardBackground,
        ),
        shape = MaterialTheme.shapes.medium,
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text(
                text = "$order",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold,
                color = TokenColors.AccentPrimary,
                modifier = Modifier.padding(end = 12.dp),
            )
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = exercise.exerciseName,
                    style = MaterialTheme.typography.bodyLarge,
                    fontWeight = FontWeight.Medium,
                    color = TokenColors.TextPrimary,
                )
                Text(
                    text = exercise.category.replaceFirstChar { it.uppercase() },
                    style = MaterialTheme.typography.bodySmall,
                    color = TokenColors.TextSecondary,
                )
            }
            Column(horizontalAlignment = Alignment.End) {
                Text(
                    text = "${exercise.targetSets} x ${exercise.targetReps}",
                    style = MaterialTheme.typography.bodyMedium,
                    fontWeight = FontWeight.Medium,
                    color = TokenColors.TextPrimary,
                )
                Text(
                    text = "sets x reps",
                    style = MaterialTheme.typography.labelSmall,
                    color = TokenColors.TextSecondary,
                )
            }
        }
    }
}
