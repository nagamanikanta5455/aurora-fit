import re

with open('/app/applet/app/src/main/java/com/example/ui/home/HomeScreen.kt', 'r') as f:
    content = f.read()

# Make sure com.example.Graph is imported
if 'import com.example.Graph' not in content:
    content = content.replace('import com.example.ui.stats.StatsHelper', 'import com.example.ui.stats.StatsHelper\nimport com.example.Graph\nimport androidx.compose.ui.draw.clip')

monthly_progress_card_old = """@SuppressLint("NewApi")
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
}"""

monthly_progress_card_new = """@SuppressLint("NewApi")
@Composable
fun MonthlyProgressCard(completedWorkouts: List<WorkoutWithExercises>) {
    val prefs = remember { Graph.appContext.getSharedPreferences("aurorafit_rest_days", android.content.Context.MODE_PRIVATE) }
    var restDays by remember { mutableStateOf(prefs.getStringSet("rest_days", emptySet())?.toSet() ?: emptySet()) }
    var selectedRestDay by remember { mutableStateOf<java.time.LocalDate?>(null) }

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
                                val cellDate = displayedMonth.atDay(currentDay)
                                val dateStr = cellDate.toString()
                                val isCompleted = completedDays.contains(currentDay)
                                val isToday = currentDay == todayDate
                                val isRestDay = restDays.contains(dateStr)
                                val isPastOrPresent = !cellDate.isAfter(java.time.LocalDate.now())
                                
                                Box(
                                    modifier = Modifier
                                        .size(32.dp)
                                        .clip(CircleShape)
                                        .background(
                                            color = if (isCompleted) MaterialTheme.colorScheme.primary 
                                                    else if (isRestDay) MaterialTheme.colorScheme.onSurface.copy(alpha = 0.1f) 
                                                    else Color.Transparent
                                        )
                                        .clickable(enabled = isPastOrPresent) {
                                            selectedRestDay = cellDate
                                        },
                                    contentAlignment = Alignment.Center
                                ) {
                                    Text(
                                        text = currentDay.toString(),
                                        fontSize = 14.sp,
                                        fontWeight = if (isCompleted || isToday || isRestDay) FontWeight.Bold else FontWeight.Normal,
                                        color = if (isCompleted) MaterialTheme.colorScheme.onPrimary 
                                                else if (isToday) MaterialTheme.colorScheme.primary 
                                                else if (isRestDay) MaterialTheme.colorScheme.onSurfaceVariant 
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
            title = { Text(if (isCurrentlyRest) "Remove Rest Day" else "Mark Rest Day") },
            text = { Text(if (isCurrentlyRest) "Do you want to remove $dateStr from your rest days?" else "Do you want to mark $dateStr as a Rest Day?") },
            confirmButton = {
                TextButton(onClick = {
                    val newSet = restDays.toMutableSet()
                    if (isCurrentlyRest) newSet.remove(dateStr) else newSet.add(dateStr)
                    restDays = newSet
                    prefs.edit().putStringSet("rest_days", newSet).apply()
                    selectedRestDay = null
                }) {
                    Text(if (isCurrentlyRest) "Remove" else "Mark as Rest Day")
                }
            },
            dismissButton = {
                TextButton(onClick = { selectedRestDay = null }) { Text("Cancel") }
            }
        )
    }
}"""

content = content.replace(monthly_progress_card_old, monthly_progress_card_new)

with open('/app/applet/app/src/main/java/com/example/ui/home/HomeScreen.kt', 'w') as f:
    f.write(content)

