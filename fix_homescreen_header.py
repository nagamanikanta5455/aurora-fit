import re

with open('/app/applet/app/src/main/java/com/example/ui/home/HomeScreen.kt', 'r') as f:
    content = f.read()

pattern = r"item \{\n\s*Column \{\n\s*val haptic = LocalHapticFeedback\.current[\s\S]*?Text\(if \(hasTrainedToday\)[^\n]*\n\s*\}"

replacement = """item {
                val haptic = LocalHapticFeedback.current
                Box(modifier = Modifier.fillMaxWidth()) {
                    Column(modifier = Modifier.align(Alignment.TopStart).padding(end = 48.dp)) {
                        Text(greeting, style = MaterialTheme.typography.labelLarge, color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold, letterSpacing = 2.sp)
                        Spacer(modifier = Modifier.height(8.dp))
                        Text(if (hasTrainedToday) "Great work today" else "Ready to train?", style = MaterialTheme.typography.headlineLarge, fontWeight = FontWeight.Light, color = MaterialTheme.colorScheme.onBackground)
                    }
                    IconButton(
                        onClick = { 
                            haptic.performHapticFeedback(HapticFeedbackType.LongPress)
                            viewModel.toggleTheme() 
                        },
                        modifier = Modifier.align(Alignment.TopEnd).offset(x = 12.dp, y = (-12).dp)
                    ) {
                        Icon(
                            imageVector = if (isDarkMode) Icons.Default.LightMode else Icons.Default.DarkMode,
                            contentDescription = "Toggle Theme",
                            tint = MaterialTheme.colorScheme.onBackground
                        )
                    }
                }"""

content = re.sub(pattern, replacement, content)

with open('/app/applet/app/src/main/java/com/example/ui/home/HomeScreen.kt', 'w') as f:
    f.write(content)
