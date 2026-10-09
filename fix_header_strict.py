import re

with open('/app/applet/app/src/main/java/com/example/ui/workout/WorkoutScreen.kt', 'r') as f:
    content = f.read()

# We need to find the item block that contains the "TODAY" text and replace the Row inside it.
pattern = r"item\s*\{\s*Row\(\s*modifier = Modifier\.fillMaxWidth\(\)[^\}]+\}\s*\)\s*\{\s*Icon\(Icons\.Default\.Close[^\}]+\}\s*\}"

new_row = """item {
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
                    }"""

content = re.sub(pattern, new_row, content, count=1, flags=re.DOTALL)

with open('/app/applet/app/src/main/java/com/example/ui/workout/WorkoutScreen.kt', 'w') as f:
    f.write(content)
