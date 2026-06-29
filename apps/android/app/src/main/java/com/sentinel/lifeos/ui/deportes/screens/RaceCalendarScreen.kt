package com.sentinel.lifeos.ui.deportes.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
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
import androidx.compose.ui.unit.dp
import com.sentinel.lifeos.ui.deportes.deportesRepository
import com.sentinel.lifeos.ui.deportes.components.RaceCard
import com.sentinel.lifeos.ui.theme.TokenColors
import kotlinx.coroutines.launch

/**
 * Race calendar screen — upcoming races first with days countdown.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun RaceCalendarScreen() {
    val scope = rememberCoroutineScope()
    var races by remember { mutableStateOf(emptyList<com.sentinel.shared.models.RaceEventResponse>()) }
    var sportsMap by remember { mutableStateOf<Map<Int, String>>(emptyMap()) }
    var loaded by remember { mutableStateOf(false) }

    if (!loaded) {
        loaded = true
        scope.launch {
            races = deportesRepository.listRaces(upcomingOnly = false)
            val sports = deportesRepository.listSports()
            sportsMap = sports.associate { it.id to it.name }
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Race Calendar") },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = TokenColors.SurfaceBackground,
                    titleContentColor = TokenColors.TextPrimary,
                ),
            )
        },
        floatingActionButton = {
            FloatingActionButton(
                onClick = { /* TODO: open create race dialog */ },
                containerColor = TokenColors.AccentPrimary,
            ) {
                Icon(Icons.Default.Add, contentDescription = "Add race")
            }
        },
        containerColor = TokenColors.SurfaceBackground,
    ) { padding ->
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(horizontal = 16.dp),
            verticalArrangement = Arrangement.spacedBy(8.dp),
        ) {
            item { Spacer(modifier = Modifier.height(8.dp)) }
            items(races) { race ->
                RaceCard(
                    race = race,
                    sportName = sportsMap[race.sport_id] ?: "Sport #${race.sport_id}",
                    onClick = { /* TODO: navigate to race detail */ },
                )
            }
        }
    }
}
