package com.sentinel.lifeos.ui.deportes.screens

import androidx.compose.foundation.clickable
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
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FloatingActionButton
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
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
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.sentinel.lifeos.ui.deportes.deportesRepository
import com.sentinel.lifeos.ui.theme.TokenColors
import kotlinx.coroutines.launch
import java.time.Instant
import java.time.ZoneId
import java.time.format.DateTimeFormatter
import java.time.temporal.ChronoUnit

/**
 * Screen displaying the list of training plans.
 * Plan name, dates, week count. FAB to add plan.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun TrainingPlanListScreen() {
    val scope = rememberCoroutineScope()
    var plans by remember { mutableStateOf(emptyList<com.sentinel.shared.models.TrainingPlanResponse>()) }
    var loaded by remember { mutableStateOf(false) }

    if (!loaded) {
        loaded = true
        scope.launch {
            plans = deportesRepository.listPlans()
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Training Plans") },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = TokenColors.SurfaceBackground,
                    titleContentColor = TokenColors.TextPrimary,
                ),
            )
        },
        floatingActionButton = {
            FloatingActionButton(
                onClick = { /* TODO: open create plan dialog */ },
                containerColor = TokenColors.AccentPrimary,
            ) {
                Icon(Icons.Default.Add, contentDescription = "Create plan")
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
            items(plans) { plan ->
                val weeks = ChronoUnit.WEEKS.between(plan.start_date, plan.end_date).toInt().coerceAtLeast(1)
                val daysUntilStart = ChronoUnit.DAYS.between(Instant.now(), plan.start_date).toInt()
                val isActive = daysUntilStart <= 0 && !plan.end_date.isBefore(Instant.now())

                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clickable { /* TODO: navigate to plan detail */ },
                    colors = CardDefaults.cardColors(
                        containerColor = TokenColors.GlassCardBackground,
                    ),
                    shape = MaterialTheme.shapes.medium,
                ) {
                    Column(modifier = Modifier.padding(16.dp)) {
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically,
                        ) {
                            Text(
                                text = plan.name,
                                style = MaterialTheme.typography.titleMedium,
                                fontWeight = FontWeight.SemiBold,
                                color = TokenColors.TextPrimary,
                            )
                            if (isActive) {
                                Text(
                                    text = "Active",
                                    style = MaterialTheme.typography.labelSmall,
                                    color = TokenColors.AccentPrimary,
                                )
                            }
                        }
                        plan.description?.let {
                            Text(
                                text = it,
                                style = MaterialTheme.typography.bodySmall,
                                color = TokenColors.TextSecondary,
                                modifier = Modifier.padding(top = 4.dp),
                            )
                        }
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(top = 8.dp),
                            horizontalArrangement = Arrangement.spacedBy(16.dp),
                        ) {
                            Text(
                                text = "${weeks} weeks",
                                style = MaterialTheme.typography.labelSmall,
                                color = TokenColors.AccentSecondary,
                            )
                            Text(
                                text = "${formatDate(plan.start_date)} – ${formatDate(plan.end_date)}",
                                style = MaterialTheme.typography.labelSmall,
                                color = TokenColors.TextSecondary,
                            )
                        }
                    }
                }
            }
        }
    }
}

private fun formatDate(instant: Instant): String {
    val formatter = DateTimeFormatter.ofPattern("MMM d")
        .withZone(ZoneId.systemDefault())
    return formatter.format(instant)
}
