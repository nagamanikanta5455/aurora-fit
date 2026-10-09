import re

with open('/app/applet/app/src/main/java/com/example/ui/home/HomeScreen.kt', 'r') as f:
    content = f.read()

# Match the @Composable fun HomeScreen ... to the end of its body
match = re.search(r'(@Composable\nfun HomeScreen.*?^})', content, re.MULTILINE | re.DOTALL)
if match:
    print(match.group(1))
else:
    print("Not found")

