content = """package com.example.ui.home

import android.annotation.SuppressLint
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.DarkMode
import androidx.compose.material.icons.filled.LightMode
import androidx.compose.material.icons.filled.LocalFireDepartment
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.shadow
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
import com.example.data.model.WorkoutWithExercises
import com.example.ui.MainViewModel
import com.example.ui.stats.StatsHelper
import java.util.Calendar
import java.util.Locale

@Composable
fun HomeScreen(viewModel: MainViewModel, navController: NavController, paddingValues: PaddingValues) {
    val workouts by viewModel.allWorkouts.collectAsState()
    val completedWorkouts = workouts.filter { it.workout.isCompleted }
    val streak = StatsHelper.calculateStreak(completedWorkouts)
    val thisMonth = StatsHelper.workoutsThisMonth(completedWorkouts)
    
    val greeting = remember {
        val hour = Calendar.getInstance(java.util.TimeZone.getDefault()).get(Calendar.HOUR_OF_DAY)
        when (hour) {
            in 5..11 -> "Good Morning"
            in 12..16 -> "Good Afternoon"
            else -> "Good Evening"
        }
    }

    val todayCompleted = completedWorkouts.firstOrNull { 
        val cal = Calendar.getInstance().apply { timeInMillis = it.workout.dateMillis }
        val now = Calendar.getInstance()
        cal.get(Calendar.YEAR) == now.get(Calendar.YEAR) && cal.get(Calendar.DAY_OF_YEAR) == now.get(Calendar.DAY_OF_YEAR)
    }
    
    val hasTrainedToday = todayCompleted != null
    val isDarkMode by viewModel.isDarkMode.collectAsState()
    val haptic = LocalHapticFeedback.current

    Scaffold(
        modifier = Modifier.fillMaxSize().padding(paddingValues),
        containerColor = Color.Transparent
    ) { innerPadding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(
                    brush = Brush.linearGradient(
                        colors = if (isDarkMode) listOf(
                            Color(0xFF0F172A),
                            Color(0xFF1E1B4B),
                            Color(0xFF064E3B)
                        ) else listOf(
                            Color(0xFFF8FAFC),
                            Color(0xFFE0E7FF),
                            Color(0xFFD1FAE5)
                        )
                    )
                )
        ) {
            LazyColumn(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(innerPadding)
                    .padding(bottom = 16.dp),
                contentPadding = PaddingValues(start = 24.dp, end = 24.dp, top = 32.dp, bottom = 48.dp),
                verticalArrangement = Arrangement.spacedBy(24.dp)
            ) {
                item {
                    Box(modifier = Modifier.fillMaxWidth()) {
                        Column(modifier = Modifier.align(Alignment.TopStart).padding(end = 48.dp)) {
                            Text(
                                text = greeting, 
                                style = MaterialTheme.typography.labelLarge, 
                                color = MaterialTheme.colorScheme.primary, 
                                fontWeight = FontWeight.Bold, 
                                letterSpacing = 2.sp
                            )
                            Spacer(modifier = Modifier.height(8.dp))
                            Text(
                                text = if (hasTrainedToday) "Great work today" else "Ready to train?", 
                                style = MaterialTheme.typography.headlineLarge, 
                                fontWeight = FontWeight.Light, 
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
                
                item {
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                        PremiumCard(modifier = Modifier.weight(1f)) {
                            Column(modifier = Modifier.padding(20.dp)) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(Icons.Default.LocalFireDepartment, contentDescription = null, tint = Color(0xFFFF9800), modifier = Modifier.size(20.dp))
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Text("$streak days", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface)
                                }
                                Spacer(modifier = Modifier.height(4.dp))
                                Text("Current Streak", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                        }
                        PremiumCard(modifier = Modifier.weight(1f)) {
                            Column(modifier = Modifier.padding(20.dp)) {
                                Text("$thisMonth", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface)
                                Spacer(modifier = Modifier.height(4.dp))
                                Text("Workouts this month", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                        }
                    }
                }
                item {
                    MonthlyProgressCard(completedWorkouts = completedWorkouts)
                }
                item {
                    Text("TODAY", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.onSurfaceVariant, letterSpacing = 1.sp)
                    Spacer(modifier = Modifier.height(12.dp))
                    
                    if (todayCompleted != null) {
                        PremiumCard {
                            Row(modifier = Modifier.fillMaxWidth().padding(24.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                Column {
                                    Text(todayCompleted.workout.name.uppercase(), style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface)
                                    Spacer(modifier = Modifier.height(4.dp))
                                    Text("Completed", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.primary)
                                }
                            }
                        }
                    } else {
                        PremiumCard(
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
                            Row(modifier = Modifier.fillMaxWidth().padding(24.dp), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                                Column {
                                    Text("No workout yet", style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface)
                                    Spacer(modifier = Modifier.height(4.dp))
                                    Text("Start today's session", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
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
                                    shape = RoundedCornerShape(12.dp),
                                    colors = ButtonDefaults.buttonColors(
                                        containerColor = MaterialTheme.colorScheme.primary,
                                        contentColor = MaterialTheme.colorScheme.onPrimary
                                    )
                                ) {
                                    Text("START", fontWeight = FontWeight.Bold)
                                }
                            }
                        }
                    }
                }
                item {
                    val lastWorkout = completedWorkouts.firstOrNull { w -> todayCompleted == null || w.workout.id != todayCompleted.workout.id }
                    if (lastWorkout != null) {
                        Text("LAST WORKOUT", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.onSurfaceVariant, letterSpacing = 1.sp)
                        Spacer(modifier = Modifier.height(12.dp))
                        PremiumCard {
                            Column(modifier = Modifier.fillMaxWidth().padding(20.dp)) {
                                Text(lastWorkout.workout.name.uppercase(), style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onSurface)
                                Spacer(modifier = Modifier.height(4.dp))
                                Text("${lastWorkout.exercises.size} exercises", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            }
                        }
                    }
                }
            }
        }
    }

    @SuppressLint("NewApi")
    @Composable
    fun MonthlyProgressCard(completedWorkouts: List<WorkoutWithExercises>) {
        val currentMonth = remember { java.time.YearMonth.now(java.time.ZoneId.systemDefault()) }
        var displayedMonth by remember { mutableStateOf(currentMonth) }
        var expanded by remember { mutableStateOf(false) }

        val availableMonths = remember(currentMonth) {
            val months = mutableListOf<java.time.YearMonth>()
            var startMonth = java.time.YearMonth.of(2026, 8)
            while (!startMonth.isAfter(currentMonth)) {
                months.add(startMonth)
                startMonth = startMonth.plusMonths(1)
            }
            months.reversed()
        }

        val daysInMonth = displayedMonth.lengthOfMonth()
        val calendar = Calendar.getInstance()
        calendar.set(Calendar.DAY_OF_MONTH, 1)
        val firstDayVal = displayedMonth.atDay(1).dayOfWeek.value
        val firstDayOffset = if (firstDayVal == 7) 0 else firstDayVal
        
        val monthFormatter = java.time.format.DateTimeFormatter.ofPattern("MMMM yyyy", Locale.getDefault())
        val monthName = displayedMonth.format(monthFormatter).uppercase()

        val completedDays = remember(completedWorkouts, displayedMonth) {
            completedWorkouts.mapNotNull {
                val c = Calendar.getInstance()
                c.timeInMillis = it.workout.dateMillis
                if (c.get(Calendar.YEAR) == displayedMonth.year && c.get(Calendar.MONTH) + 1 == displayedMonth.monthValue) {
                    c.get(Calendar.DAY_OF_MONTH)
                } else null
            }.toSet()
        }

        val percentage = if (daysInMonth > 0) (completedDays.size * 100) / daysInMonth else 0
        val todayDate = if (displayedMonth == currentMonth) java.time.LocalDate.now().dayOfMonth else -1

        PremiumCard {
            Column(modifier = Modifier.padding(20.dp)) {
                // Header
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box {
                        Text(
                            text = "$monthName ▼", 
                            fontWeight = FontWeight.Bold, 
                            color = MaterialTheme.colorScheme.primary, 
                            letterSpacing = 1.sp,
                            modifier = Modifier
                                .clickable { expanded = true }
                                .padding(vertical = 4.dp, horizontal = 2.dp)
                        )
                        DropdownMenu(
                            expanded = expanded, 
                            onDismissRequest = { expanded = false },
                            modifier = Modifier.background(MaterialTheme.colorScheme.surface)
                        ) {
                            availableMonths.forEach { ym ->
                                val textLabel = ym.format(monthFormatter).uppercase()
                                DropdownMenuItem(
                                    text = { Text(textLabel, fontWeight = FontWeight.SemiBold, color = MaterialTheme.colorScheme.primary) },
                                    onClick = {
                                        displayedMonth = ym
                                        expanded = false
                                    }
                                )
                            }
                        }
                    }
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text("$percentage%", fontWeight = FontWeight.ExtraBold, fontSize = 20.sp, color = MaterialTheme.colorScheme.onSurface)
                        Spacer(Modifier.width(12.dp))
                        Text("${completedDays.size}/$daysInMonth", fontSize = 14.sp, color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.6f))
                    }
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                
                // Days Header
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    val days = listOf("S", "M", "T", "W", "T", "F", "S")
                    days.forEach {
                        Text(it, modifier = Modifier.weight(1f), textAlign = TextAlign.Center, fontSize = 12.sp, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
                
                Spacer(modifier = Modifier.height(8.dp))
                
                // Calendar Grid
                val totalCells = daysInMonth + firstDayOffset
                val rows = Math.ceil(totalCells / 7.0).toInt()
                var currentDay = 1
                
                for (i in 0 until rows) {
                    Row(modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp), horizontalArrangement = Arrangement.SpaceBetween) {
                        for (j in 0..6) {
                            val cellIndex = i * 7 + j
                            Box(
                                modifier = Modifier.weight(1f).aspectRatio(1f),
                                contentAlignment = Alignment.Center
                            ) {
                                if (cellIndex >= firstDayOffset && currentDay <= daysInMonth) {
                                    val isCompleted = completedDays.contains(currentDay)
                                    val isToday = currentDay == todayDate
                                    
                                    Box(
                                        modifier = Modifier
                                            .size(32.dp)
                                            .background(
                                                color = if (isCompleted) MaterialTheme.colorScheme.primary else Color.Transparent,
                                                shape = CircleShape
                                            ),
                                        contentAlignment = Alignment.Center
                                    ) {
                                        Text(
                                            text = currentDay.toString(),
                                            fontSize = 14.sp,
                                            fontWeight = if (isCompleted || isToday) FontWeight.Bold else FontWeight.Normal,
                                            color = if (isCompleted) MaterialTheme.colorScheme.onPrimary else if (isToday) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface
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
    }

    @Composable
    fun PremiumCard(modifier: Modifier = Modifier, content: @Composable () -> Unit) {
        Card(
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface),
            shape = RoundedCornerShape(24.dp),
            modifier = modifier.shadow(
                elevation = 12.dp,
                shape = RoundedCornerShape(24.dp),
                spotColor = Color(0x1A000000),
                ambientColor = Color(0x05000000)
            )
        ) {
            content()
        }
    }
"""

with open('/app/applet/app/src/main/java/com/example/ui/home/HomeScreen.kt', 'w') as f:
    f.write(content)
