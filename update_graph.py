import re

with open('/app/applet/app/src/main/java/com/example/Graph.kt', 'r') as f:
    content = f.read()

if "lateinit var appContext" not in content:
    content = content.replace("lateinit var database: AppDatabase", "lateinit var database: AppDatabase\n        private set\n    lateinit var appContext: Context")
    content = content.replace("fun provide(context: Context) {", "fun provide(context: Context) {\n        appContext = context.applicationContext")

    with open('/app/applet/app/src/main/java/com/example/Graph.kt', 'w') as f:
        f.write(content)
