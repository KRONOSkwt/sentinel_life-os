package com.sentinel.lifeos.ui.deportes.components

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.sentinel.lifeos.ui.theme.TokenColors
import com.sentinel.shared.models.SportActivityResponse
import java.time.Instant
import java.time.ZoneId
import java.time.format.DateTimeFormatter

/**
 * Reusable card for activity list items.
 * Shows sport icon, date, duration, distance.
 */
@Composable
fun ActivityCard(
    activity: SportActivityResponse,
    sportName: String,
    sportIcon: String?,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
) {
    Card(
        modifier = modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
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
            horizontalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            // Sport icon
            Text(
                text = sportIcon ?: "\uD83C\uDFC3",
                style = MaterialTheme.typography.headlineMedium,
            )

            // Activity info
            Column(
                modifier = Modifier.weight(1f),
                verticalArrangement = Arrangement.spacedBy(2.dp),
            ) {
                Text(
                    text = sportName,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold,
                    color = TokenColors.TextPrimary,
                )
                Text(
                    text = formatDate(activity.date),
                    style = MaterialTheme.typography.bodySmall,
                    color = TokenColors.TextSecondary,
                )
                if (activity.notes != null) {
                    Text(
                        text = activity.notes,
                        style = MaterialTheme.typography.bodySmall,
                        color = TokenColors.TextSecondary,
                        maxLines = 1,
                    )
                }
            }

            // Duration + distance
            Column(
                horizontalAlignment = Alignment.End,
                verticalArrangement = Arrangement.spacedBy(2.dp),
            ) {
                Text(
                    text = formatDuration(activity.duration_seconds),
                    style = MaterialTheme.typography.bodyMedium,
                    fontWeight = FontWeight.Medium,
                    color = TokenColors.AccentPrimary,
                )
                if (activity.distance_km != null) {
                    Text(
                        text = String.format("%.1f km", activity.distance_km),
                        style = MaterialTheme.typography.bodySmall,
                        color = TokenColors.TextSecondary,
                    )
                }
                if (activity.calories != null) {
                    Text(
                        text = "${activity.calories} cal",
                        style = MaterialTheme.typography.labelSmall,
                        color = TokenColors.TextSecondary,
                    )
                }
            }
        }
    }
}

private fun formatDate(instant: Instant): String {
    val formatter = DateTimeFormatter.ofPattern("MMM d, yyyy • HH:mm")
        .withZone(ZoneId.systemDefault())
    return formatter.format(instant)
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
