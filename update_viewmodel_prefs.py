import re

with open('/app/applet/app/src/main/java/com/example/ui/MainViewModel.kt', 'r') as f:
    content = f.read()

# Add Context import if needed
if "android.content.Context" not in content:
    content = content.replace("import androidx.lifecycle.ViewModel", "import android.content.Context\nimport androidx.lifecycle.ViewModel")

pattern = r"private val _isDarkMode = MutableStateFlow\(false\)\n    val isDarkMode: StateFlow<Boolean> = _isDarkMode\.asStateFlow\(\)\n\n    fun toggleTheme\(\) \{\n        _isDarkMode\.value = !_isDarkMode\.value\n    \}"

replacement = r"""private val prefs = Graph.appContext.getSharedPreferences("theme_prefs", Context.MODE_PRIVATE)
    private val _isDarkMode = MutableStateFlow(prefs.getBoolean("is_dark_mode", false))
    val isDarkMode: StateFlow<Boolean> = _isDarkMode.asStateFlow()

    fun toggleTheme() {
        val newValue = !_isDarkMode.value
        _isDarkMode.value = newValue
        prefs.edit().putBoolean("is_dark_mode", newValue).apply()
    }"""

content = re.sub(pattern, replacement, content)

with open('/app/applet/app/src/main/java/com/example/ui/MainViewModel.kt', 'w') as f:
    f.write(content)
