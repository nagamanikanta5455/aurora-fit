import re

# Fix MainViewModel.kt
with open('/app/applet/app/src/main/java/com/example/ui/MainViewModel.kt', 'r') as f:
    content = f.read()
content = content.replace("import android.content.Context\nimport androidx.lifecycle.ViewModelProvider", "import androidx.lifecycle.ViewModelProvider")
with open('/app/applet/app/src/main/java/com/example/ui/MainViewModel.kt', 'w') as f:
    f.write(content)

# Fix AuroraFitApp.kt
with open('/app/applet/app/src/main/java/com/example/ui/AuroraFitApp.kt', 'r') as f:
    content = f.read()
if "import androidx.compose.foundation.layout.height" not in content:
    content = content.replace("import androidx.compose.foundation.layout.fillMaxSize", "import androidx.compose.foundation.layout.fillMaxSize\nimport androidx.compose.foundation.layout.height")
with open('/app/applet/app/src/main/java/com/example/ui/AuroraFitApp.kt', 'w') as f:
    f.write(content)

