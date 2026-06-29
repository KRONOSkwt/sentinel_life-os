package com.sentinel.lifeos.ui.gimnasio.screens

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
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
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
 * Mock AI suggestions — will be replaced with API call to /gimnasio/ai-suggestions.
 */
private data class MockSuggestion(
    val exerciseName: String,
    val currentWeight: Double,
    val suggestedWeight: Double,
    val reason: String,
    val confidence: Double,
)

private val mockSuggestions = listOf(
    MockSuggestion("Bench Press", 80.0, 82.5, "Hit 8 reps on last 2 sessions. Ready for +2.5kg progression.", 0.85),
    MockSuggestion("Squat", 100.0, 100.0, "Maintain current weight. Average RPE was 8.5 — continue building consistency.", 0.70),
    MockSuggestion("Overhead Press", 40.0, 37.5, "Average RPE 9.2 over last 3 sessions. Recommend deload -2.5kg to recover.", 0.90),
    MockSuggestion("Barbell Row", 70.0, 72.5, "Consistent 10 reps at RPE 7. Progressive overload recommended.", 0.80),
)

/**
 * AI Coach suggestion screen.
 * Shows progressive overload suggestions for recently trained exercises.
 * Each suggestion card displays current weight, suggested weight, reason, and confidence.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AISuggestionScreen(
    onBack: () -> Unit,
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("AI Coach") },
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
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(horizontal = 16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            item { Spacer(modifier = Modifier.height(8.dp)) }

            item {
                Text(
                    text = "Based on your recent sessions",
                    style = MaterialTheme.typography.bodyMedium,
                    color = TokenColors.TextSecondary,
                )
            }

            items(mockSuggestions) { suggestion ->
                SuggestionCard(suggestion)
            }

            item { Spacer(modifier = Modifier.height(24.dp)) }
        }
    }
}

@Composable
private fun SuggestionCard(suggestion: MockSuggestion) {
    val isIncrease = suggestion.suggestedWeight > suggestion.currentWeight
    val isDecrease = suggestion.suggestedWeight < suggestion.currentWeight
    val actionText = when {
        isIncrease -> "+${suggestion.suggestedWeight - suggestion.currentWeight} kg"
        isDecrease -> "${suggestion.suggestedWeight - suggestion.currentWeight} kg"
        else -> "Maintain"
    }
    val actionColor = when {
        isIncrease -> TokenColors.AccentPrimary
        isDecrease -> TokenColors.AccentSecondary
        else -> TokenColors.TextSecondary
    }

    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = TokenColors.GlassCardBackground,
        ),
        shape = MaterialTheme.shapes.medium,
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            // Exercise name and action
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Text(
                    text = suggestion.exerciseName,
                    style = MaterialTheme.typography.bodyLarge,
                    fontWeight = FontWeight.SemiBold,
                    color = TokenColors.TextPrimary,
                )
                Text(
                    text = actionText,
                    style = MaterialTheme.typography.bodyMedium,
                    fontWeight = FontWeight.Bold,
                    color = actionColor,
                )
            }

            // Weight details
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 8.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp),
            ) {
                Text(
                    text = "Current: ${suggestion.currentWeight.toInt()} kg",
                    style = MaterialTheme.typography.bodySmall,
                    color = TokenColors.TextSecondary,
                )
                Text(
                    text = "Suggested: ${suggestion.suggestedWeight.toInt()} kg",
                    style = MaterialTheme.typography.bodySmall,
                    color = TokenColors.TextSecondary,
                )
            }

            // Reason
            Text(
                text = suggestion.reason,
                style = MaterialTheme.typography.bodySmall,
                color = TokenColors.TextSecondary,
                modifier = Modifier.padding(top = 12.dp),
            )

            // Confidence bar
            Column(modifier = Modifier.padding(top = 12.dp)) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                ) {
                    Text(
                        text = "Confidence",
                        style = MaterialTheme.typography.labelSmall,
                        color = TokenColors.TextSecondary,
                    )
                    Text(
                        text = "${(suggestion.confidence * 100).toInt()}%",
                        style = MaterialTheme.typography.labelSmall,
                        color = TokenColors.AccentPrimary,
                    )
                }
                LinearProgressIndicator(
                    progress = { suggestion.confidence.toFloat() },
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(top = 4.dp),
                    color = TokenColors.AccentPrimary,
                    trackColor = TokenColors.GlassBorder,
                )
            }
        }
    }
}
