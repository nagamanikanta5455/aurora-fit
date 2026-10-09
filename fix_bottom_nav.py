import re

with open('/app/applet/app/src/main/java/com/example/ui/AuroraFitApp.kt', 'r') as f:
    content = f.read()

pattern = r"NavigationBar\("
replacement = r"NavigationBar(\n                modifier = Modifier.height(76.dp),"

content = re.sub(pattern, replacement, content)

with open('/app/applet/app/src/main/java/com/example/ui/AuroraFitApp.kt', 'w') as f:
    f.write(content)
