package com.sentinel.lifeos.ui.deportes

import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.DateRange
import androidx.compose.material.icons.filled.DirectionsRun
import androidx.compose.material.icons.filled.Leaderboard
import androidx.compose.material.icons.filled.ViewList
import androidx.compose.material3.Icon
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.NavigationBarItemDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.navigation.NavDestination.Companion.hierarchy
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.sentinel.lifeos.data.MockDeportesRepository
import com.sentinel.lifeos.ui.deportes.screens.ActivityDetailScreen
import com.sentinel.lifeos.ui.deportes.screens.ActivityListScreen
import com.sentinel.lifeos.ui.deportes.screens.RaceCalendarScreen
import com.sentinel.lifeos.ui.deportes.screens.SportStatsScreen
import com.sentinel.lifeos.ui.deportes.screens.TrainingPlanListScreen
import com.sentinel.lifeos.ui.theme.TokenColors

/**
 * Bottom navigation tabs for the Deportes module.
 */
private sealed class DeportesTab(
    val route: String,
    val label: String,
    val icon: ImageVector,
) {
    data object Activities : DeportesTab("deportes_activities", "Activities", Icons.Default.DirectionsRun)
    data object Plans : DeportesTab("deportes_plans", "Plans", Icons.Default.ViewList)
    data object Calendar : DeportesTab("deportes_calendar", "Calendar", Icons.Default.DateRange)
    data object Stats : DeportesTab("deportes_stats", "Records", Icons.Default.Leaderboard)
}

private val deportesTabs = listOf(
    DeportesTab.Activities,
    DeportesTab.Plans,
    DeportesTab.Calendar,
    DeportesTab.Stats,
)

/** Shared repository instance for mock data. */
internal val deportesRepository = MockDeportesRepository()

/**
 * Deportes module root screen — Scaffold with bottom navigation shell.
 * Each tab hosts its own nested NavHost destinations.
 */
@Composable
fun DeportesScreen() {
    val navController = rememberNavController()
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentDestination = navBackStackEntry?.destination

    val showBottomBar = currentDestination?.route in deportesTabs.map { it.route }

    Scaffold(
        bottomBar = {
            if (showBottomBar) {
                NavigationBar(
                    containerColor = TokenColors.SurfaceCard,
                ) {
                    deportesTabs.forEach { tab ->
                        NavigationBarItem(
                            icon = { Icon(tab.icon, contentDescription = tab.label) },
                            label = { Text(tab.label) },
                            selected = currentDestination?.hierarchy?.any { it.route == tab.route } == true,
                            onClick = {
                                navController.navigate(tab.route) {
                                    popUpTo(navController.graph.findStartDestination().id) {
                                        saveState = true
                                    }
                                    launchSingleTop = true
                                    restoreState = true
                                }
                            },
                            colors = NavigationBarItemDefaults.colors(
                                selectedIconColor = TokenColors.AccentPrimary,
                                selectedTextColor = TokenColors.AccentPrimary,
                                unselectedIconColor = TokenColors.TextSecondary,
                                unselectedTextColor = TokenColors.TextSecondary,
                                indicatorColor = TokenColors.GlassCardBackground,
                            ),
                        )
                    }
                }
            }
        },
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = DeportesTab.Activities.route,
            modifier = Modifier.padding(innerPadding),
        ) {
            // Tab destinations
            composable(DeportesTab.Activities.route) {
                ActivityListScreen(
                    onActivityClick = { activityId ->
                        navController.navigate("deportes_activity_detail/$activityId")
                    },
                )
            }
            composable(DeportesTab.Plans.route) {
                TrainingPlanListScreen()
            }
            composable(DeportesTab.Calendar.route) {
                RaceCalendarScreen()
            }
            composable(DeportesTab.Stats.route) {
                SportStatsScreen()
            }

            // Detail screens
            composable(
                route = "deportes_activity_detail/{activityId}",
                arguments = listOf(navArgument("activityId") { type = NavType.IntType }),
            ) { backStackEntry ->
                val activityId = backStackEntry.arguments?.getInt("activityId") ?: return@composable
                ActivityDetailScreen(
                    activityId = activityId,
                    onBack = { navController.popBackStack() },
                )
            }
        }
    }
}
