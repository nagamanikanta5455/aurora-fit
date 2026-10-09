import re

with open('/app/applet/app/src/main/java/com/example/ui/home/HomeScreen.kt', 'r') as f:
    content = f.read()

# Add imports
imports = """
import androidx.compose.material.icons.filled.DarkMode
import androidx.compose.material.icons.filled.LightMode
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.platform.LocalHapticFeedback
"""
content = content.replace("import androidx.compose.material.icons.Icons", "import androidx.compose.material.icons.Icons" + imports)

# Add isDarkMode state in HomeScreen
pattern_state = r"(val hasTrainedToday = todayCompleted != null)"
replacement_state = r"\1\n    val isDarkMode by viewModel.isDarkMode.collectAsState()"
content = re.sub(pattern_state, replacement_state, content)

# Remove hardcoded colors in Surface and Box
content = content.replace("color = Color(0xFFF8FAFC)", "color = MaterialTheme.colorScheme.background")
content = content.replace("Color(0xFFF8FAFC),", "MaterialTheme.colorScheme.background,")

# Add the toggle button
pattern_column = r"(item \{\n\s*Column \{)"
replacement_column = r"""\1
                    val haptic = LocalHapticFeedback.current
                    Row(modifier = Modifier.fillMaxWidth()) {
                        IconButton(onClick = { 
                            haptic.performHapticFeedback(HapticFeedbackType.LongPress)
                            viewModel.toggleTheme() 
                        }) {
                            Icon(
                                imageVector = if (isDarkMode) Icons.Default.LightMode else Icons.Default.DarkMode,
                                contentDescription = "Toggle Theme",
                                tint = MaterialTheme.colorScheme.onBackground
                            )
                        }
                    }"""
content = re.sub(pattern_column, replacement_column, content)

# Check MonthlyProgressCard for Color(0xFFF8FAFC)
content = content.replace("containerColor = Color(0xFFF8FAFC)", "containerColor = MaterialTheme.colorScheme.background")

with open('/app/applet/app/src/main/java/com/example/ui/home/HomeScreen.kt', 'w') as f:
    f.write(content)

