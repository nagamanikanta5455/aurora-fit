import re

# Fix HomeScreen.kt
with open('/app/applet/app/src/main/java/com/example/ui/home/HomeScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    "modifier = Modifier.fillMaxSize().padding(bottom = paddingValues.calculateBottomPadding() + 24.dp),",
    "modifier = Modifier.fillMaxSize().padding(paddingValues),"
)

with open('/app/applet/app/src/main/java/com/example/ui/home/HomeScreen.kt', 'w') as f:
    f.write(content)

# Fix HistoryScreen.kt
with open('/app/applet/app/src/main/java/com/example/ui/history/HistoryScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    "modifier = Modifier.fillMaxSize().padding(paddingValues),",
    "modifier = Modifier.fillMaxSize(),"
)

content = content.replace(
    "LazyColumn(\n                    modifier = Modifier.fillMaxSize(),",
    "LazyColumn(\n                    modifier = Modifier.fillMaxSize().padding(paddingValues),"
)

with open('/app/applet/app/src/main/java/com/example/ui/history/HistoryScreen.kt', 'w') as f:
    f.write(content)

# Fix WorkoutScreen.kt
with open('/app/applet/app/src/main/java/com/example/ui/workout/WorkoutScreen.kt', 'r') as f:
    content = f.read()

content = content.replace(
    "modifier = Modifier.fillMaxSize().padding(paddingValues),",
    "modifier = Modifier.fillMaxSize(),"
)

content = content.replace(
    "LazyColumn(\n                    modifier = Modifier.fillMaxSize(),",
    "LazyColumn(\n                    modifier = Modifier.fillMaxSize().padding(paddingValues),"
)

content = content.replace(
    "Column(\n                modifier = Modifier.fillMaxSize().padding(24.dp),",
    "Column(\n                modifier = Modifier.fillMaxSize().padding(paddingValues).padding(24.dp),"
)

with open('/app/applet/app/src/main/java/com/example/ui/workout/WorkoutScreen.kt', 'w') as f:
    f.write(content)

