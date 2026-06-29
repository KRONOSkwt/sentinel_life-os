package com.sentinel.lifeos.ui.gimnasio.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
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
import androidx.compose.ui.unit.sp
import com.sentinel.lifeos.ui.gimnasio.components.AchievementBadge
import com.sentinel.lifeos.ui.gimnasio.components.StatCard
import com.sentinel.lifeos.ui.theme.TokenColors

/**
 * Mock gamification data — will be replaced with API call.
 */
private data class MockAchievement(
    val key: String,
    val name: String,
    val description: String,
    val isUnlocked: Boolean,
)

private val mockStats = Triple(2450, 12, 21) // points, streak, longest streak
private val mockLevel = 5

private val mockAchievements = listOf(
    MockAchievement("first_workout", "First Workout", "Complete your first session", true),
    MockAchievement("iron_will", "Iron Will", "7-day streak", true),
    MockAchievement("century_club", "Century Club", "100 sessions logged", false),
    MockAchievement("pr_master", "PR Master", "50 personal records", false),
    MockAchievement("weight_warrior", "Weight Warrior", "10 exercises in 7 days", false),
    MockAchievement("dedication", "Dedication", "30-day streak", false),
    MockAchievement("centurion", "Centurion", "1000 total points", true),
    MockAchievement("iron_legend", "Iron Legend", "100-day streak", false),
    MockAchievement("perfect_week", "Perfect Week", "7 consecutive days", false),
    MockAchievement("level_10", "Level 10", "Reach level 10", false),
)

/**
 * Gamification dashboard screen.
 * Displays points, streak, level badge, and achievement grid.
 */
@OptIn(ExperimentalMaterial3Api::class, ExperimentalLayoutApi::class)
@Composable
fun GamificationScreen() {
    val (points, streak, longestStreak) = mockStats
    val level = mockLevel
    val pointsToNextLevel = (level * 500) - points

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Gamification") },
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
            // Level badge
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 24.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
            ) {
                Text(
                    text = "Level $level",
                    fontSize = 36.sp,
                    fontWeight = FontWeight.Bold,
                    color = TokenColors.AccentPrimary,
                )
                Text(
                    text = "$pointsToNextLevel pts to Level ${level + 1}",
                    style = MaterialTheme.typography.bodySmall,
                    color = TokenColors.TextSecondary,
                    modifier = Modifier.padding(top = 4.dp),
                )
            }

            // Stats row
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                StatCard(
                    label = "Points",
                    value = "$points",
                    modifier = Modifier.weight(1f),
                )
                StatCard(
                    label = "Streak",
                    value = "$streak",
                    modifier = Modifier.weight(1f),
                )
                StatCard(
                    label = "Best",
                    value = "$longestStreak",
                    modifier = Modifier.weight(1f),
                )
            }

            Spacer(modifier = Modifier.height(24.dp))

            // Achievements header
            Text(
                text = "Achievements",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.SemiBold,
                color = TokenColors.TextPrimary,
            )

            Spacer(modifier = Modifier.height(12.dp))

            // Achievement grid — responsive columns
            FlowRow(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                mockAchievements.forEach { achievement ->
                    AchievementBadge(
                        name = achievement.name,
                        description = achievement.description,
                        isUnlocked = achievement.isUnlocked,
                        modifier = Modifier
                            .fillMaxWidth()
                            .weight(1f)
                            .padding(0.dp),
                    )
                }
            }

            Spacer(modifier = Modifier.height(24.dp))
        }
    }
}
