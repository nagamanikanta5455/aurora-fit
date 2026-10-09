import re

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'r') as f:
    content = f.read()

# Make sure collectAsState is imported
if "androidx.compose.runtime.collectAsState" not in content:
    content = content.replace("import android.os.Bundle", "import android.os.Bundle\nimport androidx.compose.runtime.collectAsState\nimport androidx.compose.runtime.getValue")

# Read isDarkMode state in setContent and pass it to MyApplicationTheme
pattern = r"setContent \{\s*MyApplicationTheme \{"
replacement = r"setContent {\n      val isDarkMode by viewModel.isDarkMode.collectAsState()\n      MyApplicationTheme(darkTheme = isDarkMode) {"
content = re.sub(pattern, replacement, content)

with open('/app/applet/app/src/main/java/com/example/MainActivity.kt', 'w') as f:
    f.write(content)

