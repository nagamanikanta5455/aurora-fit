import re

with open('/app/applet/app/src/main/java/com/example/ui/workout/WorkoutScreen.kt', 'r') as f:
    content = f.read()

pattern = r"item\s*\{\s*Row\([\s\S]*?Icon\(Icons\.Default\.Close[\s\S]*?\}\s*\)\s*\{\s*Icon[\s\S]*?\}\s*\}\s*\}"

replacement = """item {
                    Box(
                        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp)
                    ) {
                        Column(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(end = 48.dp)
                        ) {
                            Text("TODAY", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant, letterSpacing = 1.sp)
                            Text(
                                text = details.workout.name.uppercase().replace(" WORKOUT", "").replace("WORKOUT", "").trim(), 
                                style = MaterialTheme.typography.headlineMedium, 
                                fontWeight = FontWeight.Bold
                            )
                        }
                        IconButton(
                            onClick = {
                                haptic.performHapticFeedback(HapticFeedbackType.LongPress)
                                try {
                                    viewModel.cancelWorkout(details.workout)
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
                            modifier = Modifier.align(Alignment.CenterEnd)
                        ) {
                            Icon(Icons.Default.Close, contentDescription = "Cancel Workout", tint = MaterialTheme.colorScheme.error)
                        }
                    }
                }"""

content = re.sub(pattern, replacement, content, count=1)

with open('/app/applet/app/src/main/java/com/example/ui/workout/WorkoutScreen.kt', 'w') as f:
    f.write(content)
