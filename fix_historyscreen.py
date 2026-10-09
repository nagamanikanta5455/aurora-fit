import re

with open('/app/applet/app/src/main/java/com/example/ui/history/HistoryScreen.kt', 'r') as f:
    content = f.read()

# Add isDarkMode
content = content.replace("val workouts by viewModel.allWorkouts.collectAsState()", "val workouts by viewModel.allWorkouts.collectAsState()\n    val isDarkMode by viewModel.isDarkMode.collectAsState()")

# Fix Surface color
content = content.replace("color = Color(0xFFF8FAFC)", "color = MaterialTheme.colorScheme.background")

# Fix Background Gradient
old_gradient = """brush = Brush.radialGradient(
                        colors = listOf(
                            MaterialTheme.colorScheme.tertiary.copy(alpha = 0.3f),
                            Color(0xFFF8FAFC)
                        ),
                        radius = 1500f
                    )"""
new_gradient = """brush = Brush.radialGradient(
                        colors = if (isDarkMode) listOf(
                            Color(0xFF064E3B),
                            Color(0xFF0F172A)
                        ) else listOf(
                            MaterialTheme.colorScheme.tertiary.copy(alpha = 0.3f),
                            MaterialTheme.colorScheme.background
                        ),
                        radius = 1500f
                    )"""
content = content.replace(old_gradient, new_gradient)

# Fix Text Colors and hardcoded colors
content = content.replace("Color(0xFFEEF2FF)", "MaterialTheme.colorScheme.surfaceVariant") # Light indigo bg
content = content.replace("Color(0xFFECFDF5)", "MaterialTheme.colorScheme.surfaceVariant") # Light emerald bg
# Make sure text isn't hardcoded dark/white where it shouldn't be. 

with open('/app/applet/app/src/main/java/com/example/ui/history/HistoryScreen.kt', 'w') as f:
    f.write(content)

