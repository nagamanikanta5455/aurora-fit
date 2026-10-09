import re
with open('/app/applet/app/src/main/java/com/example/ui/workout/WorkoutScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'modifier = modifier.height(48.dp).background(Color(0xFFF8FAFC), RoundedCornerShape(12.dp)).padding(horizontal = 8.dp),',
    'modifier = modifier.height(48.dp).background(MaterialTheme.colorScheme.surfaceVariant, RoundedCornerShape(12.dp)).padding(horizontal = 8.dp),'
)

with open('/app/applet/app/src/main/java/com/example/ui/workout/WorkoutScreen.kt', 'w') as f:
    f.write(content)
