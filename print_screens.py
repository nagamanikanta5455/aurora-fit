import re

def print_composable(filepath, composable_name):
    with open(filepath, 'r') as f:
        content = f.read()
    match = re.search(r'(@Composable\s*fun ' + composable_name + r'.*?^})', content, re.MULTILINE | re.DOTALL)
    if match:
        print(f"// {filepath.split('/')[-1]}")
        print(match.group(1))
        print("\n")

print_composable('/app/applet/app/src/main/java/com/example/ui/home/HomeScreen.kt', 'HomeScreen')
print_composable('/app/applet/app/src/main/java/com/example/ui/history/HistoryScreen.kt', 'HistoryScreen')
print_composable('/app/applet/app/src/main/java/com/example/ui/workout/WorkoutScreen.kt', 'WorkoutScreen')
