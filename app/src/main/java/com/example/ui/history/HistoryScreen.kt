package com.example.ui.history

import androidx.compose.animation.animateContentSize
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.FitnessCenter
import androidx.compose.material.icons.filled.KeyboardArrowDown
import androidx.compose.material.icons.filled.KeyboardArrowUp
import androidx.compose.material.icons.filled.LocalFireDepartment
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.PieChart
import androidx.compose.material.icons.filled.Repeat
import androidx.compose.material.icons.filled.Timer
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.data.model.ExerciseType
import com.example.data.model.WorkoutWithExercises
import com.example.ui.MainViewModel
import com.example.ui.components.GlassCard
import com.example.ui.theme.DarkMeshBackgroundGradient
import com.example.ui.theme.ElectricCyan
import com.example.ui.theme.ElectricViolet
import com.example.ui.theme.EmeraldGreen
import com.example.ui.theme.FlameOrange
import com.example.ui.theme.LightMeshBackgroundGradient
import java.text.SimpleDateFormat
import java.util.*

/**
 * Compact Number Formatter helper function:
 * 10000 -> "10k"
 * 10500 -> "10.5k"
 * 1000000 -> "1M"
 */
fun formatCompactNumber(number: Int): String {
    return when {
        number >= 1_000_000 -> {
            val millions = number / 1_000_000.0
            if (millions % 1.0 == 0.0) "${millions.toInt()}M" else String.format(Locale.US, "%.1fM", millions)
        }
        number >= 10_000 -> {
            val thousands = number / 1000.0
            if (thousands % 1.0 == 0.0) "${thousands.toInt()}k" else String.format(Locale.US, "%.1fk", thousands)
        }
        number >= 1_000 -> {
            val thousands = number / 1000.0
            if (thousands % 1.0 == 0.0) "${thousands.toInt()}k" else String.format(Locale.US, "%.1fk", thousands)
        }
        else -> number.toString()
    }
}

/**
 * Helper to format seconds into clean time strings (e.g. "52m" or "1h 45m")
 */
private fun formatDuration(totalSeconds: Int): String {
    val hours = totalSeconds / 3600
    val minutes = (totalSeconds % 3600) / 60
    return when {
        hours > 0 && minutes > 0 -> "${hours}h ${minutes}m"
        hours > 0 -> "${hours}h"
        minutes > 0 -> "${minutes}m"
        totalSeconds > 0 -> "${totalSeconds}s"
        else -> "0m"
    }
}

@Composable
fun HistoryScreen(viewModel: MainViewModel) {
    val workouts by viewModel.allWorkouts.collectAsState()
    val isDarkMode by viewModel.isDarkMode.collectAsState()
    val completedWorkouts = workouts.filter { it.workout.isCompleted }

    // Aggregate Lifetime Performance Metrics
    val totalWorkouts = completedWorkouts.size
    val totalSets = completedWorkouts.sumOf { it.exercises.sumOf { e -> e.sets.size } }
    val totalReps = completedWorkouts.sumOf { it.exercises.sumOf { e -> e.sets.sumOf { s -> s.reps ?: 0 } } }
    val totalDurationSeconds = completedWorkouts.sumOf {
        it.exercises.sumOf { e -> e.sets.sumOf { s -> s.durationSeconds ?: 0 } }
    }

    val formattedReps = formatCompactNumber(totalReps)
    val formattedSets = formatCompactNumber(totalSets)
    val formattedWorkouts = formatCompactNumber(totalWorkouts)
    val formattedActiveTime = formatDuration(totalDurationSeconds)

    // State for expanding/collapsing timeline beyond top 5
    var isTimelineExpanded by remember { mutableStateOf(false) }
    val displayedWorkouts = if (isTimelineExpanded || completedWorkouts.size <= 5) {
        completedWorkouts
    } else {
        completedWorkouts.take(5)
    }

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
                // Header Title
                item {
                    Text(
                        text = "ANALYTICS & HISTORY",
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Light,
                        letterSpacing = 2.sp,
                        color = MaterialTheme.colorScheme.onBackground
                    )
                }

                // 2x2 Performance Metrics Grid
                item {
                    Column {
                        Text(
                            "PERFORMANCE",
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            letterSpacing = 1.5.sp,
                            fontWeight = FontWeight.Bold
                        )
                        Spacer(modifier = Modifier.height(12.dp))

                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(14.dp)
                        ) {
                            HistoryStatCard(
                                modifier = Modifier.weight(1f),
                                value = formattedWorkouts,
                                label = "Workouts",
                                icon = Icons.Default.FitnessCenter,
                                accentColor = ElectricViolet
                            )
                            HistoryStatCard(
                                modifier = Modifier.weight(1f),
                                value = formattedSets,
                                label = "Sets",
                                icon = Icons.Default.Repeat,
                                accentColor = ElectricCyan
                            )
                        }

                        Spacer(modifier = Modifier.height(14.dp))

                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(14.dp)
                        ) {
                            HistoryStatCard(
                                modifier = Modifier.weight(1f),
                                value = formattedReps,
                                label = "Reps / Volume",
                                icon = Icons.Default.LocalFireDepartment,
                                accentColor = FlameOrange
                            )
                            HistoryStatCard(
                                modifier = Modifier.weight(1f),
                                value = formattedActiveTime,
                                label = "Active Time",
                                icon = Icons.Default.Timer,
                                accentColor = EmeraldGreen
                            )
                        }
                    }
                }

                // Activity Chart
                item {
                    WeeklyActivityChart(workouts = completedWorkouts)
                }

                // Training Focus Distribution
                item {
                    DistributionCard(workouts = completedWorkouts)
                }

                // Timeline Section Header
                item {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(top = 4.dp),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            "TIMELINE",
                            style = MaterialTheme.typography.labelMedium,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            letterSpacing = 1.5.sp,
                            fontWeight = FontWeight.Bold
                        )
                        if (completedWorkouts.size > 5) {
                            Text(
                                if (isTimelineExpanded) "Showing all ${completedWorkouts.size}" else "Showing top 5 of ${completedWorkouts.size}",
                                style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.7f)
                            )
                        }
                    }
                }

                // Paginated Timeline Items
                items(
                    items = displayedWorkouts,
                    key = { it.workout.id }
                ) { workout ->
                    WorkoutHistoryCard(
                        workout = workout,
                        onDelete = { viewModel.deleteWorkout(workout.workout) }
                    )
                }

                // "Show More" / "Show Less" Expand Button
                if (completedWorkouts.size > 5) {
                    item {
                        val borderColor = if (isDarkMode) Color.White.copy(alpha = 0.2f) else MaterialTheme.colorScheme.outline.copy(alpha = 0.3f)

                        OutlinedButton(
                            onClick = { isTimelineExpanded = !isTimelineExpanded },
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(52.dp),
                            shape = RoundedCornerShape(20.dp),
                            border = BorderStroke(1.dp, borderColor),
                            colors = ButtonDefaults.outlinedButtonColors(
                                contentColor = MaterialTheme.colorScheme.primary
                            )
                        ) {
                            Row(
                                verticalAlignment = Alignment.CenterVertically,
                                horizontalArrangement = Arrangement.Center
                            ) {
                                Icon(
                                    imageVector = if (isTimelineExpanded) Icons.Default.KeyboardArrowUp else Icons.Default.KeyboardArrowDown,
                                    contentDescription = null,
                                    tint = MaterialTheme.colorScheme.primary
                                )
                                Spacer(modifier = Modifier.width(8.dp))
                                Text(
                                    text = if (isTimelineExpanded) "Show Less" else "Show All Workouts (${completedWorkouts.size})",
                                    fontWeight = FontWeight.Bold,
                                    letterSpacing = 0.5.sp
                                )
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
fun HistoryStatCard(
    modifier: Modifier = Modifier,
    value: String,
    label: String,
    icon: ImageVector,
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
                    text = label.uppercase(),
                    style = MaterialTheme.typography.labelSmall,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    letterSpacing = 1.2.sp,
                    maxLines = 1,
                    modifier = Modifier.weight(1f)
                )

                Box(
                    modifier = Modifier
                        .size(28.dp)
                        .background(
                            color = accentColor.copy(alpha = 0.15f),
                            shape = CircleShape
                        ),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = icon,
                        contentDescription = null,
                        tint = accentColor,
                        modifier = Modifier.size(15.dp)
                    )
                }
            }

            Spacer(modifier = Modifier.height(10.dp))

            Text(
                text = value,
                style = MaterialTheme.typography.headlineMedium.copy(fontSize = 26.sp),
                fontWeight = FontWeight.Black,
                color = MaterialTheme.colorScheme.onSurface,
                maxLines = 1
            )
        }
    }
}

@Composable
fun WeeklyActivityChart(workouts: List<WorkoutWithExercises>) {
    val daysList = mutableListOf<Pair<String, Int>>()
    val calendar = Calendar.getInstance()
    calendar.time = Date()
    val format = SimpleDateFormat("EEE", Locale.getDefault())

    val startOfDay = Calendar.getInstance().apply {
        set(Calendar.HOUR_OF_DAY, 0)
        set(Calendar.MINUTE, 0)
        set(Calendar.SECOND, 0)
        set(Calendar.MILLISECOND, 0)
    }

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

    GlassCard {
        Column(modifier = Modifier.padding(20.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    "LAST 7 DAYS",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    letterSpacing = 1.5.sp,
                    fontWeight = FontWeight.Bold
                )
                Text(
                    "Volume breakdown",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.7f)
                )
            }

            Spacer(modifier = Modifier.height(18.dp))

            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(115.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.Bottom
            ) {
                daysList.forEach { (day, count) ->
                    val heightRatio = (count.toFloat() / maxSets.toFloat()).coerceIn(0f, 1f)
                    val animatedHeight = if (heightRatio > 0f) heightRatio else 0.08f

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
                                    brush = if (count > 0) Brush.verticalGradient(
                                        listOf(ElectricCyan, ElectricViolet)
                                    ) else Brush.verticalGradient(
                                        listOf(
                                            MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f),
                                            MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.2f)
                                        )
                                    ),
                                    shape = RoundedCornerShape(topStart = 8.dp, topEnd = 8.dp, bottomStart = 3.dp, bottomEnd = 3.dp)
                                )
                        )

                        Spacer(modifier = Modifier.height(8.dp))

                        Text(
                            day,
                            style = MaterialTheme.typography.labelSmall,
                            color = MaterialTheme.colorScheme.onSurfaceVariant,
                            fontWeight = FontWeight.SemiBold
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun DistributionCard(workouts: List<WorkoutWithExercises>) {
    var weightsCount = 0
    var bodyweightCount = 0

    workouts.forEach { w ->
        val isWeights = w.workout.name.contains("Weights", ignoreCase = true)
        val sets = w.exercises.sumOf { it.sets.size }
        if (isWeights) {
            weightsCount += sets
        } else {
            bodyweightCount += sets
        }
    }

    val total = (weightsCount + bodyweightCount).coerceAtLeast(1)
    val weightsPercent = (weightsCount * 100) / total
    val bwPercent = 100 - weightsPercent

    GlassCard {
        Column(modifier = Modifier.padding(20.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    "TRAINING FOCUS",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    letterSpacing = 1.5.sp,
                    fontWeight = FontWeight.Bold
                )
                Box(
                    modifier = Modifier
                        .size(26.dp)
                        .background(ElectricViolet.copy(alpha = 0.15f), CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        Icons.Default.PieChart,
                        contentDescription = null,
                        tint = ElectricViolet,
                        modifier = Modifier.size(15.dp)
                    )
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            // Proportional Multi-Segment Progress Bar
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(12.dp)
                    .clip(RoundedCornerShape(6.dp))
                    .background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.4f))
            ) {
                if (weightsCount > 0) {
                    Box(
                        modifier = Modifier
                            .fillMaxHeight()
                            .weight(weightsPercent.toFloat().coerceAtLeast(1f))
                            .background(Brush.horizontalGradient(listOf(ElectricViolet, Color(0xFF6366F1))))
                    )
                }
                if (bodyweightCount > 0) {
                    Box(
                        modifier = Modifier
                            .fillMaxHeight()
                            .weight(bwPercent.toFloat().coerceAtLeast(1f))
                            .background(Brush.horizontalGradient(listOf(ElectricCyan, EmeraldGreen)))
                    )
                }
            }

            Spacer(modifier = Modifier.height(16.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                // Weights breakdown
                Surface(
                    modifier = Modifier.weight(1f),
                    shape = RoundedCornerShape(14.dp),
                    color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.4f),
                    border = BorderStroke(1.dp, ElectricViolet.copy(alpha = 0.2f))
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 10.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(
                            modifier = Modifier
                                .size(10.dp)
                                .background(ElectricViolet, CircleShape)
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Column {
                            Text(
                                "Weights",
                                style = MaterialTheme.typography.labelSmall,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.onSurface
                            )
                            Text(
                                "$weightsPercent% ($weightsCount sets)",
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                }

                // Bodyweight breakdown
                Surface(
                    modifier = Modifier.weight(1f),
                    shape = RoundedCornerShape(14.dp),
                    color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.4f),
                    border = BorderStroke(1.dp, ElectricCyan.copy(alpha = 0.2f))
                ) {
                    Row(
                        modifier = Modifier.padding(horizontal = 12.dp, vertical = 10.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(
                            modifier = Modifier
                                .size(10.dp)
                                .background(ElectricCyan, CircleShape)
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Column {
                            Text(
                                "Bodyweight",
                                style = MaterialTheme.typography.labelSmall,
                                fontWeight = FontWeight.Bold,
                                color = MaterialTheme.colorScheme.onSurface
                            )
                            Text(
                                "$bwPercent% ($bodyweightCount sets)",
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant
                            )
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun WorkoutHistoryCard(
    workout: WorkoutWithExercises,
    onDelete: () -> Unit
) {
    var expanded by remember { mutableStateOf(false) }
    val fullDateFormat = remember { SimpleDateFormat("MMMM d, yyyy · h:mm a", Locale.getDefault()) }
    val dateBadgeFormat = remember { SimpleDateFormat("MMM d", Locale.getDefault()) }

    val isWeights = workout.workout.name.contains("Weights", ignoreCase = true)
    val totalSets = workout.exercises.sumOf { it.sets.size }
    val totalReps = workout.exercises.sumOf { it.sets.sumOf { s -> s.reps ?: 0 } }
    val workoutDurationSeconds = workout.exercises.sumOf {
        it.sets.sumOf { s -> s.durationSeconds ?: 0 }
    }

    GlassCard(
        modifier = Modifier
            .fillMaxWidth()
            .clickable { expanded = !expanded }
            .animateContentSize()
    ) {
        Column(modifier = Modifier.padding(18.dp)) {
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
                            .size(44.dp)
                            .background(
                                if (isWeights) ElectricViolet.copy(alpha = 0.15f) else EmeraldGreen.copy(alpha = 0.15f),
                                CircleShape
                            ),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            imageVector = if (isWeights) Icons.Default.FitnessCenter else Icons.Default.Person,
                            contentDescription = null,
                            tint = if (isWeights) ElectricViolet else EmeraldGreen,
                            modifier = Modifier.size(22.dp)
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
                    color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
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
                        color = ElectricCyan.copy(alpha = 0.15f)
                    ) {
                        Text(
                            text = "⏱ $durBadgeText",
                            style = MaterialTheme.typography.labelSmall,
                            fontWeight = FontWeight.Bold,
                            color = ElectricCyan,
                            modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp)
                        )
                    }
                }

                // 3. Exercise & Sets Badge
                Surface(
                    shape = RoundedCornerShape(10.dp),
                    color = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
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
                Spacer(modifier = Modifier.height(16.dp))
                HorizontalDivider(color = MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.3f))
                Spacer(modifier = Modifier.height(12.dp))

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
                    Spacer(modifier = Modifier.height(10.dp))
                }

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.End
                ) {
                    TextButton(
                        onClick = onDelete,
                        colors = ButtonDefaults.textButtonColors(contentColor = MaterialTheme.colorScheme.error)
                    ) {
                        Icon(Icons.Default.Delete, contentDescription = null, modifier = Modifier.size(16.dp))
                        Spacer(modifier = Modifier.width(6.dp))
                        Text("Delete Workout", fontWeight = FontWeight.Bold)
                    }
                }
            }
        }
    }
}
