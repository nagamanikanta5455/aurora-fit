with open('/app/applet/app/src/main/java/com/example/ui/AuroraFitApp.kt', 'r') as f:
    content = f.read()

content = content.replace("modifier = Modifier.height(76.dp)", "modifier = Modifier.height(72.dp)")

with open('/app/applet/app/src/main/java/com/example/ui/AuroraFitApp.kt', 'w') as f:
    f.write(content)
