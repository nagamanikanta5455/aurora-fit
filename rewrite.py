import re

with open('/app/applet/app/src/main/java/com/example/ui/workout/WorkoutScreen.kt', 'r') as f:
    content = f.read()

# 1. Add Icons.Default.Close, Icons.Default.Edit, Icons.Default.Delete to imports
imports = """import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Edit
import androidx.compose.material.icons.filled.Delete
"""
content = content.replace("import androidx.compose.material.icons.filled.Add\n", imports + "import androidx.compose.material.icons.filled.Add\n")

# 2. Cancel Workout Button
old_header = """                        Column {
                            Text("TODAY", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant, letterSpacing = 1.sp)
                            Text(details.workout.name.uppercase(), style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
                        }
                    }
                }"""

new_header = """                        Column {
                            Text("TODAY", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant, letterSpacing = 1.sp)
                            Text(details.workout.name.uppercase(), style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
                        }
                        IconButton(onClick = { 
                            viewModel.cancelWorkout(details.workout)
                            navController.navigate("home")
                        }) {
                            Icon(Icons.Default.Close, contentDescription = "Cancel Workout", tint = MaterialTheme.colorScheme.error)
                        }
                    }
                }"""
content = content.replace(old_header, new_header)

# 3. Add Custom Exercise -> Add Exercise
content = content.replace('title = { Text("Add Custom Exercise", style = MaterialTheme.typography.titleLarge) }',
                          'title = { Text("Add Exercise", style = MaterialTheme.typography.titleLarge) }')

# 4. Exercise Edit & Delete Icons
old_exercise_header = """Text(exerciseWithSets.exercise.name.uppercase(), color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, letterSpacing = 1.sp)"""

new_exercise_header = """var showEditDialog by remember { mutableStateOf(false) }
            
            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Text(exerciseWithSets.exercise.name.uppercase(), color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, letterSpacing = 1.sp, modifier = Modifier.weight(1f))
                Row {
                    IconButton(onClick = { showEditDialog = true }) {
                        Icon(Icons.Default.Edit, contentDescription = "Edit Exercise", tint = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    IconButton(onClick = { viewModel.deleteExercise(exerciseWithSets.exercise) }) {
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
            }"""
content = content.replace(old_exercise_header, new_exercise_header)

# 5. Set Logging & Deletion
# Need to update SetRow signature and its usage.
old_setrow_call = """SetRow(
                    setLog = setLog,
                    exerciseType = exerciseWithSets.exercise.type,
                    onUpdate = { updatedSet -> viewModel.updateSetLog(updatedSet) }
                )"""
new_setrow_call = """SetRow(
                    setLog = setLog,
                    exerciseType = exerciseWithSets.exercise.type,
                    onUpdate = { updatedSet -> viewModel.updateSetLog(updatedSet) },
                    onDelete = { viewModel.deleteSetLog(setLog) }
                )"""
content = content.replace(old_setrow_call, new_setrow_call)

old_setrow_sig = """fun SetRow(setLog: SetLog, exerciseType: ExerciseType, onUpdate: (SetLog) -> Unit) {"""
new_setrow_sig = """fun SetRow(setLog: SetLog, exerciseType: ExerciseType, onUpdate: (SetLog) -> Unit, onDelete: () -> Unit) {"""
content = content.replace(old_setrow_sig, new_setrow_sig)

old_setrow_action = """IconButton(onClick = { onUpdate(setLog.copy(isCompleted = !setLog.isCompleted)) }) {
            Icon(Icons.Default.Check, contentDescription = "Complete", tint = if (setLog.isCompleted) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f))
        }"""
new_setrow_action = """if (setLog.isCompleted) {
            IconButton(onClick = onDelete) {
                Icon(Icons.Default.Delete, contentDescription = "Delete Set", tint = MaterialTheme.colorScheme.error)
            }
        } else {
            Button(
                onClick = { onUpdate(setLog.copy(isCompleted = true)) },
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF4F46E5), contentColor = Color.White),
                shape = RoundedCornerShape(8.dp),
                contentPadding = PaddingValues(horizontal = 12.dp, vertical = 0.dp),
                modifier = Modifier.height(36.dp).padding(end = 4.dp, start = 4.dp)
            ) {
                Text("Log", fontWeight = FontWeight.Bold)
            }
        }"""
content = content.replace(old_setrow_action, new_setrow_action)

with open('/app/applet/app/src/main/java/com/example/ui/workout/WorkoutScreen.kt', 'w') as f:
    f.write(content)

