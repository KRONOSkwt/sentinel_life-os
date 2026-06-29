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
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
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
 * Mock workout history — will be replaced with API call.
 */
private data class HistorySession(
    val id: Int,
    val date: String,
    val duration: String,
    val exerciseCount: Int,
    val setCount: Int,
    val prCount: Int,
)

private val mockHistory = listOf(
    HistorySession(10, "2026-06-28", "52 min", 5, 18, 2),
    HistorySession(9, "2026-06-26", "45 min", 4, 16, 0),
    HistorySession(8, "2026-06-24", "60 min", 6, 22, 3),
    HistorySession(7, "2026-06-22", "38 min", 3, 12, 1),
    HistorySession(6, "2026-06-20", "55 min", 5, 20, 0),
    HistorySession(5, "2026-06-18", "48 min", 4, 15, 1),
    HistorySession(4, "2026-06-15", "50 min", 5, 18, 0),
    HistorySession(3, "2026-06-12", "42 min", 4, 14, 2),
    HistorySession(2, "2026-06-10", "55 min", 6, 24, 0),
    HistorySession(1, "2026-06-08", "35 min", 3, 10, 1),
)

/**
 * Workout history screen showing past sessions grouped by date.
 * Each card shows duration, exercise count, set count, and PR count.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun WorkoutHistoryScreen(
    onSessionClick: (Int) -> Unit,
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Workout History") },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = TokenColors.SurfaceBackground,
                    titleContentColor = TokenColors.TextPrimary,
                ),
            )
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
            items(mockHistory) { session ->
                HistoryCard(
                    session = session,
                    onClick = { onSessionClick(session.id) },
                )
            }
        }
    }
}

@Composable
private fun HistoryCard(
    session: HistorySession,
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
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Text(
                    text = session.date,
                    style = MaterialTheme.typography.bodyLarge,
                    fontWeight = FontWeight.Medium,
                    color = TokenColors.TextPrimary,
                )
                Text(
                    text = session.duration,
                    style = MaterialTheme.typography.bodyMedium,
                    color = TokenColors.AccentPrimary,
                )
            }
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 8.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp),
            ) {
                Text(
                    text = "${session.exerciseCount} exercises",
                    style = MaterialTheme.typography.bodySmall,
                    color = TokenColors.TextSecondary,
                )
                Text(
                    text = "${session.setCount} sets",
                    style = MaterialTheme.typography.bodySmall,
                    color = TokenColors.TextSecondary,
                )
                if (session.prCount > 0) {
                    Text(
                        text = "${session.prCount} PRs",
                        style = MaterialTheme.typography.bodySmall,
                        fontWeight = FontWeight.Bold,
                        color = TokenColors.AccentPrimary,
                    )
                }
            }
        }
    }
}
