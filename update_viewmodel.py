import re

with open('/app/applet/app/src/main/java/com/example/ui/MainViewModel.kt', 'r') as f:
    content = f.read()

# Add isDarkMode state and toggleTheme function
pattern = r"(class MainViewModel.*?\{)"
replacement = r"\1\n\n    private val _isDarkMode = MutableStateFlow(false)\n    val isDarkMode: StateFlow<Boolean> = _isDarkMode.asStateFlow()\n\n    fun toggleTheme() {\n        _isDarkMode.value = !_isDarkMode.value\n    }\n"

content = re.sub(pattern, replacement, content, count=1)

with open('/app/applet/app/src/main/java/com/example/ui/MainViewModel.kt', 'w') as f:
    f.write(content)

