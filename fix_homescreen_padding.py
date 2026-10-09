with open('/app/applet/app/src/main/java/com/example/ui/home/HomeScreen.kt', 'r') as f:
    content = f.read()

# I want to change contentPadding = PaddingValues(start = 24.dp, end = 24.dp, top = 32.dp, bottom = paddingValues.calculateBottomPadding() + 80.dp) to just bottom = 24.dp
import re
content = re.sub(r'bottom\s*=\s*paddingValues\.calculateBottomPadding\(\)\s*\+\s*\d+\.dp', 'bottom = 24.dp', content)
content = re.sub(r'bottom\s*=\s*\d+\.dp.*?// This dynamically reads the EXACT height of your nav bar', 'bottom = 24.dp', content)

# Check if there are any other huge paddings
content = re.sub(r'bottom\s*=\s*120\.dp', 'bottom = 24.dp', content)

with open('/app/applet/app/src/main/java/com/example/ui/home/HomeScreen.kt', 'w') as f:
    f.write(content)
