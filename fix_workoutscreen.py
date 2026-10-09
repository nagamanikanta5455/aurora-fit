import re

with open('/app/applet/app/src/main/java/com/example/ui/workout/WorkoutScreen.kt', 'r') as f:
    content = f.read()

# Add isDarkMode
content = content.replace("val activeWorkout by viewModel.activeWorkout.collectAsState()", "val activeWorkout by viewModel.activeWorkout.collectAsState()\n    val isDarkMode by viewModel.isDarkMode.collectAsState()")

# Fix Surface color
content = content.replace("color = Color(0xFFF8FAFC)", "color = MaterialTheme.colorScheme.background")

# Fix Background Gradient
old_gradient = """brush = Brush.linearGradient(
                    colors = listOf(
                        Color(0xFFF8FAFC),
                        MaterialTheme.colorScheme.tertiary.copy(alpha = 0.5f)
                    )
                )"""
new_gradient = """brush = Brush.linearGradient(
                        colors = if (isDarkMode) listOf(
                            Color(0xFF0F172A),
                            Color(0xFF1E1B4B)
                        ) else listOf(
                            MaterialTheme.colorScheme.background,
                            MaterialTheme.colorScheme.tertiary.copy(alpha = 0.5f)
                        )
                    )"""
content = content.replace(old_gradient, new_gradient)

# Fix Text Colors
content = content.replace("color = Color(0xFF888888)", "color = MaterialTheme.colorScheme.onSurfaceVariant")
content = content.replace("color = Color(0xFF666666)", "color = MaterialTheme.colorScheme.onSurfaceVariant")
content = content.replace("color = Color.Black", "color = MaterialTheme.colorScheme.onSurface")
content = content.replace("color = Color.White", "color = MaterialTheme.colorScheme.onPrimary")

# Any containerColor fixes
content = content.replace("containerColor = Color(0xFFEEEEEE)", "containerColor = MaterialTheme.colorScheme.surfaceVariant")
content = content.replace("containerColor = Color.White", "containerColor = MaterialTheme.colorScheme.surface")

with open('/app/applet/app/src/main/java/com/example/ui/workout/WorkoutScreen.kt', 'w') as f:
    f.write(content)

