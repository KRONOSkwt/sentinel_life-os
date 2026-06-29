package com.sentinel.lifeos.ui.gimnasio.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.sentinel.lifeos.ui.gimnasio.components.HeatmapCell
import com.sentinel.lifeos.ui.theme.TokenColors
import java.time.LocalDate
import java.time.Year
import java.time.format.DateTimeFormatter
import java.time.temporal.ChronoUnit

/**
 * Generate mock heatmap data for the current year.
 * In production this comes from GET /gimnasio/heatmap?year=YYYY.
 */
private fun generateMockHeatmapData(): Map<LocalDate, Int> {
    val data = mutableMapOf<LocalDate, Int>()
    val today = LocalDate.now()
    val startOfYear = Year.now().atDay(1)
    val daysBetween = ChronoUnit.DAYS.between(startOfYear, today).toInt()

    // Simulate some workout days with varying intensity
    val workoutDays = setOf(
        2, 5, 7, 9, 12, 14, 16, 19, 21, 23, 26, 28, 30, 33, 35, 37, 40, 42,
        44, 47, 49, 51, 54, 56, 58, 61, 63, 65, 68, 70, 72, 75, 77, 79, 82,
        84, 86, 89, 91, 93, 96, 98, 100, 103, 105, 107, 110, 112, 114, 117,
        119, 121, 124, 126, 128, 131, 133, 135, 138, 140, 142, 145, 147, 149,
        152, 154, 156, 159, 161, 163, 166, 168, 170, 173, 175, 177, 180, 182,
    )

    for (dayOffset in 0..daysBetween) {
        val date = startOfYear.plusDays(dayOffset.toLong())
        val intensity = when {
            dayOffset in workoutDays && dayOffset % 10 == 0 -> 3
            dayOffset in workoutDays && dayOffset % 3 == 0 -> 2
            dayOffset in workoutDays -> 1
            else -> 0
        }
        data[date] = intensity
    }
    return data
}

/**
 * Heatmap calendar screen — renders a 365-day grid similar to GitHub's contribution graph.
 * Uses a horizontal scroll with weeks as columns and days-of-week as rows.
 *
 * Layout: 53 columns (weeks) x 7 rows (Mon-Sun).
 * Each cell is a HeatmapCell component with color intensity 0-3.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HeatmapCalendarScreen(
    onBack: () -> Unit,
) {
    val heatmapData = remember { generateMockHeatmapData() }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Workout Heatmap") },
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
                .padding(horizontal = 16.dp)
                .verticalScroll(rememberScrollState()),
        ) {
            // Month labels
            MonthLabelsRow()

            Spacer(modifier = Modifier.height(4.dp))

            // Heatmap grid — 7 rows (days of week) x 53 columns (weeks)
            val dayLabels = listOf("Mon", "", "Wed", "", "Fri", "", "Sun")
            val startOfYear = Year.now().atDay(1)

            // Build weeks grid
            val weeks = buildHeatmapGrid(heatmapData, startOfYear)

            // Render each row (day of week)
            for (dayOfWeek in 0..6) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(3.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    // Day label
                    Text(
                        text = dayLabels[dayOfWeek],
                        style = MaterialTheme.typography.labelSmall,
                        color = TokenColors.TextSecondary,
                        modifier = Modifier.width(24.dp),
                    )
                    // Week cells
                    for (week in 0 until weeks.size) {
                        val intensity = if (week < weeks.size) {
                            weeks[week].getOrElse(dayOfWeek) { 0 }
                        } else {
                            0
                        }
                        HeatmapCell(intensity = intensity)
                    }
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Legend
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.Center,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Text("Less", style = MaterialTheme.typography.labelSmall, color = TokenColors.TextSecondary)
                Spacer(modifier = Modifier.width(8.dp))
                HeatmapCell(intensity = 0)
                Spacer(modifier = Modifier.width(4.dp))
                HeatmapCell(intensity = 1)
                Spacer(modifier = Modifier.width(4.dp))
                HeatmapCell(intensity = 2)
                Spacer(modifier = Modifier.width(4.dp))
                HeatmapCell(intensity = 3)
                Spacer(modifier = Modifier.width(8.dp))
                Text("More", style = MaterialTheme.typography.labelSmall, color = TokenColors.TextSecondary)
            }

            Spacer(modifier = Modifier.height(24.dp))

            // Stats summary
            val totalWorkouts = heatmapData.values.count { it > 0 }
            val prDays = heatmapData.values.count { it == 3 }
            Column(
                modifier = Modifier.fillMaxWidth(),
                horizontalAlignment = Alignment.CenterHorizontally,
            ) {
                Text(
                    text = "$totalWorkouts workout days this year",
                    style = MaterialTheme.typography.bodyMedium,
                    color = TokenColors.TextSecondary,
                )
                if (prDays > 0) {
                    Text(
                        text = "$prDays PR days",
                        style = MaterialTheme.typography.bodySmall,
                        color = TokenColors.AccentPrimary,
                        modifier = Modifier.padding(top = 4.dp),
                    )
                }
            }

            Spacer(modifier = Modifier.height(24.dp))
        }
    }
}

/**
 * Build the heatmap grid as a list of weeks, where each week is a map
 * of dayOfWeek (0=Mon, 6=Sun) to intensity (0-3).
 */
private fun buildHeatmapGrid(
    data: Map<LocalDate, Int>,
    startOfYear: LocalDate,
): List<Map<Int, Int>> {
    val weeks = mutableListOf<MutableMap<Int, Int>>()
    var currentWeek = mutableMapOf<Int, Int>()

    var current = startOfYear
    val today = LocalDate.now()

    while (!current.isAfter(today)) {
        val dayOfWeek = (current.dayOfWeek.value - 1) // 0=Mon, 6=Sun
        currentWeek[dayOfWeek] = data[current] ?: 0

        if (dayOfWeek == 6) {
            weeks.add(currentWeek)
            currentWeek = mutableMapOf()
        }
        current = current.plusDays(1)
    }

    // Add the last incomplete week
    if (currentWeek.isNotEmpty()) {
        weeks.add(currentWeek)
    }

    return weeks
}

/**
 * Month labels row aligned with the heatmap columns.
 */
@Composable
private fun MonthLabelsRow() {
    val months = listOf("Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(start = 27.dp), // offset for day label column
        horizontalArrangement = Arrangement.SpaceBetween,
    ) {
        months.forEach { month ->
            Text(
                text = month,
                style = MaterialTheme.typography.labelSmall,
                color = TokenColors.TextSecondary,
            )
        }
    }
}
