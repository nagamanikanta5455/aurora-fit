import re

with open('/app/applet/app/src/main/java/com/example/ui/workout/WorkoutScreen.kt', 'r') as f:
    content = f.read()

# Add import
if 'import androidx.navigation.NavGraph.Companion.findStartDestination' not in content:
    content = content.replace('import androidx.navigation.NavController\n', 
                              'import androidx.navigation.NavController\nimport androidx.navigation.NavGraph.Companion.findStartDestination\n')


# Fix Cancel Button
old_cancel = """                        IconButton(onClick = {
                            haptic.performHapticFeedback(HapticFeedbackType.LongPress)
                            viewModel.cancelWorkout(details.workout)
                            navController.navigate("home")
                        })"""

new_cancel = """                        IconButton(onClick = {
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
                        })"""
content = content.replace(old_cancel, new_cancel)


# Fix Finish Button
old_finish = """                    Button(
                        onClick = {
                            try {
                                val uri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION)
                                RingtoneManager.getRingtone(context, uri).play()
                            } catch (e: Exception) { e.printStackTrace() }
                            viewModel.finishWorkout(details.workout)
                            navController.navigate("home")
                        },"""

new_finish = """                    Button(
                        onClick = {
                            try {
                                val uri = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION)
                                RingtoneManager.getRingtone(context, uri).play()
                            } catch (e: Exception) { e.printStackTrace() }
                            
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
                        },"""
content = content.replace(old_finish, new_finish)

with open('/app/applet/app/src/main/java/com/example/ui/workout/WorkoutScreen.kt', 'w') as f:
    f.write(content)
