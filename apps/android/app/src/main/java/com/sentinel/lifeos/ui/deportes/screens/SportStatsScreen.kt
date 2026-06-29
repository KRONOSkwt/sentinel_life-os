package com.sentinel.lifeos.ui.deportes.screens

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
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.ExposedDropdownMenuDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.material3.TextFieldDefaults
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
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
 * Sport stats screen — sport selector dropdown, stats grid, personal records list.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SportStatsScreen() {
    val scope = rememberCoroutineScope()
    var sports by remember { mutableStateOf(emptyList<com.sentinel.shared.models.SportResponse>()) }
    var selectedSportIndex by remember { mutableIntStateOf(0) }
    var stats by remember { mutableStateOf<com.sentinel.shared.models.SportStatsResponse?>(null) }
    var personalRecords by remember { mutableStateOf<com.sentinel.shared.models.PersonalRecordResponse?>(null) }
    var expanded by remember { mutableStateOf(false) }
    var loaded by remember { mutableStateOf(false) }

    if (!loaded) {
        loaded = true
        scope.launch {
            sports = deportesRepository.listSports()
            if (sports.isNotEmpty()) {
                val sport = sports[0]
                stats = deportesRepository.getSportStats(sport.id)
                personalRecords = deportesRepository.getPersonalRecords(sport.id)
            }
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Records") },
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
            verticalArrangement = Arrangement.spacedBy(16.dp),
        ) {
            item { Spacer(modifier = Modifier.height(8.dp)) }

            // Sport selector
            item {
                if (sports.isNotEmpty()) {
                    ExposedDropdownMenuBox(
                        expanded = expanded,
                        onExpandedChange = { expanded = it },
                    ) {
                        TextField(
                            value = sports[selectedSportIndex].let { "${it.icon ?: ""} ${it.name}" },
                            onValueChange = {},
                            readOnly = true,
                            label = { Text("Select sport") },
                            trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = expanded) },
                            modifier = Modifier
                                .fillMaxWidth()
                                .menuAnchor(),
                            colors = TextFieldDefaults.colors(
                                focusedContainerColor = TokenColors.GlassCardBackground,
                                unfocusedContainerColor = TokenColors.GlassCardBackground,
                                focusedTextColor = TokenColors.TextPrimary,
                                unfocusedTextColor = TokenColors.TextPrimary,
                                focusedLabelColor = TokenColors.TextSecondary,
                                unfocusedLabelColor = TokenColors.TextSecondary,
                            ),
                        )
                        ExposedDropdownMenu(
                            expanded = expanded,
                            onDismissRequest = { expanded = false },
                        ) {
                            sports.forEachIndexed { index, sport ->
                                DropdownMenuItem(
                                    text = { Text("${sport.icon ?: ""} ${sport.name}") },
                                    onClick = {
                                        selectedSportIndex = index
                                        expanded = false
                                        scope.launch {
                                            stats = deportesRepository.getSportStats(sport.id)
                                            personalRecords = deportesRepository.getPersonalRecords(sport.id)
                                        }
                                    },
                                )
                            }
                        }
                    }
                }
            }

            // Stats grid
            stats?.let { s ->
                item {
                    Text(
                        text = "Statistics",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.SemiBold,
                        color = TokenColors.TextPrimary,
                    )
                }
                item {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                    ) {
                        StatItem(
                            label = "Activities",
                            value = "${s.total_activities}",
                            modifier = Modifier.weight(1f),
                        )
                        StatItem(
                            label = "Total Time",
                            value = formatDuration(s.total_time_seconds),
                            modifier = Modifier.weight(1f),
                        )
                    }
                }
                item {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                    ) {
                        s.total_distance_km?.let { dist ->
                            StatItem(
                                label = "Total Distance",
                                value = String.format("%.1f km", dist),
                                modifier = Modifier.weight(1f),
                            )
                        }
                        s.average_duration_seconds?.let { avg ->
                            StatItem(
                                label = "Avg Duration",
                                value = formatDuration(avg.toInt()),
                                modifier = Modifier.weight(1f),
                            )
                        }
                    }
                }
            }

            // Personal Records
            personalRecords?.let { pr ->
                item {
                    Text(
                        text = "Personal Records",
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.SemiBold,
                        color = TokenColors.TextPrimary,
                        modifier = Modifier.padding(top = 8.dp),
                    )
                }

                pr.best_time_seconds?.let { time ->
                    item {
                        PRRow(
                            label = "Best Time",
                            value = formatDuration(time),
                            date = pr.best_time_date,
                        )
                    }
                }
                pr.best_distance_km?.let { dist ->
                    item {
                        PRRow(
                            label = "Best Distance",
                            value = String.format("%.1f km", dist),
                            date = pr.best_distance_date,
                        )
                    }
                }
                pr.best_pace_seconds_per_km?.let { pace ->
                    item {
                        PRRow(
                            label = "Best Pace",
                            value = formatPace(pace),
                            date = null,
                        )
                    }
                }

                // Empty state
                if (pr.best_time_seconds == null && pr.best_distance_km == null && pr.best_pace_seconds_per_km == null) {
                    item {
                        Text(
                            text = "No records yet. Log activities to set personal records!",
                            style = MaterialTheme.typography.bodyMedium,
                            color = TokenColors.TextSecondary,
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun StatItem(
    label: String,
    value: String,
    modifier: Modifier = Modifier,
) {
    Card(
        modifier = modifier,
        colors = CardDefaults.cardColors(
            containerColor = TokenColors.GlassCardBackground,
        ),
        shape = MaterialTheme.shapes.medium,
    ) {
        Column(
            modifier = Modifier.padding(12.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
        ) {
            Text(
                text = value,
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
                color = TokenColors.AccentPrimary,
            )
            Text(
                text = label,
                style = MaterialTheme.typography.labelSmall,
                color = TokenColors.TextSecondary,
            )
        }
    }
}

@Composable
private fun PRRow(
    label: String,
    value: String,
    date: Instant?,
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
                .padding(12.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Column {
                Text(
                    text = label,
                    style = MaterialTheme.typography.bodyMedium,
                    color = TokenColors.TextSecondary,
                )
                date?.let {
                    Text(
                        text = formatDate(it),
                        style = MaterialTheme.typography.labelSmall,
                        color = TokenColors.TextSecondary,
                    )
                }
            }
            Text(
                text = value,
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold,
                color = TokenColors.AccentPrimary,
            )
        }
    }
}

private fun formatDuration(seconds: Int): String {
    val hours = seconds / 3600
    val minutes = (seconds % 3600) / 60
    val secs = seconds % 60
    return if (hours > 0) {
        String.format("%dh %02dm", hours, minutes)
    } else {
        String.format("%dm %02ds", minutes, secs)
    }
}

private fun formatPace(secondsPerKm: Int): String {
    val minutes = secondsPerKm / 60
    val secs = secondsPerKm % 60
    return String.format("%d:%02d /km", minutes, secs)
}

private fun formatDate(instant: Instant): String {
    val formatter = DateTimeFormatter.ofPattern("MMM d, yyyy")
        .withZone(ZoneId.systemDefault())
    return formatter.format(instant)
}
