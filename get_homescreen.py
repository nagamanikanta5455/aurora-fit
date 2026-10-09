import re
with open('/app/applet/app/src/main/java/com/example/ui/home/HomeScreen.kt', 'r') as f:
    content = f.read()

# find HomeScreen function
pattern = r"(@Composable\s*fun HomeScreen.*?)\n@SuppressLint"
match = re.search(pattern, content, re.DOTALL)
if match:
    print(match.group(1).strip())
