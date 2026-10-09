with open('/app/applet/app/src/main/java/com/example/ui/home/HomeScreen.kt', 'r') as f:
    content = f.read()

# I wrote `}    }` at the end of the HomeScreen instead of closing it completely, before `@SuppressLint("NewApi")`
# Let's insert the missing brace right before `@SuppressLint("NewApi")\n    @Composable\n    fun MonthlyProgressCard`

content = content.replace('    @SuppressLint("NewApi")\n    @Composable\n    fun MonthlyProgressCard', '}\n\n@SuppressLint("NewApi")\n@Composable\nfun MonthlyProgressCard')

with open('/app/applet/app/src/main/java/com/example/ui/home/HomeScreen.kt', 'w') as f:
    f.write(content)

