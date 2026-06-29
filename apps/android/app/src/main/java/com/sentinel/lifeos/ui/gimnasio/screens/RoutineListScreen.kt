package com.sentinel.lifeos.ui.gimnasio.screens

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.sentinel.lifeos.ui.theme.TokenColors

/**
 * Mock data for routine list — will be replaced with API call.
 */
private data class RoutineSummary(
    val id: Int,
    val name: String,
    val description: String?,
    val exerciseCount: Int,
)

private val mockRoutines = listOf(
    RoutineSummary(1, "Push Day", "Chest, shoulders, triceps", 6),
    RoutineSummary(2, "Pull Day", "Back, biceps", 5),
    RoutineSummary(3, "Leg Day", "Quads, hamstrings, glutes", 7),
    RoutineSummary(4, "Full Body", "Complete workout", 8),
)

/**
 * Screen displaying the list of workout routines.
 * Each item shows name, description, and exercise count.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RoutineListScreen(
    onRoutineClick: (Int) -> Unit,
) {
    var routines by remember { mutableStateOf(mockRoutines) }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Routines") },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = TokenColors.SurfaceBackground,
                    titleContentColor = TokenColors.TextPrimary,
                ),
            )
        },
        floatingActionButton = {
            FloatingActionButton(
                onClick = { /* TODO: open create routine dialog */ },
                containerColor = TokenColors.AccentPrimary,
            ) {
                Icon(Icons.Default.Add, contentDescription = "Create routine")
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
            items(routines) { routine ->
                RoutineCard(
                    routine = routine,
                    onClick = { onRoutineClick(routine.id) },
                )
            }
        }
    }
}

@Composable
private fun RoutineCard(
    routine: RoutineSummary,
    onClick: () -> Unit,
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        colors = CardDefaults.cardColors(
            containerColor = TokenColors.GlassCardBackground,
        ),
        shape = MaterialTheme.shapes.medium,
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = routine.name,
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.SemiBold,
                color = TokenColors.TextPrimary,
            )
            if (routine.description != null) {
                Text(
                    text = routine.description,
                    style = MaterialTheme.typography.bodySmall,
                    color = TokenColors.TextSecondary,
                    modifier = Modifier.padding(top = 4.dp),
                )
            }
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 8.dp),
                horizontalArrangement = Arrangement.End,
            ) {
                Text(
                    text = "${routine.exerciseCount} exercises",
                    style = MaterialTheme.typography.labelSmall,
                    color = TokenColors.AccentPrimary,
                )
            }
        }
    }
}
