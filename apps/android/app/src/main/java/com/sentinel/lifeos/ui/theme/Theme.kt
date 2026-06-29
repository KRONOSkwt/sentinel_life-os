package com.sentinel.lifeos.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp

// Generated from design tokens — DO NOT EDIT
object TokenColors {
    val GlassBackground = Color(0x14ffffff)
    val GlassCardBackground = Color(0x1effffff)
    val GlassBorder = Color(0x26ffffff)
    val AccentPrimary = Color(0xFF6366f1)
    val AccentSecondary = Color(0xFF8b5cf6)
    val SurfaceBackground = Color(0xFF0f0f23)
    val SurfaceCard = Color(0xFF1a1a2e)
    val TextPrimary = Color(0xFFe2e8f0)
    val TextSecondary = Color(0xFF94a3b8)
}

object TokenSpacing {
    val Xs = 4.dp
    val Sm = 8.dp
    val Md = 16.dp
    val Lg = 24.dp
    val Xl = 32.dp
}

object TokenRadius {
    val Sm = 8.dp
    val Md = 12.dp
    val Lg = 16.dp
    val Xl = 24.dp
}

// ---------------------------------------------------------------------------
// Material3 dark color scheme wired to design tokens
// ---------------------------------------------------------------------------

private val SentinelColorScheme = darkColorScheme(
    primary = TokenColors.AccentPrimary,
    secondary = TokenColors.AccentSecondary,
    background = TokenColors.SurfaceBackground,
    surface = TokenColors.SurfaceCard,
    onPrimary = Color.White,
    onSecondary = Color.White,
    onBackground = TokenColors.TextPrimary,
    onSurface = TokenColors.TextPrimary,
)

@Composable
fun SentinelLifeOsTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = SentinelColorScheme,
        typography = Typography,
        content = content,
    )
}
