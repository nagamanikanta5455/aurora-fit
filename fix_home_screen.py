import re

with open('/app/applet/app/src/main/java/com/example/ui/home/HomeScreen.kt', 'r') as f:
    content = f.read()

# Find the todayCompleted variable
today_completed_pattern = r"(val todayCompleted = completedWorkouts\.firstOrNull \{[\s\S]*?\n\s*\})"

# Add val hasTrainedToday = todayCompleted != null after it
def add_has_trained(match):
    return match.group(1) + "\n    val hasTrainedToday = todayCompleted != null\n"

content = re.sub(today_completed_pattern, add_has_trained, content, count=1)

# Find the "Ready to train?" text
ready_to_train_pattern = r'Text\(\s*"Ready to train\?",\s*style\s*=\s*MaterialTheme\.typography\.headlineLarge,\s*fontWeight\s*=\s*FontWeight\.Light,\s*color\s*=\s*MaterialTheme\.colorScheme\.onBackground\s*\)'

replacement = 'Text(if (hasTrainedToday) "Great work today" else "Ready to train?", style = MaterialTheme.typography.headlineLarge, fontWeight = FontWeight.Light, color = MaterialTheme.colorScheme.onBackground)'

content = re.sub(ready_to_train_pattern, replacement, content, count=1)

with open('/app/applet/app/src/main/java/com/example/ui/home/HomeScreen.kt', 'w') as f:
    f.write(content)

