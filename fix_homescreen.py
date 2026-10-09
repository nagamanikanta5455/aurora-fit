import re

with open('/app/applet/app/src/main/java/com/example/ui/home/HomeScreen.kt', 'r') as f:
    content = f.read()

# Replace the toggle button Row with Box TopEnd
pattern = r"val haptic = LocalHapticFeedback.current\s+Row\(modifier = Modifier.fillMaxWidth\(\)\) \{\s+IconButton"
replacement = r"""val haptic = LocalHapticFeedback.current
                        Box(modifier = Modifier.fillMaxWidth(), contentAlignment = Alignment.TopEnd) {
                            IconButton"""
content = re.sub(pattern, replacement, content)
content = content.replace("tint = MaterialTheme.colorScheme.onBackground\n                                )\n                            }\n                        }", "tint = MaterialTheme.colorScheme.onBackground\n                                )\n                            }\n                        }") # This doesn't change anything, just checking the brace matching. Let's do it cleaner.

# Actually, let's just do a string replacement for the exact block.
old_block = """val haptic = LocalHapticFeedback.current
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
new_block = """val haptic = LocalHapticFeedback.current
                        Box(modifier = Modifier.fillMaxWidth().padding(top = 4.dp, end = 4.dp), contentAlignment = Alignment.TopEnd) {
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
content = content.replace(old_block, new_block)

# Fix Background Gradient in HomeScreen
old_gradient = """brush = Brush.linearGradient(
                    colors = listOf(
                        MaterialTheme.colorScheme.background,
                        MaterialTheme.colorScheme.tertiary.copy(alpha = 0.5f),
                        MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
                    )
                )"""
new_gradient = """brush = Brush.linearGradient(
                        colors = if (isDarkMode) listOf(
                            Color(0xFF0F172A),
                            Color(0xFF1E1B4B),
                            Color(0xFF064E3B)
                        ) else listOf(
                            MaterialTheme.colorScheme.background,
                            MaterialTheme.colorScheme.tertiary.copy(alpha = 0.5f),
                            MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f)
                        )
                    )"""
content = content.replace(old_gradient, new_gradient)

# MonthlyProgressCard text color fixes
content = content.replace("color = Color(0xFF4F46E5)", "color = MaterialTheme.colorScheme.primary")
content = content.replace("color = Color.White", "color = MaterialTheme.colorScheme.onPrimary")
content = content.replace("color = if (isCompleted) Color(0xFF4F46E5) else Color.Transparent", "color = if (isCompleted) MaterialTheme.colorScheme.primary else Color.Transparent")
content = content.replace("color = if (isCompleted) Color.White else if (isToday) Color(0xFF4F46E5) else MaterialTheme.colorScheme.onSurface", "color = if (isCompleted) MaterialTheme.colorScheme.onPrimary else if (isToday) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onSurface")

with open('/app/applet/app/src/main/java/com/example/ui/home/HomeScreen.kt', 'w') as f:
    f.write(content)

