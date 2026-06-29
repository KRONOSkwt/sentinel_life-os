package com.sentinel.lifeos.ui.gimnasio

import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.FitnessCenter
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.LocalFireDepartment
import androidx.compose.material.icons.filled.ShowChart
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
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
import com.sentinel.lifeos.ui.gimnasio.screens.AISuggestionScreen
import com.sentinel.lifeos.ui.gimnasio.screens.GamificationScreen
import com.sentinel.lifeos.ui.gimnasio.screens.HeatmapCalendarScreen
import com.sentinel.lifeos.ui.gimnasio.screens.RoutineDetailScreen
import com.sentinel.lifeos.ui.gimnasio.screens.RoutineListScreen
import com.sentinel.lifeos.ui.gimnasio.screens.WeightProgressScreen
import com.sentinel.lifeos.ui.gimnasio.screens.WorkoutHistoryScreen
import com.sentinel.lifeos.ui.gimnasio.screens.WorkoutSessionScreen
import com.sentinel.lifeos.ui.theme.TokenColors

/**
 * Bottom navigation tabs for the Gimnasio module.
 */
private sealed class GimnasioTab(
    val route: String,
    val label: String,
    val icon: ImageVector,
) {
    data object Routines : GimnasioTab("gimnasio_routines", "Routines", Icons.Default.FitnessCenter)
    data object Session : GimnasioTab("gimnasio_session", "Session", Icons.Default.Home)
    data object History : GimnasioTab("gimnasio_history", "History", Icons.Default.ShowChart)
    data object Stats : GimnasioTab("gimnasio_stats", "Stats", Icons.Default.LocalFireDepartment)
}

private val gimnasioTabs = listOf(
    GimnasioTab.Routines,
    GimnasioTab.Session,
    GimnasioTab.History,
    GimnasioTab.Stats,
)

/**
 * Gimnasio module root screen — Scaffold with bottom navigation shell.
 * Each tab hosts its own nested NavHost destinations.
 */
@Composable
fun GimnasioScreen() {
    val navController = rememberNavController()
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentDestination = navBackStackEntry?.destination

    // Only show bottom bar on tab-level destinations
    val showBottomBar = currentDestination?.route in gimnasioTabs.map { it.route }

    Scaffold(
        bottomBar = {
            if (showBottomBar) {
                NavigationBar(
                    containerColor = TokenColors.SurfaceCard,
                ) {
                    gimnasioTabs.forEach { tab ->
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
            startDestination = GimnasioTab.Routines.route,
            modifier = Modifier.padding(innerPadding),
        ) {
            // Tab destinations
            composable(GimnasioTab.Routines.route) {
                RoutineListScreen(
                    onRoutineClick = { routineId ->
                        navController.navigate("gimnasio_routine_detail/$routineId")
                    },
                )
            }
            composable(GimnasioTab.Session.route) {
                WorkoutSessionScreen()
            }
            composable(GimnasioTab.History.route) {
                WorkoutHistoryScreen(
                    onSessionClick = { /* TODO: navigate to session detail */ },
                )
            }
            composable(GimnasioTab.Stats.route) {
                GamificationScreen()
            }

            // Detail / sub-screens
            composable(
                route = "gimnasio_routine_detail/{routineId}",
                arguments = listOf(navArgument("routineId") { type = NavType.IntType }),
            ) { backStackEntry ->
                val routineId = backStackEntry.arguments?.getInt("routineId") ?: return@composable
                RoutineDetailScreen(
                    routineId = routineId,
                    onBack = { navController.popBackStack() },
                    onStartWorkout = { rid ->
                        navController.navigate(GimnasioTab.Session.route)
                    },
                )
            }
            composable("gimnasio_exercises") {
                com.sentinel.lifeos.ui.gimnasio.screens.ExerciseCatalogScreen(
                    onBack = { navController.popBackStack() },
                )
            }
            composable("gimnasio_heatmap") {
                HeatmapCalendarScreen(
                    onBack = { navController.popBackStack() },
                )
            }
            composable("gimnasio_ai_coach") {
                AISuggestionScreen(
                    onBack = { navController.popBackStack() },
                )
            }
            composable(
                route = "gimnasio_weight/{exerciseId}",
                arguments = listOf(navArgument("exerciseId") { type = NavType.IntType }),
            ) { backStackEntry ->
                val exerciseId = backStackEntry.arguments?.getInt("exerciseId") ?: return@composable
                WeightProgressScreen(
                    exerciseId = exerciseId,
                    onBack = { navController.popBackStack() },
                )
            }
        }
    }
}
