package com.example.ui

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.FitnessCenter
import androidx.compose.material.icons.filled.History
import androidx.compose.material.icons.filled.Home
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.NavigationBarItemDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import com.example.ui.home.HomeScreen
import com.example.ui.workout.WorkoutScreen
import com.example.ui.history.HistoryScreen
import com.example.ui.theme.ElectricViolet

@Composable
fun AuroraFitApp(viewModel: MainViewModel) {
    val navController = rememberNavController()
    val navBackStackEntry by navController.currentBackStackEntryAsState()
    val currentRoute = navBackStackEntry?.destination?.route
    val isDark = isSystemInDarkTheme()

    val navContainerColor = if (isDark) Color(0xF00F172A) else Color(0xF5FFFFFF)
    val navBorderColor = if (isDark) Color.White.copy(alpha = 0.1f) else Color(0xFFCBD5E1).copy(alpha = 0.5f)

    Scaffold(
        containerColor = MaterialTheme.colorScheme.background,
        bottomBar = {
            NavigationBar(
                modifier = Modifier.height(80.dp),
                containerColor = if (isDark) Color(0xF20F172A) else Color(0xF8FFFFFF),
                contentColor = MaterialTheme.colorScheme.primary,
                tonalElevation = 0.dp
            ) {
                val itemColors = NavigationBarItemDefaults.colors(
                    selectedIconColor = ElectricViolet,
                    selectedTextColor = ElectricViolet,
                    indicatorColor = ElectricViolet.copy(alpha = 0.15f),
                    unselectedIconColor = if (isDark) Color(0xFF64748B) else Color(0xFF94A3B8),
                    unselectedTextColor = if (isDark) Color(0xFF64748B) else Color(0xFF94A3B8)
                )

                NavigationBarItem(
                    selected = currentRoute == "home",
                    colors = itemColors,
                    onClick = {
                        navController.navigate("home") {
                            popUpTo(navController.graph.findStartDestination().id) { saveState = true }
                            launchSingleTop = true
                            restoreState = true
                        }
                    },
                    icon = { Icon(Icons.Default.Home, contentDescription = "Home") },
                    label = { Text("Home", fontWeight = if (currentRoute == "home") FontWeight.Bold else FontWeight.Medium) }
                )
                NavigationBarItem(
                    selected = currentRoute == "workout",
                    colors = itemColors,
                    onClick = {
                        navController.navigate("workout") {
                            popUpTo(navController.graph.findStartDestination().id) { saveState = true }
                            launchSingleTop = true
                            restoreState = true
                        }
                    },
                    icon = { Icon(Icons.Default.FitnessCenter, contentDescription = "Workout") },
                    label = { Text("Workout", fontWeight = if (currentRoute == "workout") FontWeight.Bold else FontWeight.Medium) }
                )
                NavigationBarItem(
                    selected = currentRoute == "history",
                    colors = itemColors,
                    onClick = {
                        navController.navigate("history") {
                            popUpTo(navController.graph.findStartDestination().id) { saveState = true }
                            launchSingleTop = true
                            restoreState = true
                        }
                    },
                    icon = { Icon(Icons.Default.History, contentDescription = "History") },
                    label = { Text("History", fontWeight = if (currentRoute == "history") FontWeight.Bold else FontWeight.Medium) }
                )
            }
        }
    ) { innerPadding ->
        NavHost(
            navController = navController,
            startDestination = "home",
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .background(MaterialTheme.colorScheme.background)
        ) {
            composable("home") { HomeScreen(viewModel, navController) }
            composable("workout") { WorkoutScreen(viewModel, navController) }
            composable("history") { HistoryScreen(viewModel) }
        }
    }
}
