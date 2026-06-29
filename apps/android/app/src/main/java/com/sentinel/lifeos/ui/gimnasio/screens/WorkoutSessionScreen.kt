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
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Slider
import androidx.compose.material3.SliderDefaults
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.sentinel.lifeos.ui.gimnasio.components.WorkoutSetRow
import com.sentinel.lifeos.ui.theme.TokenColors

/**
 * Mock data for active session — will be replaced with API calls.
 */
private data class ActiveSet(
    val exerciseName: String,
    val setNumber: Int,
    val weight: Double,
    val reps: Int,
    val rpe: Double?,
    val isPr: Boolean,
)

private val mockSets = listOf(
    ActiveSet("Bench Press", 1, 80.0, 8, null, false),
    ActiveSet("Bench Press", 2, 80.0, 8, 7.0, false),
    ActiveSet("Bench Press", 3, 82.5, 8, 8.0, true),
    ActiveSet("Overhead Press", 1, 40.0, 10, 6.5, false),
    ActiveSet("Overhead Press", 2, 40.0, 10, 7.0, false),
)

/**
 * Active workout session screen.
 * Displays logged sets with RPE slider and set logging controls.
 * Shows session duration timer (mock) and complete button.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun WorkoutSessionScreen() {
    var rpe by remember { mutableFloatStateOf(7f) }
    val sets = remember { mutableStateOf(mockSets) }
    val sessionDuration = "00:42:15" // TODO: real timer

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Column {
                        Text("Active Session", color = TokenColors.TextPrimary)
                        Text(
                            text = sessionDuration,
                            style = MaterialTheme.typography.bodySmall,
                            color = TokenColors.TextSecondary,
                        )
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = TokenColors.SurfaceBackground,
                    titleContentColor = TokenColors.TextPrimary,
                ),
                actions = {
                    IconButton(onClick = { /* TODO: cancel session */ }) {
                        Icon(
                            Icons.Default.Close,
                            contentDescription = "Cancel",
                            tint = TokenColors.TextSecondary,
                        )
                    }
                },
            )
        },
        floatingActionButton = {
            Row(
                horizontalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                FloatingActionButton(
                    onClick = { /* TODO: add set */ },
                    containerColor = TokenColors.AccentSecondary,
                ) {
                    Icon(Icons.Default.Add, contentDescription = "Add set")
                }
                FloatingActionButton(
                    onClick = { /* TODO: complete session */ },
                    containerColor = TokenColors.AccentPrimary,
                ) {
                    Icon(Icons.Default.Check, contentDescription = "Complete")
                }
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

            // RPE slider
            item {
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(
                        containerColor = TokenColors.GlassCardBackground,
                    ),
                    shape = MaterialTheme.shapes.medium,
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Text(
                            text = "RPE: ${rpe.toInt()}",
                            style = MaterialTheme.typography.bodyMedium,
                            fontWeight = FontWeight.Medium,
                            color = TokenColors.TextPrimary,
                        )
                        Slider(
                            value = rpe,
                            onValueChange = { rpe = it },
                            valueRange = 1f..10f,
                            steps = 8,
                            colors = SliderDefaults.colors(
                                thumbColor = TokenColors.AccentPrimary,
                                activeTrackColor = TokenColors.AccentPrimary,
                            ),
                        )
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                        ) {
                            Text("1", style = MaterialTheme.typography.labelSmall, color = TokenColors.TextSecondary)
                            Text("10", style = MaterialTheme.typography.labelSmall, color = TokenColors.TextSecondary)
                        }
                    }
                }
            }

            // Sets grouped by exercise
            val grouped = sets.value.groupBy { it.exerciseName }
            grouped.forEach { (exerciseName, exerciseSets) ->
                item {
                    Text(
                        text = exerciseName,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.SemiBold,
                        color = TokenColors.TextPrimary,
                        modifier = Modifier.padding(top = 8.dp),
                    )
                }
                itemsIndexed(exerciseSets) { _, set ->
                    WorkoutSetRow(
                        setNumber = set.setNumber,
                        weight = set.weight,
                        reps = set.reps,
                        rpe = set.rpe,
                        isPr = set.isPr,
                    )
                }
            }

            item { Spacer(modifier = Modifier.height(80.dp)) }
        }
    }
}
