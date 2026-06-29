package com.sentinel.lifeos.ui.deportes.screens

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
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.FilterList
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.sentinel.lifeos.ui.deportes.deportesRepository
import com.sentinel.lifeos.ui.deportes.components.ActivityCard
import com.sentinel.lifeos.ui.theme.TokenColors
import kotlinx.coroutines.launch

/**
 * Screen displaying the list of sport activities.
 * Filter by date range, FAB to add activity, click to navigate to detail.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ActivityListScreen(
    onActivityClick: (Int) -> Unit,
) {
    val scope = rememberCoroutineScope()
    var activities by remember { mutableStateOf(emptyList<com.sentinel.shared.models.SportActivityResponse>()) }
    var sportsMap by remember { mutableStateOf<Map<Int, Pair<String, String?>>>(emptyMap()) }
    var loaded by remember { mutableStateOf(false) }

    // Load data
    if (!loaded) {
        loaded = true
        scope.launch {
            activities = deportesRepository.listActivities()
            val sports = deportesRepository.listSports()
            sportsMap = sports.associate { it.id to (it.name to it.icon) }
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Activities") },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = TokenColors.SurfaceBackground,
                    titleContentColor = TokenColors.TextPrimary,
                ),
                actions = {
                    IconButton(onClick = { /* TODO: open date filter dialog */ }) {
                        Icon(
                            Icons.Default.FilterList,
                            contentDescription = "Filter",
                            tint = TokenColors.TextSecondary,
                        )
                    }
                },
            )
        },
        floatingActionButton = {
            FloatingActionButton(
                onClick = { /* TODO: open create activity dialog */ },
                containerColor = TokenColors.AccentPrimary,
            ) {
                Icon(Icons.Default.Add, contentDescription = "Log activity")
            }
        },
        containerColor = TokenColors.SurfaceBackground,
    ) { padding ->
        if (activities.isEmpty()) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding),
            ) {
                // Empty state — no content needed
            }
        } else {
            LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding)
                    .padding(horizontal = 16.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                item { Spacer(modifier = Modifier.height(8.dp)) }
                items(activities) { activity ->
                    val sport = sportsMap[activity.sport_id]
                    ActivityCard(
                        activity = activity,
                        sportName = sport?.first ?: "Sport #${activity.sport_id}",
                        sportIcon = sport?.second,
                        onClick = { onActivityClick(activity.id) },
                    )
                }
            }
        }
    }
}
