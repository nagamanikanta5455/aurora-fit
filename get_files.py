import json

def get_file(path):
    with open(path, 'r') as f:
        return f.read()

print(json.dumps({
    "HomeScreen.kt": get_file('/app/applet/app/src/main/java/com/example/ui/home/HomeScreen.kt'),
    "WorkoutScreen.kt": get_file('/app/applet/app/src/main/java/com/example/ui/workout/WorkoutScreen.kt'),
    "HistoryScreen.kt": get_file('/app/applet/app/src/main/java/com/example/ui/history/HistoryScreen.kt')
}))
