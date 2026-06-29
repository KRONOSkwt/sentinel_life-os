package com.sentinel.lifeos.ui.deportes.components

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.sentinel.lifeos.ui.theme.TokenColors
import com.sentinel.shared.models.RaceEventResponse
import java.time.Instant
import java.time.ZoneId
import java.time.format.DateTimeFormatter
import java.time.temporal.ChronoUnit

/**
 * Reusable card for race list items.
 * Shows race name, date, distance, location, and countdown.
 */
@Composable
fun RaceCard(
    race: RaceEventResponse,
    sportName: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
) {
    val now = Instant.now()
    val daysUntil = ChronoUnit.DAYS.between(now, race.event_date).toInt()
    val isPast = daysUntil < 0

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
            // Race info
            Column(
                modifier = Modifier.weight(1f),
                verticalArrangement = Arrangement.spacedBy(4.dp),
            ) {
                Text(
                    text = race.name,
                    style = MaterialTheme.typography.titleMedium,
                    fontWeight = FontWeight.SemiBold,
                    color = TokenColors.TextPrimary,
                )
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Text(
                        text = formatDate(race.event_date),
                        style = MaterialTheme.typography.bodySmall,
                        color = TokenColors.TextSecondary,
                    )
                    Text(
                        text = sportName,
                        style = MaterialTheme.typography.bodySmall,
                        color = TokenColors.AccentSecondary,
                    )
                }
                if (race.distance_km != null) {
                    Text(
                        text = String.format("%.1f km", race.distance_km),
                        style = MaterialTheme.typography.bodySmall,
                        color = TokenColors.TextSecondary,
                    )
                }
                if (race.location != null) {
                    Text(
                        text = race.location,
                        style = MaterialTheme.typography.bodySmall,
                        color = TokenColors.TextSecondary,
                    )
                }
            }

            // Countdown badge
            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
            ) {
                if (isPast) {
                    Text(
                        text = "Past",
                        fontSize = 14.sp,
                        fontWeight = FontWeight.Bold,
                        color = TokenColors.TextSecondary,
                    )
                } else {
                    Text(
                        text = "$daysUntil",
                        fontSize = 28.sp,
                        fontWeight = FontWeight.Bold,
                        color = TokenColors.AccentPrimary,
                    )
                    Text(
                        text = if (daysUntil == 1) "day" else "days",
                        style = MaterialTheme.typography.labelSmall,
                        color = TokenColors.TextSecondary,
                    )
                }
            }
        }
    }
}

private fun formatDate(instant: Instant): String {
    val formatter = DateTimeFormatter.ofPattern("MMM d, yyyy")
        .withZone(ZoneId.systemDefault())
    return formatter.format(instant)
}
