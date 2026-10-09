content = """package com.example.ui.workout

import android.media.RingtoneManager
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Check
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import com.example.data.model.ExerciseType
import com.example.data.model.SetLog
import com.example.data.model.ExerciseWithSets
import com.example.ui.MainViewModel

@Composable
fun WorkoutScreen(viewModel: MainViewModel, navController: NavController, paddingValues: PaddingValues) {
    val activeWorkout by viewModel.activeWorkout.collectAsState()
    val activeWorkoutDetails by viewModel.activeWorkoutDetails.collectAsState()
    val previousSessions by viewModel.previousSessions.collectAsState()
    
    val haptic = LocalHapticFeedback.current
    val context = LocalContext.current

    Surface(
        modifier = Modifier.fillMaxSize().padding(paddingValues),
        color = Color(0xFFF8FAFC)
    ) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(
                    brush = Brush.linearGradient(
                    colors = listOf(
                        Color(0xFFF8FAFC),
                        MaterialTheme.colorScheme.tertiary.copy(alpha = 0.5f)
                    )
                )
            )
        ) {
        if (activeWorkout == null) {
            Column(
                modifier = Modifier.fillMaxSize().padding(24.dp),
                verticalArrangement = Arrangement.Center,
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Text("HOW ARE YOU", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.onSurfaceVariant, letterSpacing = 2.sp)
                Text("TRAINING TODAY?", style = MaterialTheme.typography.headlineLarge, fontWeight = FontWeight.Light, color = MaterialTheme.colorScheme.onBackground)
                Spacer(modifier = Modifier.height(48.dp))
                
                Card(
                    modifier = Modifier.fillMaxWidth().height(120.dp).clickable { viewModel.startNewWorkout(isWeights = true) }.shadow(16.dp, RoundedCornerShape(24.dp), spotColor = Color(0x1A000000)),
                    shape = RoundedCornerShape(24.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
                ) {
                    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                        Text("WEIGHTS", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.primary, letterSpacing = 2.sp)
                    }
                }
                Spacer(modifier = Modifier.height(24.dp))
                Card(
                    modifier = Modifier.fillMaxWidth().height(120.dp).clickable { viewModel.startNewWorkout(isWeights = false) }.shadow(16.dp, RoundedCornerShape(24.dp), spotColor = Color(0x1A000000)),
                    shape = RoundedCornerShape(24.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
                ) {
                    Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                        Text("BODYWEIGHT", style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.secondary, letterSpacing = 2.sp)
                    }
                }
            }
        } else {
            val details = activeWorkoutDetails
            if (details == null) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    androidx.compose.material3.CircularProgressIndicator()
                }
            } else {
                var showAddExercise by remember { mutableStateOf(false) }

                LazyColumn(
                    modifier = Modifier.fillMaxSize(),
                    contentPadding = PaddingValues(start = 16.dp, end = 16.dp, top = 24.dp, bottom = 120.dp),
                    verticalArrangement = Arrangement.spacedBy(24.dp)
                ) {
                item {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column {
                            Text("TODAY", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant, letterSpacing = 1.sp)
                            Text(details.workout.name.uppercase(), style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
                        }
                        IconButton(onClick = {
                            haptic.performHapticFeedback(HapticFeedbackType.LongPress)
                            viewModel.cancelWorkout(details.workout)
                            navController.navigate("home")
                        }) {
                            Icon(Icons.Default.Close, contentDescription = "Cancel Workout", tint = MaterialTheme.colorScheme.error)
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
                    OutlinedButton(
                        onClick = { 
                            haptic.performHapticFeedback(HapticFeedbackType.LongPress)
                            showAddExercise = true 
                        },
                        modifier = Modifier.fillMaxWidth().height(64.dp),
                        shape = RoundedCornerShape(24.dp),
                        colors = ButtonDefaults.outlinedButtonColors(
                            containerColor = Color.White,
                            contentColor = Color(0xFF4F46E5)
                        )
                    ) {
                        Icon(Icons.Default.Add, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
                        Spacer(Modifier.width(8.dp))
                        Text("ADD EXERCISE", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, letterSpacing = 1.sp)
                    }
                    Spacer(modifier = Modifier.height(24.dp))
                    Button(
                        onClick = {
                            try {
                                val uri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION)
                                RingtoneManager.getRingtone(context, uri).play()
                            } catch (e: Exception) { e.printStackTrace() }
                            viewModel.finishWorkout(details.workout)
                            navController.navigate("home")
                        },
                        modifier = Modifier.fillMaxWidth().height(64.dp),
                        colors = ButtonDefaults.buttonColors(
                            containerColor = Color(0xFF4F46E5),
                            contentColor = Color.White
                        ),
                        shape = RoundedCornerShape(24.dp)
                    ) {
                        Text("FINISH WORKOUT", fontWeight = FontWeight.Bold, letterSpacing = 1.sp)
                    }
                }
            }
            
            if (showAddExercise) {
                var newExerciseName by remember { mutableStateOf("") }
                val isWeights = details.workout.name.contains("Weights")
                var selectedType by remember { mutableStateOf(if (isWeights) ExerciseType.WEIGHTED else ExerciseType.BODYWEIGHT) }

                AlertDialog(
                    onDismissRequest = { showAddExercise = false },
                    title = { Text("Add Exercise", style = MaterialTheme.typography.titleLarge) },
                    text = {
                        Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                            OutlinedTextField(
                                value = newExerciseName,
                                onValueChange = { newExerciseName = it },
                                label = { Text("Exercise Name") },
                                singleLine = true,
                                modifier = Modifier.fillMaxWidth()
                            )
                            
                            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                                if (isWeights) {
                                    FilterChip(
                                        selected = selectedType == ExerciseType.WEIGHTED,
                                        onClick = { selectedType = ExerciseType.WEIGHTED },
                                        label = { Text("Weights") }
                                    )
                                    FilterChip(
                                        selected = selectedType == ExerciseType.WEIGHTED_BODYWEIGHT,
                                        onClick = { selectedType = ExerciseType.WEIGHTED_BODYWEIGHT },
                                        label = { Text("Weighted BW") }
                                    )
                                } else {
                                    FilterChip(
                                        selected = selectedType == ExerciseType.BODYWEIGHT,
                                        onClick = { selectedType = ExerciseType.BODYWEIGHT },
                                        label = { Text("Bodyweight") }
                                    )
                                    FilterChip(
                                        selected = selectedType == ExerciseType.TIMED,
                                        onClick = { selectedType = ExerciseType.TIMED },
                                        label = { Text("Timed") }
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
                                containerColor = Color(0xFF4F46E5),
                                contentColor = Color.White
                            )
                        ) { Text("Add") }
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
fun ExerciseCard(exerciseWithSets: ExerciseWithSets, prevSession: ExerciseWithSets?, viewModel: MainViewModel) {
    val haptic = LocalHapticFeedback.current

    Card(
        colors = CardDefaults.cardColors(containerColor = Color.White),
        modifier = Modifier.fillMaxWidth().shadow(12.dp, RoundedCornerShape(24.dp), spotColor = Color(0x0A000000)),
        shape = RoundedCornerShape(24.dp)
    ) {
        Column(modifier = Modifier.padding(20.dp)) {
            var showEditDialog by remember { mutableStateOf(false) }
            
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text(exerciseWithSets.exercise.name.uppercase(), color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, letterSpacing = 1.sp, modifier = Modifier.weight(1f))
                Row {
                    IconButton(onClick = { 
                        haptic.performHapticFeedback(HapticFeedbackType.LongPress)
                        showEditDialog = true 
                    }) {
                        Icon(Icons.Default.Edit, contentDescription = "Edit Exercise", tint = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    IconButton(onClick = { 
                        haptic.performHapticFeedback(HapticFeedbackType.LongPress)
                        viewModel.deleteExercise(exerciseWithSets.exercise) 
                    }) {
                        Icon(Icons.Default.Delete, contentDescription = "Delete Exercise", tint = MaterialTheme.colorScheme.error)
                    }
                }
            }
            
            if (showEditDialog) {
                var editName by remember { mutableStateOf(exerciseWithSets.exercise.name) }
                AlertDialog(
                    onDismissRequest = { showEditDialog = false },
                    title = { Text("Edit Exercise", style = MaterialTheme.typography.titleLarge) },
                    text = {
                        OutlinedTextField(
                            value = editName,
                            onValueChange = { editName = it },
                            label = { Text("Exercise Name") },
                            singleLine = true,
                            modifier = Modifier.fillMaxWidth()
                        )
                    },
                    confirmButton = {
                        Button(
                            onClick = { 
                                if (editName.isNotBlank()) {
                                    viewModel.updateExercise(exerciseWithSets.exercise.copy(name = editName.trim()))
                                    showEditDialog = false
                                }
                            },
                            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF4F46E5), contentColor = Color.White)
                        ) { Text("Save") }
                    },
                    dismissButton = {
                        TextButton(onClick = { showEditDialog = false }) { Text("Cancel") }
                    }
                )
            }
            Spacer(modifier = Modifier.height(16.dp))
            
            if (prevSession != null && prevSession.sets.isNotEmpty()) {
                Box(
                    modifier = Modifier.fillMaxWidth().background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f), RoundedCornerShape(16.dp)).padding(16.dp)
                ) {
                    Column {
                        Text("LAST TIME", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant, letterSpacing = 1.sp)
                        Spacer(modifier = Modifier.height(8.dp))
                        prevSession.sets.forEach { s ->
                            val text = when (exerciseWithSets.exercise.type) {
                                ExerciseType.WEIGHTED, ExerciseType.WEIGHTED_BODYWEIGHT -> "${s.weight?.toInt() ?: 0} kg × ${s.reps ?: 0}"
                                ExerciseType.BODYWEIGHT -> "${s.reps ?: 0} reps"
                                ExerciseType.TIMED -> "${s.durationSeconds ?: 0} sec"
                            }
                            Text(text, style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurface)
                        }
                    }
                }
                Spacer(modifier = Modifier.height(16.dp))
            }

            Text("TODAY", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant, letterSpacing = 1.sp)
            Spacer(modifier = Modifier.height(8.dp))
            
            exerciseWithSets.sets.forEach { setLog ->
                SetRow(
                    setLog = setLog,
                    exerciseType = exerciseWithSets.exercise.type,
                    onUpdate = { updatedSet -> viewModel.updateSetLog(updatedSet) },
                    onDelete = { viewModel.deleteSetLog(setLog) }
                )
            }
            
            Spacer(modifier = Modifier.height(12.dp))
            TextButton(
                onClick = { viewModel.addSetLog(exerciseWithSets.exercise.id, exerciseWithSets.sets.size + 1) },
                modifier = Modifier.fillMaxWidth()
            ) {
                Icon(Icons.Default.Add, contentDescription = null)
                Spacer(Modifier.width(8.dp))
                Text("ADD SET", fontWeight = FontWeight.Bold)
            }
        }
    }
}

@Composable
fun SetRow(setLog: SetLog, exerciseType: ExerciseType, onUpdate: (SetLog) -> Unit, onDelete: () -> Unit) {
    val haptic = LocalHapticFeedback.current
    val context = LocalContext.current

    var weightText by remember(setLog.id) { mutableStateOf(setLog.weight?.let { if (it % 1 == 0f) it.toInt().toString() else it.toString() } ?: "") }
    var repsText by remember(setLog.id) { mutableStateOf(setLog.reps?.toString() ?: "") }
    var timeText by remember(setLog.id) { mutableStateOf(setLog.durationSeconds?.toString() ?: "") }

    val bgColor = if (setLog.isCompleted) MaterialTheme.colorScheme.primary.copy(alpha = 0.1f) else Color.Transparent
    
    Row(
        modifier = Modifier.fillMaxWidth().padding(vertical = 4.dp).background(bgColor, RoundedCornerShape(12.dp)).padding(vertical = 4.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        if (exerciseType == ExerciseType.WEIGHTED || exerciseType == ExerciseType.WEIGHTED_BODYWEIGHT) {
            SetInputField(value = weightText, placeholder = "kg", onValueChange = { weightText = it; it.toFloatOrNull()?.let { weight -> onUpdate(setLog.copy(weight = weight)) } }, modifier = Modifier.weight(1f))
            Text(" × ", color = MaterialTheme.colorScheme.onSurfaceVariant)
            SetInputField(value = repsText, placeholder = "reps", onValueChange = { repsText = it; it.toIntOrNull()?.let { reps -> onUpdate(setLog.copy(reps = reps)) } }, modifier = Modifier.weight(1f))
        } else if (exerciseType == ExerciseType.BODYWEIGHT) {
            SetInputField(value = repsText, placeholder = "reps", onValueChange = { repsText = it; it.toIntOrNull()?.let { reps -> onUpdate(setLog.copy(reps = reps)) } }, modifier = Modifier.weight(1f))
            Text(" reps", color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.weight(1f).padding(start = 8.dp))
        } else {
            SetInputField(value = timeText, placeholder = "sec", onValueChange = { timeText = it; it.toIntOrNull()?.let { time -> onUpdate(setLog.copy(durationSeconds = time)) } }, modifier = Modifier.weight(1f))
            Text(" sec", color = MaterialTheme.colorScheme.onSurfaceVariant, modifier = Modifier.weight(1f).padding(start = 8.dp))
        }
        
        if (setLog.isCompleted) {
            IconButton(onClick = {
                haptic.performHapticFeedback(HapticFeedbackType.LongPress)
                onDelete()
            }) {
                Icon(Icons.Default.Delete, contentDescription = "Delete Set", tint = MaterialTheme.colorScheme.error)
            }
        } else {
            Button(
                onClick = { 
                    try {
                        val uri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION)
                        RingtoneManager.getRingtone(context, uri).play()
                    } catch (e: Exception) { e.printStackTrace() }
                    onUpdate(setLog.copy(isCompleted = true)) 
                },
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF4F46E5), contentColor = Color.White),
                shape = RoundedCornerShape(8.dp),
                contentPadding = PaddingValues(horizontal = 12.dp, vertical = 0.dp),
                modifier = Modifier.height(36.dp).padding(end = 4.dp, start = 4.dp)
            ) {
                Text("Log", fontWeight = FontWeight.Bold)
            }
        }
    }
}

@Composable
fun SetInputField(value: String, placeholder: String, onValueChange: (String) -> Unit, modifier: Modifier = Modifier) {
    val focusManager = LocalFocusManager.current
    Box(
        modifier = modifier.height(48.dp).background(Color(0xFFF8FAFC), RoundedCornerShape(12.dp)).padding(horizontal = 8.dp),
        contentAlignment = Alignment.Center
    ) {
        if (value.isEmpty()) {
            Text(placeholder, color = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f))
        }
        BasicTextField(
            value = value,
            onValueChange = onValueChange,
            textStyle = TextStyle(color = MaterialTheme.colorScheme.onSurface, fontSize = 20.sp, textAlign = TextAlign.Center, fontWeight = FontWeight.Bold),
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number, imeAction = ImeAction.Done),
            keyboardActions = KeyboardActions(onDone = { focusManager.clearFocus() }),
            cursorBrush = SolidColor(MaterialTheme.colorScheme.primary),
            modifier = Modifier.fillMaxWidth()
        )
    }
}
"""

with open("/app/applet/app/src/main/java/com/example/ui/workout/WorkoutScreen.kt", "w") as f:
    f.write(content)
