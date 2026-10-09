package com.example.ui.home

import android.annotation.SuppressLint
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Bedtime
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.DarkMode
import androidx.compose.material.icons.filled.FitnessCenter
import androidx.compose.material.icons.filled.LightMode
import androidx.compose.material.icons.filled.LocalFireDepartment
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import androidx.navigation.NavGraph.Companion.findStartDestination
import com.example.Graph
import com.example.data.model.WorkoutWithExercises
import com.example.ui.MainViewModel
import com.example.ui.components.GlassCard
import com.example.ui.stats.StatsHelper
import com.example.ui.theme.CompletedBadgeGradient
import com.example.ui.theme.DarkMeshBackgroundGradient
import com.example.ui.theme.ElectricCyan
import com.example.ui.theme.ElectricViolet
import com.example.ui.theme.EmeraldGreen
import com.example.ui.theme.FlameOrange
import com.example.ui.theme.LightMeshBackgroundGradient
import java.util.*

@Composable
fun HomeScreen(viewModel: MainViewModel, navController: NavController) {
    val workouts by viewModel.allWorkouts.collectAsState()
    val completedWorkouts = workouts.filter { it.workout.isCompleted }
    val streak = StatsHelper.calculateStreak(completedWorkouts)
    val thisMonth = StatsHelper.workoutsThisMonth(completedWorkouts)

    val todayCalendar = Calendar.getInstance()
    val todayCompleted = completedWorkouts.firstOrNull {
        val c = Calendar.getInstance()
        c.timeInMillis = it.workout.dateMillis
        c.get(Calendar.YEAR) == todayCalendar.get(Calendar.YEAR) &&
                c.get(Calendar.DAY_OF_YEAR) == todayCalendar.get(Calendar.DAY_OF_YEAR)
    }

    val isDarkMode by viewModel.isDarkMode.collectAsState()
    val haptic = LocalHapticFeedback.current

    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background
    ) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(
                    brush = if (isDarkMode) DarkMeshBackgroundGradient else LightMeshBackgroundGradient
                )
        ) {
            LazyColumn(
                modifier = Modifier.fillMaxSize(),
                contentPadding = PaddingValues(start = 16.dp, end = 16.dp, top = 20.dp, bottom = 100.dp),
                verticalArrangement = Arrangement.spacedBy(20.dp)
            ) {
                // Header Row
                item {
                    Box(modifier = Modifier.fillMaxWidth()) {
                        Column {
                            Text(
                                "AURORA FIT",
                                style = MaterialTheme.typography.titleMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                letterSpacing = 2.sp,
                                fontWeight = FontWeight.Bold
                            )
                            Spacer(modifier = Modifier.height(2.dp))
                            Text(
                                "DASHBOARD",
                                style = MaterialTheme.typography.headlineLarge,
                                fontWeight = FontWeight.Light,
                                letterSpacing = 2.sp,
                                color = MaterialTheme.colorScheme.onBackground
                            )
                        }

                        IconButton(
                            onClick = {
                                haptic.performHapticFeedback(HapticFeedbackType.LongPress)
                                viewModel.toggleTheme()
                            },
                            modifier = Modifier.align(Alignment.TopEnd)
                        ) {
                            Icon(
                                imageVector = if (isDarkMode) Icons.Default.LightMode else Icons.Default.DarkMode,
                                contentDescription = "Toggle Theme",
                                tint = MaterialTheme.colorScheme.onBackground
                            )
                        }
                    }
                }

                // Top Metrics (Current Streak & This Month)
                item {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(14.dp)
                    ) {
                        HomeStatCard(
                            modifier = Modifier.weight(1f),
                            label = "CURRENT STREAK",
                            value = "$streak",
                            unit = "days",
                            icon = Icons.Default.LocalFireDepartment,
                            accentColor = FlameOrange
                        )

                        HomeStatCard(
                            modifier = Modifier.weight(1f),
                            label = "THIS MONTH",
                            value = "$thisMonth",
                            unit = "sessions",
                            icon = Icons.Default.Star,
                            accentColor = ElectricViolet
                        )
                    }
                }

                // Monthly Progress Calendar
                item {
                    MonthlyProgressCard(completedWorkouts = completedWorkouts)
                }

                // Today's Session Section
                item {
                    Column {
                        Text(
                            "TODAY'S SESSION",
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            letterSpacing = 1.5.sp,
                            fontWeight = FontWeight.Bold
                        )
                        Spacer(modifier = Modifier.height(10.dp))

                        if (todayCompleted != null) {
                            GlassCard {
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(20.dp),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Row(
                                        verticalAlignment = Alignment.CenterVertically,
                                        modifier = Modifier.weight(1f)
                                    ) {
                                        Box(
                                            modifier = Modifier
                                                .size(42.dp)
                                                .background(EmeraldGreen.copy(alpha = 0.15f), CircleShape),
                                            contentAlignment = Alignment.Center
                                        ) {
                                            Icon(
                                                Icons.Default.Check,
                                                contentDescription = null,
                                                tint = EmeraldGreen,
                                                modifier = Modifier.size(22.dp)
                                            )
                                        }
                                        Spacer(modifier = Modifier.width(14.dp))
                                        Column {
                                            Text(
                                                todayCompleted.workout.name.uppercase(),
                                                style = MaterialTheme.typography.titleMedium,
                                                fontWeight = FontWeight.Bold,
                                                color = MaterialTheme.colorScheme.onSurface
                                            )
                                            Spacer(modifier = Modifier.height(2.dp))
                                            Text(
                                                "Completed today",
                                                style = MaterialTheme.typography.bodySmall,
                                                color = EmeraldGreen,
                                                fontWeight = FontWeight.SemiBold
                                            )
                                        }
                                    }

                                    Surface(
                                        shape = RoundedCornerShape(12.dp),
                                        color = EmeraldGreen.copy(alpha = 0.15f)
                                    ) {
                                        Text(
                                            "Done",
                                            style = MaterialTheme.typography.labelSmall,
                                            fontWeight = FontWeight.Bold,
                                            color = EmeraldGreen,
                                            modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp)
                                        )
                                    }
                                }
                            }
                        } else {
                            GlassCard(
                                modifier = Modifier.clickable {
                                    navController.navigate("workout") {
                                        popUpTo(navController.graph.findStartDestination().id) {
                                            saveState = true
                                        }
                                        launchSingleTop = true
                                        restoreState = true
                                    }
                                }
                            ) {
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(20.dp),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Row(
                                        verticalAlignment = Alignment.CenterVertically,
                                        modifier = Modifier.weight(1f)
                                    ) {
                                        Box(
                                            modifier = Modifier
                                                .size(42.dp)
                                                .background(ElectricViolet.copy(alpha = 0.15f), CircleShape),
                                            contentAlignment = Alignment.Center
                                        ) {
                                            Icon(
                                                Icons.Default.FitnessCenter,
                                                contentDescription = null,
                                                tint = ElectricViolet,
                                                modifier = Modifier.size(22.dp)
                                            )
                                        }
                                        Spacer(modifier = Modifier.width(14.dp))
                                        Column {
                                            Text(
                                                "No workout yet",
                                                style = MaterialTheme.typography.titleMedium,
                                                fontWeight = FontWeight.Bold,
                                                color = MaterialTheme.colorScheme.onSurface
                                            )
                                            Spacer(modifier = Modifier.height(2.dp))
                                            Text(
                                                "Ready to train?",
                                                style = MaterialTheme.typography.bodySmall,
                                                color = MaterialTheme.colorScheme.onSurfaceVariant
                                            )
                                        }
                                    }

                                    Button(
                                        onClick = {
                                            navController.navigate("workout") {
                                                popUpTo(navController.graph.findStartDestination().id) {
                                                    saveState = true
                                                }
                                                launchSingleTop = true
                                                restoreState = true
                                            }
                                        },
                                        shape = RoundedCornerShape(16.dp),
                                        colors = ButtonDefaults.buttonColors(
                                            containerColor = ElectricViolet,
                                            contentColor = Color.White
                                        ),
                                        contentPadding = PaddingValues(horizontal = 16.dp, vertical = 10.dp)
                                    ) {
                                        Icon(Icons.Default.PlayArrow, contentDescription = null, modifier = Modifier.size(18.dp))
                                        Spacer(Modifier.width(4.dp))
                                        Text("START", fontWeight = FontWeight.Bold, letterSpacing = 1.sp)
                                    }
                                }
                            }
                        }
                    }
                }

                // Last Workout Section
                item {
                    val lastWorkout = completedWorkouts.firstOrNull { w -> todayCompleted == null || w.workout.id != todayCompleted.workout.id }
                    if (lastWorkout != null) {
                        Column {
                            Text(
                                "LAST WORKOUT",
                                style = MaterialTheme.typography.labelMedium,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                letterSpacing = 1.5.sp,
                                fontWeight = FontWeight.Bold
                            )
                            Spacer(modifier = Modifier.height(10.dp))

                            GlassCard {
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(20.dp),
                                    horizontalArrangement = Arrangement.SpaceBetween,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Column(modifier = Modifier.weight(1f)) {
                                        Text(
                                            lastWorkout.workout.name.uppercase(),
                                            style = MaterialTheme.typography.titleMedium,
                                            fontWeight = FontWeight.Bold,
                                            color = MaterialTheme.colorScheme.onSurface
                                        )
                                        Spacer(modifier = Modifier.height(3.dp))
                                        Text(
                                            "${lastWorkout.exercises.size} exercises completed",
                                            style = MaterialTheme.typography.bodySmall,
                                            color = MaterialTheme.colorScheme.onSurfaceVariant
                                        )
                                    }

                                    Surface(
                                        shape = RoundedCornerShape(12.dp),
                                        color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
                                    ) {
                                        Text(
                                            "${lastWorkout.exercises.sumOf { it.sets.size }} sets",
                                            style = MaterialTheme.typography.labelSmall,
                                            fontWeight = FontWeight.SemiBold,
                                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                                            modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp)
                                        )
                                    }
                                }
                            }
                        }
                    }
                }

                item {
                    Spacer(modifier = Modifier.height(100.dp))
                }
            }
        }
    }
}

@Composable
fun HomeStatCard(
    modifier: Modifier = Modifier,
    label: String,
    value: String,
    unit: String,
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    accentColor: Color
) {
    GlassCard(modifier = modifier) {
        Column(
            modifier = Modifier
                .padding(16.dp)
                .fillMaxWidth()
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = label,
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    letterSpacing = 1.2.sp,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.weight(1f),
                    maxLines = 1
                )
                Box(
                    modifier = Modifier
                        .size(28.dp)
                        .background(accentColor.copy(alpha = 0.15f), CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = icon,
                        contentDescription = null,
                        tint = accentColor,
                        modifier = Modifier.size(16.dp)
                    )
                }
            }

            Spacer(modifier = Modifier.height(10.dp))

            Row(
                verticalAlignment = Alignment.Bottom,
                horizontalArrangement = Arrangement.spacedBy(4.dp)
            ) {
                Text(
                    text = value,
                    style = MaterialTheme.typography.headlineMedium.copy(fontSize = 28.sp),
                    fontWeight = FontWeight.Black,
                    color = MaterialTheme.colorScheme.onSurface
                )
                if (unit.isNotEmpty()) {
                    Text(
                        text = unit,
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.padding(bottom = 4.dp)
                    )
                }
            }
        }
    }
}

@Composable
fun MonthlyProgressCard(completedWorkouts: List<WorkoutWithExercises>) {
    val prefs = Graph.appContext.getSharedPreferences("aurora_prefs", android.content.Context.MODE_PRIVATE)
    var restDays by remember {
        mutableStateOf(prefs.getStringSet("rest_days", emptySet()) ?: emptySet())
    }
    var selectedRestDay by remember { mutableStateOf<java.time.LocalDate?>(null) }

    var displayedMonth by remember { mutableStateOf(java.time.YearMonth.now()) }
    var expanded by remember { mutableStateOf(false) }

    val daysInMonth = displayedMonth.lengthOfMonth()
    val firstDayOffset = displayedMonth.atDay(1).dayOfWeek.value % 7

    val completedDays = remember(completedWorkouts, displayedMonth) {
        val set = mutableSetOf<Int>()
        completedWorkouts.forEach {
            val cal = Calendar.getInstance()
            cal.timeInMillis = it.workout.dateMillis
            val wYear = cal.get(Calendar.YEAR)
            val wMonth = cal.get(Calendar.MONTH) + 1
            if (wYear == displayedMonth.year && wMonth == displayedMonth.monthValue) {
                set.add(cal.get(Calendar.DAY_OF_MONTH))
            }
        }
        set
    }

    val percentage = if (daysInMonth > 0) (completedDays.size * 100) / daysInMonth else 0
    val todayDate = if (displayedMonth == java.time.YearMonth.now()) java.time.LocalDate.now().dayOfMonth else -1

    GlassCard {
        Column(modifier = Modifier.padding(20.dp)) {
            // Header Row
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Box {
                    Text(
                        text = displayedMonth.month.name + " " + displayedMonth.year,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onSurface,
                        modifier = Modifier.clickable { expanded = true }
                    )
                    DropdownMenu(
                        expanded = expanded,
                        onDismissRequest = { expanded = false }
                    ) {
                        for (offset in -3..3) {
                            val ym = java.time.YearMonth.now().plusMonths(offset.toLong())
                            val currentLabel = ym.month.name.take(3) + " " + ym.year
                            DropdownMenuItem(
                                text = { Text(currentLabel, fontWeight = FontWeight.SemiBold, color = MaterialTheme.colorScheme.primary) },
                                onClick = {
                                    displayedMonth = ym
                                    expanded = false
                                }
                            )
                        }
                    }
                }

                Row(verticalAlignment = Alignment.CenterVertically) {
                    Text(
                        "$percentage%",
                        fontWeight = FontWeight.ExtraBold,
                        fontSize = 18.sp,
                        color = MaterialTheme.colorScheme.onSurface
                    )
                    Spacer(Modifier.width(8.dp))
                    Text(
                        "${completedDays.size}/$daysInMonth",
                        fontSize = 13.sp,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Days Header
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                val days = listOf("S", "M", "T", "W", "T", "F", "S")
                days.forEach {
                    Text(
                        it,
                        modifier = Modifier.weight(1f),
                        textAlign = TextAlign.Center,
                        fontSize = 12.sp,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        fontWeight = FontWeight.SemiBold
                    )
                }
            }

            Spacer(modifier = Modifier.height(8.dp))

            // Calendar Grid
            val totalCells = daysInMonth + firstDayOffset
            val rows = Math.ceil(totalCells / 7.0).toInt()
            var currentDay = 1

            for (i in 0 until rows) {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 3.dp),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    for (j in 0..6) {
                        val cellIndex = i * 7 + j
                        Box(
                            modifier = Modifier
                                .weight(1f)
                                .aspectRatio(1f),
                            contentAlignment = Alignment.Center
                        ) {
                            if (cellIndex >= firstDayOffset && currentDay <= daysInMonth) {
                                val cellDate = displayedMonth.atDay(currentDay)
                                val dateStr = cellDate.toString()
                                val isCompleted = completedDays.contains(currentDay)
                                val isToday = currentDay == todayDate
                                val isRestDay = restDays.contains(dateStr)
                                val isPastOrPresent = !cellDate.isAfter(java.time.LocalDate.now())

                                Box(
                                    modifier = Modifier
                                        .size(34.dp)
                                        .clip(CircleShape)
                                        .background(
                                            brush = if (isCompleted) CompletedBadgeGradient
                                            else if (isRestDay) Brush.linearGradient(listOf(Color(0xFF38BDF8).copy(alpha = 0.25f), Color(0xFF0284C7).copy(alpha = 0.25f)))
                                            else Brush.linearGradient(listOf(Color.Transparent, Color.Transparent)),
                                            shape = CircleShape
                                        )
                                        .clickable(enabled = isPastOrPresent) {
                                            selectedRestDay = cellDate
                                        },
                                    contentAlignment = Alignment.Center
                                ) {
                                    Text(
                                        text = currentDay.toString(),
                                        fontSize = 13.sp,
                                        fontWeight = if (isCompleted || isToday || isRestDay) FontWeight.Bold else FontWeight.Normal,
                                        color = if (isCompleted) Color.White
                                        else if (isToday) ElectricViolet
                                        else if (isRestDay) ElectricCyan
                                        else MaterialTheme.colorScheme.onSurface
                                    )
                                }
                                currentDay++
                            }
                        }
                    }
                }
            }
        }
    }

    if (selectedRestDay != null) {
        val dateStr = selectedRestDay.toString()
        val isCurrentlyRest = restDays.contains(dateStr)
        AlertDialog(
            onDismissRequest = { selectedRestDay = null },
            shape = RoundedCornerShape(24.dp),
            title = {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Icon(
                        Icons.Default.Bedtime,
                        contentDescription = null,
                        tint = ElectricCyan,
                        modifier = Modifier.size(24.dp)
                    )
                    Spacer(Modifier.width(10.dp))
                    Text(
                        if (isCurrentlyRest) "Remove Rest Day" else "Mark Rest Day",
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold
                    )
                }
            },
            text = {
                Text(
                    if (isCurrentlyRest) "Do you want to remove $dateStr from your recorded rest days?"
                    else "Do you want to mark $dateStr as a Rest Day in your activity calendar?",
                    style = MaterialTheme.typography.bodyMedium
                )
            },
            confirmButton = {
                Button(
                    onClick = {
                        val newSet = restDays.toMutableSet()
                        if (isCurrentlyRest) newSet.remove(dateStr) else newSet.add(dateStr)
                        restDays = newSet
                        prefs.edit().putStringSet("rest_days", newSet).apply()
                        selectedRestDay = null
                    },
                    colors = ButtonDefaults.buttonColors(
                        containerColor = if (isCurrentlyRest) MaterialTheme.colorScheme.error else ElectricViolet,
                        contentColor = Color.White
                    ),
                    shape = RoundedCornerShape(14.dp)
                ) {
                    Text(if (isCurrentlyRest) "Remove" else "Mark as Rest Day", fontWeight = FontWeight.Bold)
                }
            },
            dismissButton = {
                TextButton(onClick = { selectedRestDay = null }) { Text("Cancel") }
            }
        )
    }
}
