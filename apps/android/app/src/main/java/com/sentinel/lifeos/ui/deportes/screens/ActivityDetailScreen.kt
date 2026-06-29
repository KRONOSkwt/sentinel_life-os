package com.sentinel.lifeos.ui.deportes.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.sentinel.lifeos.ui.deportes.deportesRepository
import com.sentinel.lifeos.ui.theme.TokenColors
import kotlinx.coroutines.launch
import java.time.Instant
import java.time.ZoneId
import java.time.format.DateTimeFormatter

/**
 * Full activity detail display with edit/delete buttons.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ActivityDetailScreen(
    activityId: Int,
    onBack: () -> Unit,
) {
    val scope = rememberCoroutineScope()
    var activity by remember { mutableStateOf<com.sentinel.shared.models.SportActivityResponse?>(null) }
    var sportName by remember { mutableStateOf("") }
    var sportIcon by remember { mutableStateOf<String?>(null) }
    var loaded by remember { mutableStateOf(false) }

    if (!loaded) {
        loaded = true
        scope.launch {
            activity = deportesRepository.getActivity(activityId)
            activity?.let { act ->
                val sports = deportesRepository.listSports()
                val sport = sports.firstOrNull { it.id == act.sport_id }
                sportName = sport?.name ?: "Sport #${act.sport_id}"
                sportIcon = sport?.icon
            }
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Activity Detail") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.Default.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    IconButton(onClick = { /* TODO: open edit dialog */ }) {
                        Icon(Icons.Default.Edit, contentDescription = "Edit", tint = TokenColors.AccentPrimary)
                    }
                    IconButton(onClick = {
                        scope.launch {
                            deportesRepository.deleteActivity(activityId)
                            onBack()
                        }
                    }) {
                        Icon(Icons.Default.Delete, contentDescription = "Delete", tint = TokenColors.TextSecondary)
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
        activity?.let { act ->
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding)
                    .padding(16.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp),
            ) {
                // Header with icon and sport name
                Row(
                    horizontalArrangement = Arrangement.spacedBy(12.dp),
                ) {
                    Text(
                        text = sportIcon ?: "\uD83C\uDFC3",
                        style = MaterialTheme.typography.headlineLarge,
                    )
                    Column {
                        Text(
                            text = sportName,
                            style = MaterialTheme.typography.headlineSmall,
                            fontWeight = FontWeight.Bold,
                            color = TokenColors.TextPrimary,
                        )
                        Text(
                            text = formatDate(act.date),
                            style = MaterialTheme.typography.bodyMedium,
                            color = TokenColors.TextSecondary,
                        )
                    }
                }

                // Stats card
                Card(
                    modifier = Modifier.fillMaxWidth(),
                    colors = CardDefaults.cardColors(
                        containerColor = TokenColors.GlassCardBackground,
                    ),
                    shape = MaterialTheme.shapes.medium,
                ) {
                    Column(
                        modifier = Modifier.padding(16.dp),
                        verticalArrangement = Arrangement.spacedBy(12.dp),
                    ) {
                        DetailRow("Duration", formatDuration(act.duration_seconds))
                        act.distance_km?.let {
                            DetailRow("Distance", String.format("%.1f km", it))
                        }
                        act.calories?.let {
                            DetailRow("Calories", "$it cal")
                        }
                        act.heart_rate_avg?.let {
                            DetailRow("Avg Heart Rate", "$it bpm")
                        }
                    }
                }

                // Notes card
                act.notes?.let { notes ->
                    Card(
                        modifier = Modifier.fillMaxWidth(),
                        colors = CardDefaults.cardColors(
                            containerColor = TokenColors.GlassCardBackground,
                        ),
                        shape = MaterialTheme.shapes.medium,
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            Text(
                                text = "Notes",
                                style = MaterialTheme.typography.labelMedium,
                                color = TokenColors.TextSecondary,
                            )
                            Text(
                                text = notes,
                                style = MaterialTheme.typography.bodyMedium,
                                color = TokenColors.TextPrimary,
                                modifier = Modifier.padding(top = 4.dp),
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun DetailRow(label: String, value: String) {
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.SpaceBetween,
    ) {
        Text(
            text = label,
            style = MaterialTheme.typography.bodyMedium,
            color = TokenColors.TextSecondary,
        )
        Text(
            text = value,
            style = MaterialTheme.typography.bodyMedium,
            fontWeight = FontWeight.Medium,
            color = TokenColors.TextPrimary,
        )
    }
}

private fun formatDate(instant: Instant): String {
    val formatter = DateTimeFormatter.ofPattern("EEEE, MMMM d, yyyy • HH:mm")
        .withZone(ZoneId.systemDefault())
    return formatter.format(instant)
}

private fun formatDuration(seconds: Int): String {
    val hours = seconds / 3600
    val minutes = (seconds % 3600) / 60
    val secs = seconds % 60
    return if (hours > 0) {
        String.format("%dh %02dm %02ds", hours, minutes, secs)
    } else {
        String.format("%dm %02ds", minutes, secs)
    }
}
