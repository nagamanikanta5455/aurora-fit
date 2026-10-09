import re

with open('/app/applet/app/src/main/java/com/example/ui/theme/Theme.kt', 'r') as f:
    content = f.read()

# Add a generic dark color scheme if missing
if "AuroraDarkColorScheme" not in content:
    dark_scheme = """
private val AuroraDarkColorScheme = darkColorScheme(
    primary = Color(0xFF818CF8),
    secondary = Color(0xFF34D399),
    tertiary = Color(0xFF2DD4BF),
    background = Color(0xFF121212),
    surface = Color(0xFF1E1E1E),
    surfaceVariant = Color(0xFF333333),
    onPrimary = Color.White,
    onSecondary = Color.Black,
    onTertiary = Color.Black,
    onBackground = Color.White,
    onSurface = Color.White,
    onSurfaceVariant = Color(0xFFAAAAAA),
    outline = Color(0xFF444444)
)
"""
    content = content.replace("private val AuroraLightColorScheme", dark_scheme + "\nprivate val AuroraLightColorScheme")

# Update MyApplicationTheme to accept darkTheme
pattern = r"fun MyApplicationTheme\(\s*content: @Composable \(\) -> Unit,?\s*\) \{"
replacement = r"fun MyApplicationTheme(\n  darkTheme: Boolean = isSystemInDarkTheme(),\n  content: @Composable () -> Unit\n) {"
content = re.sub(pattern, replacement, content)

# Use darkTheme to select colorScheme
color_scheme_pattern = r"val colorScheme = AuroraLightColorScheme"
color_scheme_replacement = r"val colorScheme = if (darkTheme) AuroraDarkColorScheme else AuroraLightColorScheme"
content = re.sub(color_scheme_pattern, color_scheme_replacement, content)

# Update system bars
bars_pattern = r"WindowCompat.getInsetsController\(window, view\)\.isAppearanceLightStatusBars = true\n\s*WindowCompat.getInsetsController\(window, view\)\.isAppearanceLightNavigationBars = true"
bars_replacement = r"WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = !darkTheme\n      WindowCompat.getInsetsController(window, view).isAppearanceLightNavigationBars = !darkTheme"
content = re.sub(bars_pattern, bars_replacement, content)

with open('/app/applet/app/src/main/java/com/example/ui/theme/Theme.kt', 'w') as f:
    f.write(content)

