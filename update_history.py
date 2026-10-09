import re

with open('/app/applet/app/src/main/java/com/example/ui/history/HistoryScreen.kt', 'r') as f:
    content = f.read()

# 1. Update the calculations and top metrics layout in HistoryScreen
stats_old = """    // Calculates lifetime stats
    val totalWorkouts = completedWorkouts.size
    var totalSets = 0
    var totalReps = 0
    completedWorkouts.forEach { w ->
        w.exercises.forEach { e ->
            totalSets += e.sets.size
            e.sets.forEach { set ->
                totalReps += set.reps ?: 0
            }
        }
    }"""

stats_new = """    // Calculates lifetime stats
    val totalWorkouts = completedWorkouts.size
    var totalSets = 0
    var totalReps = 0
    var totalDurationSeconds = 0
    completedWorkouts.forEach { w ->
        w.exercises.forEach { e ->
            totalSets += e.sets.size
            e.sets.forEach { set ->
                totalReps += set.reps ?: 0
                totalDurationSeconds += set.durationSeconds ?: 0
            }
        }
    }
    
    val formattedDuration = if (totalDurationSeconds < 3600) {
        val m = totalDurationSeconds / 60
        "${m}m"
    } else {
        val h = totalDurationSeconds / 3600
        val m = (totalDurationSeconds % 3600) / 60
        if (m > 0) "${h}h ${m}m" else "${h}h"
    }"""

content = content.replace(stats_old, stats_new)

row_old = """                        // Lifetime Stats Row
                        Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                            StatCard(modifier = Modifier.weight(1f), value = totalWorkouts.toString(), label = "Workouts")
                            StatCard(modifier = Modifier.weight(1f), value = totalSets.toString(), label = "Sets")
                            StatCard(modifier = Modifier.weight(1f), value = totalReps.toString(), label = "Reps")
                        }"""

row_new = """                        // Lifetime Stats Grid
                        Column(verticalArrangement = Arrangement.spacedBy(12.dp)) {
                            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                                StatCard(modifier = Modifier.weight(1f), value = totalWorkouts.toString(), label = "Workouts")
                                StatCard(modifier = Modifier.weight(1f), value = totalSets.toString(), label = "Sets")
                            }
                            Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                                StatCard(modifier = Modifier.weight(1f), value = totalReps.toString(), label = "Reps")
                                StatCard(modifier = Modifier.weight(1f), value = formattedDuration, label = "Duration")
                            }
                        }"""

content = content.replace(row_old, row_new)

# 2. Update WorkoutHistoryCard for the timeline badge
card_old = """                val totalSets = workout.exercises.sumOf { it.sets.size }
                Column(horizontalAlignment = Alignment.End) {
                    Text("${workout.exercises.size} Ex", fontWeight = FontWeight.SemiBold, color = MaterialTheme.colorScheme.onSurface)
                    Text("$totalSets Sets", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }"""

card_new = """                val totalSets = workout.exercises.sumOf { it.sets.size }
                val workoutDurationSeconds = workout.exercises.sumOf { e -> e.sets.sumOf { it.durationSeconds ?: 0 } }
                
                Column(horizontalAlignment = Alignment.End) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        if (workoutDurationSeconds > 0) {
                            val durText = if (workoutDurationSeconds < 3600) {
                                "${workoutDurationSeconds / 60}m"
                            } else {
                                val h = workoutDurationSeconds / 3600
                                val m = (workoutDurationSeconds % 3600) / 60
                                if (m > 0) "${h}h ${m}m" else "${h}h"
                            }
                            Text("⏱ $durText", fontWeight = FontWeight.SemiBold, color = MaterialTheme.colorScheme.primary, fontSize = 13.sp)
                            Spacer(modifier = Modifier.width(6.dp))
                        }
                        Text("${workout.exercises.size} Ex", fontWeight = FontWeight.SemiBold, color = MaterialTheme.colorScheme.onSurface)
                    }
                    Text("$totalSets Sets", style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                }"""

content = content.replace(card_old, card_new)

with open('/app/applet/app/src/main/java/com/example/ui/history/HistoryScreen.kt', 'w') as f:
    f.write(content)

