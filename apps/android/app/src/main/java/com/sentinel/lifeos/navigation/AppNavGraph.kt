package com.sentinel.lifeos.navigation

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.sentinel.lifeos.ui.gimnasio.GimnasioScreen

/** Route constants — mirrors Angular routes for consistency. */
object Routes {
    const val HOME = "home"
    const val GIMNASIO = "gimnasio"
    const val DEPORTES = "deportes"
    const val LESIONES = "lesiones"
    const val PASTORAL = "pastoral"
    const val FILOSOFIA = "filosofia"
    const val CIBERSEGURIDAD = "ciberseguridad"
}

// ---------------------------------------------------------------------------
// Placeholder screens — real implementations will replace these.
// ---------------------------------------------------------------------------

@Composable
fun HomeScreen() = ModulePlaceholder("Home")

@Composable
fun DeportesScreen() = ModulePlaceholder("Deportes")

@Composable
fun LesionesScreen() = ModulePlaceholder("Lesiones")

@Composable
fun PastoralScreen() = ModulePlaceholder("Pastoral")

@Composable
fun FilosofiaScreen() = ModulePlaceholder("Filosofia")

@Composable
fun CiberseguridadScreen() = ModulePlaceholder("Ciberseguridad")

@Composable
private fun ModulePlaceholder(name: String) {
    Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
        Text(text = name)
    }
}

// ---------------------------------------------------------------------------
// Navigation graph
// ---------------------------------------------------------------------------

@Composable
fun AppNavGraph(navController: NavHostController) {
    NavHost(
        navController = navController,
        startDestination = Routes.HOME,
    ) {
        composable(Routes.HOME) { HomeScreen() }
        composable(Routes.GIMNASIO) { GimnasioScreen() }
        composable(Routes.DEPORTES) { DeportesScreen() }
        composable(Routes.LESIONES) { LesionesScreen() }
        composable(Routes.PASTORAL) { PastoralScreen() }
        composable(Routes.FILOSOFIA) { FilosofiaScreen() }
        composable(Routes.CIBERSEGURIDAD) { CiberseguridadScreen() }
    }
}
