with open('/app/applet/app/src/main/java/com/example/ui/workout/WorkoutScreen.kt', 'r') as f:
    content = f.read()

import re

# We will just replace everything between 'item {' and 'items(' which contains the header.
pattern = r"item\s*\{\s*Row\([\s\S]*?Icon\(Icons\.Default\.Close[\s\S]*?\}\s*\)\s*\{\s*Icon[\s\S]*?\}\s*\}\s*\}"

replacement = """item {
                    Row(
                        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Column(modifier = Modifier.weight(1f)) {
                            Text("TODAY", style = MaterialTheme.typography.labelMedium, color = MaterialTheme.colorScheme.onSurfaceVariant, letterSpacing = 1.sp)
                            Text(
                                text = details.workout.name.uppercase(), 
                                style = MaterialTheme.typography.headlineMedium, 
                                fontWeight = FontWeight.Bold,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis
                            )
                        }
                        IconButton(onClick = {
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
                        }) {
                            Icon(Icons.Default.Close, contentDescription = "Cancel Workout", tint = MaterialTheme.colorScheme.error)
                        }
                    }
                }"""

content = re.sub(pattern, replacement, content, count=1)

with open('/app/applet/app/src/main/java/com/example/ui/workout/WorkoutScreen.kt', 'w') as f:
    f.write(content)
