import re

with open('/app/applet/app/src/main/java/com/example/ui/AuroraFitApp.kt', 'r') as f:
    content = f.read()

content = content.replace(
    'modifier = Modifier.fillMaxSize().background(MaterialTheme.colorScheme.background)',
    'modifier = Modifier.fillMaxSize().padding(paddingValues).background(MaterialTheme.colorScheme.background)'
)

with open('/app/applet/app/src/main/java/com/example/ui/AuroraFitApp.kt', 'w') as f:
    f.write(content)
