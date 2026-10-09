code = '''package com.example.ui.history

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.animateContentSize
import androidx.compose.animation.core.tween
import androidx.compose.animation.expandVertically
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.animation.shrinkVertically
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.FitnessCenter
import androidx.compose.material.icons.filled.KeyboardArrowDown
import androidx.compose.material.icons.filled.KeyboardArrowUp
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Timer
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.data.model.WorkoutWithExercises
import com.example.data.model.ExerciseType
import com.example.ui.MainViewModel
import java.text.DecimalFormat
import java.text.SimpleDateFormat
import java.util.*

/**
 * Helper function to format large numbers compactly (e.g., 10000 -> "10k", 10500 -> "10.5k", 1000000 -> "1M")
 */
fun formatCompactNumber(number: Int): String {
    if (number < 1000) return number.toString()
    val df = DecimalFormat("#.#")
    return if (number < 1_000_000) {
        val kVal = number / 1000.0
        "${df.format(kVal)}k"
    } else {
        val mVal = number / 1_000_000.0
        "${df.format(mVal)}M"
    }
}

fun formatDuration(totalSeconds: Int): String {
    if (totalSeconds < 60) return "${totalSeconds}s"
    val minutes = totalSeconds / 60
    if (minutes < 60) return "${minutes}m"
    val hours = minutes / 60
    val remainingMinutes = minutes % 60
    return if (remainingMinutes > 0) "${hours}h ${remainingMinutes}m" else "${hours}h"
}

@Composable
fun HistoryScreen(viewModel: MainViewModel, paddingValues: PaddingValues) {
    val workouts by viewModel.allWorkouts.collectAsState()
    val isDarkMode by viewModel.isDarkMode.collectAsState()
    val completedWorkouts = workouts.filter { it.workout.isCompleted }.sortedByDescending { it.workout.dateMillis }

    // Calculates lifetime stats in-memory
    val totalWorkouts = completedWorkouts.size
    var totalSets = 0
    var totalReps = 0
    var totalDurationSeconds = 0

    completedWorkouts.forEach { w ->
        w.exercises.forEach { e ->
            totalSets += e.sets.size
            e.sets.forEach { set ->
                totalReps += set.reps ?: 0
                totalDurationSeconds += set.durationSeconds ?: 0
            }
        }
    }

    val formattedDuration = formatDuration(totalDurationSeconds)
    val formattedReps = formatCompactNumber(totalReps)
    val formattedSets = formatCompactNumber(totalSets)
    val formattedWorkouts = formatCompactNumber(totalWorkouts)

    // State for expanding/collapsing timeline beyond top 5
    var isTimelineExpanded by remember { mutableStateOf(false) }
    val displayedWorkouts = if (isTimelineExpanded) completedWorkouts else completedWorkouts.take(5)

    Surface(
        modifier = Modifier.fillMaxSize(),
        color = MaterialTheme.colorScheme.background
    ) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(
                    brush = Brush.radialGradient(
                        colors = if (isDarkMode) listOf(
                            Color(0xFF064E3B),
                            Color(0xFF0F172A)
                        ) else listOf(
                            MaterialTheme.colorScheme.tertiary.copy(alpha = 0.3f),
                            MaterialTheme.colorScheme.background
                        ),
                        radius = 1500f
                    )
                )
        ) {
            if (completedWorkouts.isEmpty()) {
                Box(modifier = Modifier.fillMaxSize().padding(32.dp), contentAlignment = Alignment.Center) {
                    Text("Your training timeline is empty.", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 18.sp)
                }
            } else {
                LazyColumn(
                    modifier = Modifier.fillMaxSize().padding(paddingValues),
                    contentPadding = PaddingValues(start = 24.dp, end = 24.dp, top = 32.dp, bottom = 24.dp),
                    verticalArrangement = Arrangement.spacedBy(24.dp)
                ) {
                    item {
                        Text("DASHBOARD", style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, letterSpacing = 2.sp)
                        Spacer(modifier = Modifier.height(8.dp))
                        Text("Performance", style = MaterialTheme.typography.headlineLarge, fontWeight = FontWeight.Light, color = MaterialTheme.colorScheme.onBackground)
                        Spacer(modifier = Modifier.height(16.dp))

                        // Advanced 2x2 Performance Metrics Grid
                        Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                                StatCard(
                                    modifier = Modifier.weight(1f),
                                    value = formattedWorkouts,
                                    label = "Workouts",
                                    subtitle = "Total sessions"
                                )
                                StatCard(
                                    modifier = Modifier.weight(1f),
                                    value = formattedSets,
                                    label = "Sets",
                                    subtitle = "Completed sets"
                                )
                            }
                            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                                StatCard(
                                    modifier = Modifier.weight(1f),
                                    value = formattedReps,
                                    label = "Reps / Volume",
                                    subtitle = "Total volume"
                                )
                                StatCard(
                                    modifier = Modifier.weight(1f),
                                    value = formattedDuration,
                                    label = "Active Time",
                                    subtitle = "Total duration"
                                )
                            }
                        }
                    }

                    item {
                        WeeklyActivityChart(completedWorkouts)
                    }

                    item {
                        DistributionCard(completedWorkouts)
                    }

                    item {
                        Spacer(modifier = Modifier.height(8.dp))
                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.SpaceBetween,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Text(
                                "TIMELINE",
                                style = MaterialTheme.typography.labelLarge,
                                color = MaterialTheme.colorScheme.primary,
                                fontWeight = FontWeight.Bold,
                                letterSpacing = 2.sp
                            )
                            Surface(
                                shape = RoundedCornerShape(12.dp),
                                color = MaterialTheme.colorScheme.primary.copy(alpha = 0.12f)
                            ) {
                                Text(
                                    text = "${completedWorkouts.size} total",
                                    style = MaterialTheme.typography.labelSmall,
                                    color = MaterialTheme.colorScheme.primary,
                                    fontWeight = FontWeight.SemiBold,
                                    modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp)
                                )
                            }
                        }
                    }

                    items(
                        items = displayedWorkouts,
                        key = { it.workout.id }
                    ) { workout ->
                        WorkoutHistoryCard(
                            workout = workout,
                            onDelete = { viewModel.deleteWorkout(workout.workout) }
                        )
                    }

                    // Show More / Show Less Pagination Button if more than 5 workouts
                    if (completedWorkouts.size > 5) {
                        item {
                            Surface(
                                shape = RoundedCornerShape(16.dp),
                                color = MaterialTheme.colorScheme.surface.copy(alpha = 0.9f),
                                tonalElevation = 2.dp,
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .shadow(4.dp, RoundedCornerShape(16.dp), spotColor = Color(0x0A000000))
                                    .clickable { isTimelineExpanded = !isTimelineExpanded }
                            ) {
                                Row(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(vertical = 14.dp, horizontal = 20.dp),
                                    horizontalArrangement = Arrangement.Center,
                                    verticalAlignment = Alignment.CenterVertically
                                ) {
                                    Text(
                                        text = if (isTimelineExpanded) "Show Less" else "Show All Workouts (${completedWorkouts.size})",
                                        style = MaterialTheme.typography.labelLarge,
                                        fontWeight = FontWeight.Bold,
                                        color = MaterialTheme.colorScheme.primary,
                                        letterSpacing = 0.5.sp
                                    )
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Icon(
                                        imageVector = if (isTimelineExpanded) Icons.Default.KeyboardArrowUp else Icons.Default.KeyboardArrowDown,
                                        contentDescription = if (isTimelineExpanded) "Collapse timeline" else "Expand timeline",
                                        tint = MaterialTheme.colorScheme.primary,
                                        modifier = Modifier.size(20.dp)
                                    )
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun StatCard(
    modifier: Modifier = Modifier,
    value: String,
    label: String,
    subtitle: String = ""
) {
    Card(
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface.copy(alpha = 0.95f)),
        shape = RoundedCornerShape(20.dp),
        modifier = modifier.shadow(8.dp, RoundedCornerShape(20.dp), spotColor = Color(0x0A000000))
    ) {
        Column(
            modifier = Modifier
                .padding(horizontal = 16.dp, vertical = 18.dp)
                .fillMaxWidth(),
            horizontalAlignment = Alignment.Start
        ) {
            Text(
                text = value,
                style = MaterialTheme.typography.headlineMedium,
                fontWeight = FontWeight.ExtraBold,
                color = MaterialTheme.colorScheme.onSurface,
                maxLines = 1
            )
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = label,
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.SemiBold,
                color = MaterialTheme.colorScheme.primary,
                maxLines = 1
            )
            if (subtitle.isNotEmpty()) {
                Spacer(modifier = Modifier.height(2.dp))
                Text(
                    text = subtitle,
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.8f),
                    maxLines = 1
                )
            }
        }
    }
}

@Composable
fun WeeklyActivityChart(workouts: List<WorkoutWithExercises>) {
    // Generate last 7 days
    val daysList = mutableListOf<Pair<String, Int>>() // Day name ("Mon") to sets count
    val calendar = Calendar.getInstance()
    calendar.time = Date()

    val format = SimpleDateFormat("EEE", Locale.getDefault())
    val startOfDay = Calendar.getInstance().apply {
        set(Calendar.HOUR_OF_DAY, 0)
        set(Calendar.MINUTE, 0)
        set(Calendar.SECOND, 0)
        set(Calendar.MILLISECOND, 0)
    }

    // Go back 6 days to get a 7 day window ending today
    startOfDay.add(Calendar.DAY_OF_YEAR, -6)

    for (i in 0..6) {
        val currentDayStart = startOfDay.timeInMillis
        val currentDayEnd = currentDayStart + (24 * 60 * 60 * 1000) - 1

        val dayName = format.format(Date(currentDayStart))

        val setsThatDay = workouts.filter {
            it.workout.dateMillis in currentDayStart..currentDayEnd
        }.sumOf { w -> w.exercises.sumOf { e -> e.sets.size } }

        daysList.add(dayName to setsThatDay)
        startOfDay.add(Calendar.DAY_OF_YEAR, 1)
    }

    val maxSets = daysList.maxOfOrNull { it.second }?.coerceAtLeast(1) ?: 1

    Card(
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface.copy(alpha = 0.95f)),
        shape = RoundedCornerShape(24.dp),
        modifier = Modifier.fillMaxWidth().shadow(12.dp, RoundedCornerShape(24.dp), spotColor = Color(0x0A000000))
    ) {
        Column(modifier = Modifier.padding(24.dp)) {
            Text("LAST 7 DAYS", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant, letterSpacing = 1.sp)
            Spacer(modifier = Modifier.height(24.dp))

            Row(
                modifier = Modifier.fillMaxWidth().height(120.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.Bottom
            ) {
                daysList.forEach { (day, count) ->
                    val heightRatio = (count.toFloat() / maxSets.toFloat()).coerceIn(0f, 1f)
                    // Ensure a minimum height so empty days show a tiny nub
                    val animatedHeight = if (heightRatio > 0f) heightRatio else 0.05f

                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        verticalArrangement = Arrangement.Bottom,
                        modifier = Modifier.fillMaxHeight()
                    ) {
                        Box(
                            modifier = Modifier
                                .width(28.dp)
                                .weight(1f, fill = false)
                                .fillMaxHeight(animatedHeight)
                                .background(
                                    color = if (count > 0) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f),
                                    shape = RoundedCornerShape(topStart = 8.dp, topEnd = 8.dp, bottomStart = 2.dp, bottomEnd = 2.dp)
                                )
                        )
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(day, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                }
            }
        }
    }
}

@Composable
fun DistributionCard(workouts: List<WorkoutWithExercises>) {
    val total = workouts.size
    val weights = workouts.count { it.workout.name.contains("Weights", ignoreCase = true) }
    val bw = total - weights

    val weightsWeight = if (total > 0) weights.toFloat() / total else 0.5f
    val bwWeight = if (total > 0) bw.toFloat() / total else 0.5f

    Card(
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface.copy(alpha = 0.95f)),
        shape = RoundedCornerShape(24.dp),
        modifier = Modifier.fillMaxWidth().shadow(12.dp, RoundedCornerShape(24.dp), spotColor = Color(0x0A000000))
    ) {
        Column(modifier = Modifier.padding(24.dp)) {
            Text("TRAINING FOCUS", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant, letterSpacing = 1.sp)
            Spacer(modifier = Modifier.height(20.dp))

            // Sleek Segmented Progress Bar
            Row(modifier = Modifier.fillMaxWidth().height(16.dp).clip(RoundedCornerShape(8.dp))) {
                if (weightsWeight > 0f) {
                    Box(modifier = Modifier.fillMaxHeight().weight(weightsWeight).background(
                        brush = Brush.horizontalGradient(
                            colors = listOf(Color(0xFF4F46E5), Color(0xFF818CF8))
                        )
                    ))
                }
                if (bwWeight > 0f) {
                    Box(modifier = Modifier.fillMaxHeight().weight(bwWeight).background(
                        brush = Brush.horizontalGradient(
                            colors = listOf(Color(0xFF10B981), Color(0xFF34D399))
                        )
                    ))
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Box(modifier = Modifier.size(10.dp).background(Color(0xFF4F46E5), CircleShape))
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("Weights", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.SemiBold)
                    Spacer(modifier = Modifier.width(4.dp))
                    Text("($weights)", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Box(modifier = Modifier.size(10.dp).background(Color(0xFF10B981), CircleShape))
                    Spacer(modifier = Modifier.width(8.dp))
                    Text("Bodyweight", style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurface, fontWeight = FontWeight.SemiBold)
                    Spacer(modifier = Modifier.width(4.dp))
                    Text("($bw)", style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }
            }
        }
    }
}

@Composable
fun WorkoutHistoryCard(workout: WorkoutWithExercises, onDelete: () -> Unit) {
    var expanded by remember { mutableStateOf(false) }
    val dateBadgeFormat = remember { SimpleDateFormat("MMM d", Locale.getDefault()) }
    val fullDateFormat = remember { SimpleDateFormat("MMM d, yyyy", Locale.getDefault()) }

    val isWeights = workout.workout.name.contains("Weights", ignoreCase = true)
    val totalSets = workout.exercises.sumOf { it.sets.size }
    val totalReps = workout.exercises.sumOf { e -> e.sets.sumOf { it.reps ?: 0 } }
    val workoutDurationSeconds = workout.exercises.sumOf { e -> e.sets.sumOf { it.durationSeconds ?: 0 } }

    Card(
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface.copy(alpha = 0.95f)),
        shape = RoundedCornerShape(24.dp),
        modifier = Modifier
            .fillMaxWidth()
            .shadow(12.dp, RoundedCornerShape(24.dp), spotColor = Color(0x0A000000))
            .clickable { expanded = !expanded }
            .animateContentSize()
    ) {
        Column(modifier = Modifier.padding(20.dp)) {
            // Header Row: Icon + Title & Date
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.weight(1f)
                ) {
                    Box(
                        modifier = Modifier
                            .size(46.dp)
                            .background(
                                color = if (isWeights) MaterialTheme.colorScheme.primary.copy(alpha = 0.12f)
                                else MaterialTheme.colorScheme.tertiary.copy(alpha = 0.15f),
                                shape = CircleShape
                            ),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            imageVector = if (isWeights) Icons.Default.FitnessCenter else Icons.Default.Person,
                            contentDescription = null,
                            tint = if (isWeights) MaterialTheme.colorScheme.primary else Color(0xFF10B981),
                            modifier = Modifier.size(24.dp)
                        )
                    }
                    Spacer(modifier = Modifier.width(14.dp))
                    Column {
                        Text(
                            text = workout.workout.name.uppercase().replace(" WORKOUT", ""),
                            style = MaterialTheme.typography.titleMedium,
                            fontWeight = FontWeight.Bold,
                            color = MaterialTheme.colorScheme.onSurface
                        )
                        Spacer(modifier = Modifier.height(2.dp))
                        Text(
                            text = fullDateFormat.format(Date(workout.workout.dateMillis)),
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            style = MaterialTheme.typography.labelSmall
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(14.dp))

            // Dynamic Badges Row: Date Badge, Duration Badge, Sets/Exercises Badges
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                // 1. Date Badge
                Surface(
                    shape = RoundedCornerShape(10.dp),
                    color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.7f)
                ) {
                    Text(
                        text = dateBadgeFormat.format(Date(workout.workout.dateMillis)),
                        style = MaterialTheme.typography.labelSmall,
                        fontWeight = FontWeight.SemiBold,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                    )
                }

                // 2. Duration Badge (if timed sets exist)
                if (workoutDurationSeconds > 0) {
                    val durBadgeText = formatDuration(workoutDurationSeconds)
                    Surface(
                        shape = RoundedCornerShape(10.dp),
                        color = MaterialTheme.colorScheme.primary.copy(alpha = 0.14f)
                    ) {
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                        ) {
                            Text(
                                text = "⏱ $durBadgeText",
                                style = MaterialTheme.typography.labelSmall,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.primary
                            )
                        }
                    }
                }

                // 3. Exercise & Sets Badge
                Surface(
                    shape = RoundedCornerShape(10.dp),
                    color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.7f)
                ) {
                    Text(
                        text = "${workout.exercises.size} Ex · $totalSets Sets",
                        style = MaterialTheme.typography.labelSmall,
                        fontWeight = FontWeight.Medium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                    )
                }

                // 4. Reps badge if any reps exist
                if (totalReps > 0) {
                    Surface(
                        shape = RoundedCornerShape(10.dp),
                        color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
                    ) {
                        Text(
                            text = "${formatCompactNumber(totalReps)} reps",
                            style = MaterialTheme.typography.labelSmall,
                            fontWeight = FontWeight.Medium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                        )
                    }
                }
            }

            // Expanded Workout Details
            if (expanded) {
                Spacer(modifier = Modifier.height(20.dp))
                HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.4f))
                Spacer(modifier = Modifier.height(16.dp))

                workout.exercises.forEach { exercise ->
                    Text(
                        text = exercise.exercise.name,
                        fontWeight = FontWeight.SemiBold,
                        color = MaterialTheme.colorScheme.primary,
                        fontSize = 15.sp
                    )
                    Spacer(modifier = Modifier.height(4.dp))
                    val setsText = exercise.sets.joinToString(" · ") { set ->
                        when (exercise.exercise.type) {
                            ExerciseType.WEIGHTED, ExerciseType.WEIGHTED_BODYWEIGHT -> "${set.weight?.toInt() ?: 0}×${set.reps ?: 0}"
                            ExerciseType.BODYWEIGHT -> "${set.reps ?: 0} reps"
                            ExerciseType.TIMED -> "${set.durationSeconds ?: 0}s"
                        }
                    }
                    Text(
                        text = setsText,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        fontSize = 14.sp
                    )
                    Spacer(modifier = Modifier.height(14.dp))
                }

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.End
                ) {
                    TextButton(
                        onClick = onDelete,
                        colors = ButtonDefaults.textButtonColors(contentColor = MaterialTheme.colorScheme.error)
                    ) {
                        Text("DELETE RECORD", fontWeight = FontWeight.Bold, letterSpacing = 1.sp)
                    }
                }
            }
        }
    }
}
'''

with open('app/src/main/java/com/example/ui/history/HistoryScreen.kt', 'w') as f:
    f.write(code)

print("Updated HistoryScreen.kt successfully!")
