# Check WorkoutScreen and HistoryScreen as well
files = [
    '/app/applet/app/src/main/java/com/example/ui/workout/WorkoutScreen.kt',
    '/app/applet/app/src/main/java/com/example/ui/history/HistoryScreen.kt'
]
import re
for path in files:
    with open(path, 'r') as f:
        content = f.read()
    
    # We replace any `bottom = 120.dp` or `paddingValues.calculateBottomPadding() + 80.dp` with `24.dp`
    content = re.sub(r'bottom\s*=\s*paddingValues\.calculateBottomPadding\(\)\s*\+\s*\d+\.dp', 'bottom = 24.dp', content)
    content = re.sub(r'bottom\s*=\s*\d+\.dp.*?// This dynamically reads the EXACT height of your nav bar', 'bottom = 24.dp', content)
    content = re.sub(r'bottom\s*=\s*120\.dp', 'bottom = 24.dp', content)
    
    with open(path, 'w') as f:
        f.write(content)
