package com.sentinel.lifeos.ui.gimnasio.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import com.sentinel.lifeos.ui.theme.TokenColors

/**
 * A single cell in the heatmap calendar grid.
 * Color intensity maps to workout count for that day.
 *
 * Intensity levels:
 *   0 = no workouts (transparent)
 *   1 = 1 workout (light green)
 *   2 = 2 workouts (medium green)
 *   3 = 3+ workouts (bright green)
 */
@Composable
fun HeatmapCell(
    intensity: Int,
    modifier: Modifier = Modifier,
) {
    val color = when (intensity) {
        0 -> TokenColors.GlassBorder
        1 -> Color(0xFF1B4332)
        2 -> Color(0xFF2D6A4F)
        3 -> Color(0xFF52B788)
        else -> Color(0xFF52B788)
    }

    Box(
        modifier = modifier
            .size(14.dp)
            .clip(RoundedCornerShape(2.dp))
            .background(color),
    )
}
