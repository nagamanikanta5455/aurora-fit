package com.example.ui.workout

import android.media.RingtoneManager
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.ChevronRight
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.DirectionsRun
import androidx.compose.material.icons.filled.FitnessCenter
import androidx.compose.material.icons.filled.Timer
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import androidx.navigation.NavGraph.Companion.findStartDestination
import com.example.data.model.ExerciseType
import com.example.data.model.ExerciseWithSets
import com.example.data.model.SetLog
import com.example.ui.MainViewModel
import com.example.ui.components.GlassCard
import com.example.ui.theme.DarkMeshBackgroundGradient
import com.example.ui.theme.ElectricCyan
import com.example.ui.theme.ElectricViolet
import com.example.ui.theme.EmeraldGreen
import com.example.ui.theme.LightMeshBackgroundGradient

@Composable
fun WorkoutScreen(viewModel: MainViewModel, navController: NavController) {
    val activeWorkout by viewModel.activeWorkout.collectAsState()
    val isDarkMode by viewModel.isDarkMode.collectAsState()
    val activeWorkoutDetails by viewModel.activeWorkoutDetails.collectAsState()
    val previousSessions by viewModel.previousSessions.collectAsState()
    val haptic = LocalHapticFeedback.current
    val context = LocalContext.current

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
            if (activeWorkout == null) {
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(24.dp),
                    verticalArrangement = Arrangement.Center,
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text(
                        "START SESSION",
                        style = MaterialTheme.typography.titleMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        letterSpacing = 1.5.sp,
                        fontWeight = FontWeight.SemiBold
                    )
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        "TRAINING FOCUS",
                        style = MaterialTheme.typography.headlineLarge,
                        fontWeight = FontWeight.Light,
                        color = MaterialTheme.colorScheme.onBackground
                    )
                    Spacer(modifier = Modifier.height(36.dp))

                    WorkoutTypeSelectionCard(
                        title = "WEIGHTS",
                        subtitle = "Free weights, barbells & machines",
                        icon = Icons.Default.FitnessCenter,
                        gradient = Brush.horizontalGradient(listOf(ElectricViolet, Color(0xFF6366F1))),
                        accentColor = ElectricViolet,
                        onClick = { viewModel.startNewWorkout(isWeights = true) }
                    )

                    Spacer(modifier = Modifier.height(16.dp))

                    WorkoutTypeSelectionCard(
                        title = "BODYWEIGHT",
                        subtitle = "Calisthenics, core & timed holds",
                        icon = Icons.Default.DirectionsRun,
                        gradient = Brush.horizontalGradient(listOf(ElectricCyan, EmeraldGreen)),
                        accentColor = ElectricCyan,
                        onClick = { viewModel.startNewWorkout(isWeights = false) }
                    )
                }
            } else {
                val details = activeWorkoutDetails
                if (details == null) {
                    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                        CircularProgressIndicator(color = MaterialTheme.colorScheme.primary)
                    }
                } else {
                    var showAddExercise by remember { mutableStateOf(false) }

                    LazyColumn(
                        modifier = Modifier.fillMaxSize(),
                        contentPadding = PaddingValues(start = 16.dp, end = 16.dp, top = 20.dp, bottom = 100.dp),
                        verticalArrangement = Arrangement.spacedBy(20.dp)
                    ) {
                        item {
                            Box(
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .padding(horizontal = 4.dp)
                            ) {
                                Column(
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .padding(end = 48.dp)
                                ) {
                                    Text(
                                        "ACTIVE WORKOUT",
                                        style = MaterialTheme.typography.labelSmall,
                                        color = MaterialTheme.colorScheme.primary,
                                        letterSpacing = 1.5.sp,
                                        fontWeight = FontWeight.Bold
                                    )
                                    Spacer(modifier = Modifier.height(4.dp))
                                    Text(
                                        text = details.workout.name.uppercase().replace(" WORKOUT", "").replace("WORKOUT", "").trim(),
                                        style = MaterialTheme.typography.headlineMedium,
                                        fontWeight = FontWeight.Bold,
                                        color = MaterialTheme.colorScheme.onBackground
                                    )
                                }

                                IconButton(
                                    onClick = {
                                        haptic.performHapticFeedback(HapticFeedbackType.LongPress)
                                        try {
                                            viewModel.cancelWorkout(details.workout)
                                            navController.navigate("home") {
                                                popUpTo(navController.graph.startDestinationId)
                                                launchSingleTop = true
                                            }
                                        } catch (e: Exception) {
                                            e.printStackTrace()
                                        }
                                    },
                                    modifier = Modifier.align(Alignment.CenterEnd)
                                ) {
                                    Icon(
                                        Icons.Default.Close,
                                        contentDescription = "Cancel Workout",
                                        tint = MaterialTheme.colorScheme.error
                                    )
                                }
                            }
                        }

                        items(
                            items = details.exercises,
                            key = { it.exercise.id }
                        ) { exerciseWithSets ->
                            val prevSession = previousSessions[exerciseWithSets.exercise.id]
                            ExerciseCard(
                                exerciseWithSets = exerciseWithSets,
                                prevSession = prevSession,
                                viewModel = viewModel
                            )
                        }

                        item {
                            val borderColor = if (isDarkMode) Color.White.copy(alpha = 0.2f) else MaterialTheme.colorScheme.outline.copy(alpha = 0.3f)

                            OutlinedButton(
                                onClick = {
                                    haptic.performHapticFeedback(HapticFeedbackType.LongPress)
                                    showAddExercise = true
                                },
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(56.dp),
                                shape = RoundedCornerShape(20.dp),
                                border = BorderStroke(1.dp, borderColor),
                                colors = ButtonDefaults.outlinedButtonColors(
                                    contentColor = MaterialTheme.colorScheme.primary
                                )
                            ) {
                                Icon(Icons.Default.Add, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                                Spacer(Modifier.width(8.dp))
                                Text(
                                    "ADD EXERCISE",
                                    color = MaterialTheme.colorScheme.primary,
                                    fontWeight = FontWeight.Bold,
                                    letterSpacing = 1.sp
                                )
                            }

                            Spacer(modifier = Modifier.height(16.dp))

                            Button(
                                onClick = {
                                    try {
                                        val uri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION)
                                        RingtoneManager.getRingtone(context, uri).play()
                                    } catch (e: Exception) {
                                        e.printStackTrace()
                                    }
                                    try {
                                        viewModel.finishWorkout(details.workout)
                                        navController.navigate("home") {
                                            popUpTo(navController.graph.findStartDestination().id) {
                                                saveState = true
                                            }
                                            launchSingleTop = true
                                            restoreState = true
                                        }
                                    } catch (e: Exception) {
                                        e.printStackTrace()
                                    }
                                },
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .height(56.dp)
                                    .shadow(
                                        elevation = 12.dp,
                                        shape = RoundedCornerShape(20.dp),
                                        spotColor = ElectricViolet.copy(alpha = 0.4f)
                                    ),
                                colors = ButtonDefaults.buttonColors(
                                    containerColor = ElectricViolet,
                                    contentColor = Color.White
                                ),
                                shape = RoundedCornerShape(20.dp)
                            ) {
                                Icon(Icons.Default.Check, contentDescription = null, tint = Color.White)
                                Spacer(Modifier.width(8.dp))
                                Text("FINISH WORKOUT", fontWeight = FontWeight.ExtraBold, letterSpacing = 1.2.sp)
                            }
                        }

                        item {
                            Spacer(modifier = Modifier.height(100.dp))
                        }
                    }

                    if (showAddExercise) {
                        var newExerciseName by remember { mutableStateOf("") }
                        val isWeights = details.workout.name.contains("Weights")
                        var selectedType by remember { mutableStateOf(if (isWeights) ExerciseType.WEIGHTED else ExerciseType.BODYWEIGHT) }

                        AlertDialog(
                            onDismissRequest = { showAddExercise = false },
                            shape = RoundedCornerShape(24.dp),
                            title = { Text("Add Exercise", style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold) },
                            text = {
                                Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                                    OutlinedTextField(
                                        value = newExerciseName,
                                        onValueChange = { newExerciseName = it },
                                        label = { Text("Exercise Name") },
                                        singleLine = true,
                                        modifier = Modifier.fillMaxWidth(),
                                        shape = RoundedCornerShape(16.dp)
                                    )

                                    Text(
                                        "CATEGORY",
                                        style = MaterialTheme.typography.labelSmall,
                                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                                        letterSpacing = 1.sp,
                                        fontWeight = FontWeight.Bold
                                    )

                                    Row(
                                        modifier = Modifier.fillMaxWidth(),
                                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                                    ) {
                                        if (isWeights) {
                                            TypeSelectPill(
                                                selected = selectedType == ExerciseType.WEIGHTED,
                                                label = "Weights",
                                                icon = Icons.Default.FitnessCenter,
                                                onClick = { selectedType = ExerciseType.WEIGHTED },
                                                modifier = Modifier.weight(1f)
                                            )
                                            TypeSelectPill(
                                                selected = selectedType == ExerciseType.WEIGHTED_BODYWEIGHT,
                                                label = "Weighted BW",
                                                icon = Icons.Default.Add,
                                                onClick = { selectedType = ExerciseType.WEIGHTED_BODYWEIGHT },
                                                modifier = Modifier.weight(1f)
                                            )
                                        } else {
                                            TypeSelectPill(
                                                selected = selectedType == ExerciseType.BODYWEIGHT,
                                                label = "Bodyweight",
                                                icon = Icons.Default.DirectionsRun,
                                                onClick = { selectedType = ExerciseType.BODYWEIGHT },
                                                modifier = Modifier.weight(1f)
                                            )
                                            TypeSelectPill(
                                                selected = selectedType == ExerciseType.TIMED,
                                                label = "Timed",
                                                icon = Icons.Default.Timer,
                                                onClick = { selectedType = ExerciseType.TIMED },
                                                modifier = Modifier.weight(1f)
                                            )
                                        }
                                    }
                                }
                            },
                            confirmButton = {
                                Button(
                                    onClick = {
                                        if (newExerciseName.isNotBlank()) {
                                            viewModel.addExerciseToActive(newExerciseName.trim(), selectedType)
                                            showAddExercise = false
                                        }
                                    },
                                    colors = ButtonDefaults.buttonColors(
                                        containerColor = ElectricViolet,
                                        contentColor = Color.White
                                    ),
                                    shape = RoundedCornerShape(14.dp)
                                ) { Text("Add", fontWeight = FontWeight.Bold) }
                            },
                            dismissButton = {
                                TextButton(onClick = { showAddExercise = false }) { Text("Cancel") }
                            }
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun WorkoutTypeSelectionCard(
    title: String,
    subtitle: String,
    icon: ImageVector,
    gradient: Brush,
    accentColor: Color,
    onClick: () -> Unit
) {
    val haptic = LocalHapticFeedback.current

    GlassCard(
        modifier = Modifier
            .fillMaxWidth()
            .clickable {
                haptic.performHapticFeedback(HapticFeedbackType.LongPress)
                onClick()
            }
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(20.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(52.dp)
                    .background(gradient, RoundedCornerShape(16.dp)),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = icon,
                    contentDescription = null,
                    tint = Color.White,
                    modifier = Modifier.size(26.dp)
                )
            }

            Spacer(modifier = Modifier.width(16.dp))

            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = title,
                    style = MaterialTheme.typography.titleLarge,
                    fontWeight = FontWeight.ExtraBold,
                    color = MaterialTheme.colorScheme.onSurface,
                    letterSpacing = 1.sp
                )
                Spacer(modifier = Modifier.height(2.dp))
                Text(
                    text = subtitle,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant
                )
            }

            Icon(
                Icons.Default.ChevronRight,
                contentDescription = null,
                tint = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f),
                modifier = Modifier.size(24.dp)
            )
        }
    }
}

@Composable
fun TypeSelectPill(
    selected: Boolean,
    label: String,
    icon: ImageVector,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val isDark = isSystemInDarkTheme()
    val bgColor = if (selected) {
        ElectricViolet.copy(alpha = 0.2f)
    } else {
        if (isDark) Color(0x1F1E293B) else Color(0xFFF1F5F9)
    }
    val borderColor = if (selected) ElectricViolet else Color.Transparent

    Surface(
        modifier = modifier
            .clip(RoundedCornerShape(14.dp))
            .clickable { onClick() },
        shape = RoundedCornerShape(14.dp),
        color = bgColor,
        border = BorderStroke(1.dp, borderColor)
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 10.dp, vertical = 10.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.Center
        ) {
            Icon(
                imageVector = icon,
                contentDescription = null,
                tint = if (selected) ElectricViolet else MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.size(16.dp)
            )
            Spacer(modifier = Modifier.width(6.dp))
            Text(
                text = label,
                fontSize = 12.sp,
                fontWeight = if (selected) FontWeight.Bold else FontWeight.Medium,
                color = if (selected) ElectricViolet else MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}

@Composable
fun ExerciseCard(
    exerciseWithSets: ExerciseWithSets,
    prevSession: ExerciseWithSets?,
    viewModel: MainViewModel
) {
    val haptic = LocalHapticFeedback.current

    GlassCard(modifier = Modifier.fillMaxWidth()) {
        Column(modifier = Modifier.padding(18.dp)) {
            // Exercise Header
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = exerciseWithSets.exercise.name,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.onSurface
                    )
                    Spacer(modifier = Modifier.height(2.dp))
                    Text(
                        text = when (exerciseWithSets.exercise.type) {
                            ExerciseType.WEIGHTED -> "WEIGHTS (KG × REPS)"
                            ExerciseType.WEIGHTED_BODYWEIGHT -> "WEIGHTED BW (+KG × REPS)"
                            ExerciseType.BODYWEIGHT -> "BODYWEIGHT (REPS)"
                            ExerciseType.TIMED -> "TIMED (SECONDS)"
                        },
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                        letterSpacing = 0.5.sp
                    )
                }

                IconButton(
                    onClick = {
                        haptic.performHapticFeedback(HapticFeedbackType.LongPress)
                        viewModel.deleteExercise(exerciseWithSets.exercise)
                    }
                ) {
                    Icon(
                        Icons.Default.Delete,
                        contentDescription = "Delete Exercise",
                        tint = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.6f),
                        modifier = Modifier.size(20.dp)
                    )
                }
            }

            // Previous Session ghost hint
            if (prevSession != null && prevSession.sets.isNotEmpty()) {
                val lastSummary = prevSession.sets.joinToString(", ") { s ->
                    when (prevSession.exercise.type) {
                        ExerciseType.WEIGHTED, ExerciseType.WEIGHTED_BODYWEIGHT -> "${s.weight?.toInt() ?: 0}×${s.reps ?: 0}"
                        ExerciseType.BODYWEIGHT -> "${s.reps ?: 0}r"
                        ExerciseType.TIMED -> "${s.durationSeconds ?: 0}s"
                    }
                }
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = "Previous: $lastSummary",
                    style = MaterialTheme.typography.bodySmall,
                    color = ElectricCyan,
                    fontWeight = FontWeight.Medium
                )
            }

            Spacer(modifier = Modifier.height(14.dp))

            // Column Headers
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(horizontal = 4.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    "SET",
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.width(36.dp),
                    textAlign = TextAlign.Center
                )
                Spacer(Modifier.width(8.dp))
                Text(
                    when (exerciseWithSets.exercise.type) {
                        ExerciseType.WEIGHTED, ExerciseType.WEIGHTED_BODYWEIGHT -> "KG & REPS"
                        ExerciseType.BODYWEIGHT -> "REPS"
                        ExerciseType.TIMED -> "DURATION"
                    },
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.weight(1f),
                    textAlign = TextAlign.Center
                )
                Spacer(Modifier.width(8.dp))
                Text(
                    "LOG",
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.width(50.dp),
                    textAlign = TextAlign.Center
                )
            }

            Spacer(modifier = Modifier.height(8.dp))

            // Sets List
            exerciseWithSets.sets.forEachIndexed { index, setLog ->
                SetRow(
                    setLog = setLog,
                    setNumber = index + 1,
                    exerciseType = exerciseWithSets.exercise.type,
                    onUpdate = { viewModel.updateSetLog(it) },
                    onDelete = { viewModel.deleteSetLog(setLog) }
                )
                Spacer(modifier = Modifier.height(8.dp))
            }

            Spacer(modifier = Modifier.height(8.dp))

            // Add Set Button
            TextButton(
                onClick = {
                    haptic.performHapticFeedback(HapticFeedbackType.LongPress)
                    viewModel.addSetLog(exerciseWithSets.exercise.id, exerciseWithSets.sets.size + 1)
                },
                modifier = Modifier.align(Alignment.CenterHorizontally),
                colors = ButtonDefaults.textButtonColors(contentColor = MaterialTheme.colorScheme.primary)
            ) {
                Icon(Icons.Default.Add, contentDescription = null, modifier = Modifier.size(18.dp))
                Spacer(Modifier.width(4.dp))
                Text("ADD SET", fontWeight = FontWeight.Bold, letterSpacing = 0.5.sp)
            }
        }
    }
}

@Composable
fun SetRow(
    setLog: SetLog,
    setNumber: Int,
    exerciseType: ExerciseType,
    onUpdate: (SetLog) -> Unit,
    onDelete: () -> Unit
) {
    var weightText by remember(setLog.weight) { mutableStateOf(setLog.weight?.toString()?.replace(".0", "") ?: "") }
    var repsText by remember(setLog.reps) { mutableStateOf(setLog.reps?.toString() ?: "") }
    var timeText by remember(setLog.durationSeconds) { mutableStateOf(setLog.durationSeconds?.toString() ?: "") }
    val haptic = LocalHapticFeedback.current
    val context = LocalContext.current

    Row(
        modifier = Modifier.fillMaxWidth(),
        verticalAlignment = Alignment.CenterVertically
    ) {
        // Set Number Badge
        Box(
            modifier = Modifier
                .size(36.dp)
                .background(
                    if (setLog.isCompleted) EmeraldGreen.copy(alpha = 0.15f)
                    else MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.4f),
                    CircleShape
                ),
            contentAlignment = Alignment.Center
        ) {
            Text(
                text = setNumber.toString(),
                style = MaterialTheme.typography.labelMedium,
                fontWeight = FontWeight.Bold,
                color = if (setLog.isCompleted) EmeraldGreen else MaterialTheme.colorScheme.onSurface
            )
        }

        Spacer(Modifier.width(8.dp))

        if (exerciseType == ExerciseType.WEIGHTED || exerciseType == ExerciseType.WEIGHTED_BODYWEIGHT) {
            SetInputField(
                value = weightText,
                unit = "kg",
                placeholder = "0",
                onValueChange = {
                    weightText = it
                    it.toFloatOrNull()?.let { weight -> onUpdate(setLog.copy(weight = weight)) }
                },
                modifier = Modifier.weight(1f)
            )
            Text(
                " × ",
                color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.6f),
                fontWeight = FontWeight.Bold,
                fontSize = 16.sp
            )
            SetInputField(
                value = repsText,
                unit = "reps",
                placeholder = "0",
                onValueChange = {
                    repsText = it
                    it.toIntOrNull()?.let { reps -> onUpdate(setLog.copy(reps = reps)) }
                },
                modifier = Modifier.weight(1f)
            )
        } else if (exerciseType == ExerciseType.BODYWEIGHT) {
            SetInputField(
                value = repsText,
                unit = "reps",
                placeholder = "0",
                onValueChange = {
                    repsText = it
                    it.toIntOrNull()?.let { reps -> onUpdate(setLog.copy(reps = reps)) }
                },
                modifier = Modifier.weight(1f)
            )
            Spacer(modifier = Modifier.weight(1f))
        } else {
            SetInputField(
                value = timeText,
                unit = "sec",
                placeholder = "0",
                onValueChange = {
                    timeText = it
                    it.toIntOrNull()?.let { time -> onUpdate(setLog.copy(durationSeconds = time)) }
                },
                modifier = Modifier.weight(1f)
            )
            Spacer(modifier = Modifier.weight(1f))
        }

        Spacer(Modifier.width(8.dp))

        // Checkmark / Log Action Button
        if (setLog.isCompleted) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Box(
                    modifier = Modifier
                        .size(34.dp)
                        .background(EmeraldGreen, CircleShape)
                        .clickable {
                            haptic.performHapticFeedback(HapticFeedbackType.LongPress)
                            onUpdate(setLog.copy(isCompleted = false))
                        },
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        Icons.Default.Check,
                        contentDescription = "Completed (tap to undo)",
                        tint = Color.White,
                        modifier = Modifier.size(18.dp)
                    )
                }

                IconButton(
                    onClick = {
                        haptic.performHapticFeedback(HapticFeedbackType.LongPress)
                        onDelete()
                    },
                    modifier = Modifier
                        .size(32.dp)
                        .padding(start = 2.dp)
                ) {
                    Icon(
                        Icons.Default.Delete,
                        contentDescription = "Delete Set",
                        tint = MaterialTheme.colorScheme.error.copy(alpha = 0.7f),
                        modifier = Modifier.size(16.dp)
                    )
                }
            }
        } else {
            Box(
                modifier = Modifier
                    .height(36.dp)
                    .width(46.dp)
                    .background(
                        brush = Brush.horizontalGradient(listOf(ElectricViolet, Color(0xFF6366F1))),
                        shape = RoundedCornerShape(12.dp)
                    )
                    .clickable {
                        haptic.performHapticFeedback(HapticFeedbackType.LongPress)
                        try {
                            val uri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION)
                            RingtoneManager.getRingtone(context, uri).play()
                        } catch (e: Exception) {
                            e.printStackTrace()
                        }
                        onUpdate(setLog.copy(isCompleted = true))
                    },
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    Icons.Default.Check,
                    contentDescription = "Log Set",
                    tint = Color.White,
                    modifier = Modifier.size(18.dp)
                )
            }
        }
    }
}

@Composable
fun SetInputField(
    value: String,
    unit: String,
    placeholder: String,
    onValueChange: (String) -> Unit,
    modifier: Modifier = Modifier
) {
    var isFocused by remember { mutableStateOf(false) }
    val focusManager = LocalFocusManager.current
    val containerBg = MaterialTheme.colorScheme.surfaceVariant
    val borderColor = if (isFocused) {
        MaterialTheme.colorScheme.primary
    } else {
        MaterialTheme.colorScheme.outlineVariant.copy(alpha = 0.5f)
    }

    Box(
        modifier = modifier
            .height(44.dp)
            .background(containerBg, RoundedCornerShape(12.dp))
            .border(BorderStroke(1.dp, borderColor), RoundedCornerShape(12.dp))
            .padding(horizontal = 8.dp),
        contentAlignment = Alignment.Center
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.Center,
            modifier = Modifier.fillMaxWidth()
        ) {
            Box(
                contentAlignment = Alignment.Center,
                modifier = Modifier.weight(1f, fill = false)
            ) {
                if (value.isEmpty()) {
                    Text(
                        placeholder,
                        color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.6f),
                        fontSize = 16.sp,
                        fontWeight = FontWeight.Bold,
                        textAlign = TextAlign.Center
                    )
                }
                BasicTextField(
                    value = value,
                    onValueChange = onValueChange,
                    modifier = Modifier
                        .fillMaxWidth()
                        .onFocusChanged { isFocused = it.isFocused },
                    textStyle = TextStyle(
                        color = MaterialTheme.colorScheme.onSurface,
                        fontSize = 16.sp,
                        textAlign = TextAlign.Center,
                        fontWeight = FontWeight.Bold
                    ),
                    singleLine = true,
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number, imeAction = ImeAction.Done),
                    keyboardActions = KeyboardActions(onDone = { focusManager.clearFocus() }),
                    cursorBrush = SolidColor(MaterialTheme.colorScheme.primary)
                )
            }

            if (value.isNotEmpty() && unit.isNotEmpty()) {
                Text(
                    text = unit,
                    fontSize = 11.sp,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    fontWeight = FontWeight.SemiBold,
                    modifier = Modifier.padding(start = 2.dp)
                )
            }
        }
    }
}
