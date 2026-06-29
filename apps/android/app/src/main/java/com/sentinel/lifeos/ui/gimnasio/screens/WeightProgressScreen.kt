package com.sentinel.lifeos.ui.gimnasio.screens

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.FilterChipDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Path
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.sentinel.lifeos.ui.theme.TokenColors

/**
 * Mock weight chart data — will be replaced with API call to /gimnasio/weight-chart/{exerciseId}.
 */
private data class WeightPoint(val date: String, val weight: Double)

private val ranges = listOf(30, 90, 365)

private fun mockWeightData(range: Int): List<WeightPoint> {
    val base = when (range) {
        30 -> listOf(75.0, 75.0, 77.5, 77.5, 80.0, 80.0, 80.0, 82.5, 82.5, 82.5)
        90 -> listOf(70.0, 72.5, 75.0, 75.0, 77.5, 80.0, 80.0, 82.5, 82.5)
        else -> listOf(60.0, 65.0, 70.0, 72.5, 75.0, 77.5, 80.0, 82.5)
    }
    return base.mapIndexed { i, w -> WeightPoint("Day $i", w) }
}

/**
 * Weight progress screen with a simple line chart drawn via Canvas.
 * Displays weight progression for a specific exercise over selectable time ranges.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun WeightProgressScreen(
    exerciseId: Int,
    onBack: () -> Unit,
) {
    var selectedRange by remember { mutableIntStateOf(90) }
    val data = remember(selectedRange) { mockWeightData(selectedRange) }
    val exerciseName = "Bench Press" // TODO: fetch from API

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(exerciseName) },
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
            // Range selector
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                ranges.forEach { range ->
                    FilterChip(
                        selected = selectedRange == range,
                        onClick = { selectedRange = range },
                        label = { Text("${range}d") },
                        colors = FilterChipDefaults.filterChipColors(
                            selectedContainerColor = TokenColors.AccentPrimary,
                            selectedLabelColor = TokenColors.TextPrimary,
                            containerColor = TokenColors.GlassCardBackground,
                            labelColor = TokenColors.TextSecondary,
                        ),
                    )
                }
            }

            Spacer(modifier = Modifier.height(24.dp))

            // Weight chart (Canvas)
            if (data.isNotEmpty()) {
                val minWeight = data.minOf { it.weight } - 5.0
                val maxWeight = data.maxOf { it.weight } + 5.0

                Canvas(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(200.dp),
                ) {
                    val width = size.width
                    val height = size.height
                    val stepX = width / (data.size - 1).coerceAtLeast(1)

                    // Draw grid lines
                    for (i in 0..4) {
                        val y = height * i / 4
                        drawLine(
                            color = TokenColors.GlassBorder,
                            start = Offset(0f, y),
                            end = Offset(width, y),
                            strokeWidth = 1f,
                        )
                    }

                    // Draw line chart
                    val path = Path()
                    data.forEachIndexed { index, point ->
                        val x = index * stepX
                        val normalizedWeight = (point.weight - minWeight) / (maxWeight - minWeight)
                        val y = height - (normalizedWeight * height).toFloat()

                        if (index == 0) {
                            path.moveTo(x, y)
                        } else {
                            path.lineTo(x, y)
                        }
                    }

                    drawPath(
                        path = path,
                        color = TokenColors.AccentPrimary,
                        style = Stroke(width = 3f),
                    )

                    // Draw data points
                    data.forEachIndexed { index, point ->
                        val x = index * stepX
                        val normalizedWeight = (point.weight - minWeight) / (maxWeight - minWeight)
                        val y = height - (normalizedWeight * height).toFloat()

                        drawCircle(
                            color = TokenColors.AccentPrimary,
                            radius = 5f,
                            center = Offset(x, y),
                        )
                    }
                }

                // Y-axis labels
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 8.dp),
                    horizontalArrangement = Arrangement.SpaceBetween,
                ) {
                    Text(
                        text = "${maxWeight.toInt()} kg",
                        style = MaterialTheme.typography.labelSmall,
                        color = TokenColors.TextSecondary,
                    )
                    Text(
                        text = "${minWeight.toInt()} kg",
                        style = MaterialTheme.typography.labelSmall,
                        color = TokenColors.TextSecondary,
                    )
                }
            }

            Spacer(modifier = Modifier.height(24.dp))

            // Stats
            if (data.isNotEmpty()) {
                val latest = data.last().weight
                val first = data.first().weight
                val change = latest - first
                val changeText = if (change >= 0) "+${change.toInt()}" else "${change.toInt()}"

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceEvenly,
                ) {
                    Column {
                        Text(
                            text = "Latest",
                            style = MaterialTheme.typography.labelSmall,
                            color = TokenColors.TextSecondary,
                        )
                        Text(
                            text = "${latest.toInt()} kg",
                            style = MaterialTheme.typography.bodyLarge,
                            fontWeight = FontWeight.Bold,
                            color = TokenColors.TextPrimary,
                        )
                    }
                    Column {
                        Text(
                            text = "Change",
                            style = MaterialTheme.typography.labelSmall,
                            color = TokenColors.TextSecondary,
                        )
                        Text(
                            text = "$changeText kg",
                            style = MaterialTheme.typography.bodyLarge,
                            fontWeight = FontWeight.Bold,
                            color = if (change >= 0) TokenColors.AccentPrimary else TokenColors.AccentSecondary,
                        )
                    }
                }
            }
        }
    }
}
