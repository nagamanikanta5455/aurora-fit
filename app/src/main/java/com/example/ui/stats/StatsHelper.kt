package com.example.ui.stats

import com.example.data.model.WorkoutWithExercises
import java.util.Calendar

object StatsHelper {
    fun calculateStreak(
        workouts: List<WorkoutWithExercises>,
        restDays: Set<String> = emptySet()
    ): Int {
        val dateFormat = java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.US)
        
        // Collect dates that have completed workouts
        val workoutDates = workouts.map {
            dateFormat.format(java.util.Date(it.workout.dateMillis))
        }.toSet()

        // Active days are either workout days or planned rest days
        val activeDates = workoutDates + restDays
        if (activeDates.isEmpty()) return 0

        val cal = Calendar.getInstance()
        val todayStr = dateFormat.format(cal.time)

        cal.add(Calendar.DAY_OF_YEAR, -1)
        val yesterdayStr = dateFormat.format(cal.time)

        // Check if current streak is active today or yesterday
        val streakActiveFrom: Calendar = when {
            activeDates.contains(todayStr) -> Calendar.getInstance()
            activeDates.contains(yesterdayStr) -> Calendar.getInstance().apply { add(Calendar.DAY_OF_YEAR, -1) }
            else -> return 0 // Streak broken if neither today nor yesterday has activity/rest day
        }

        var streak = 0
        val checkCal = Calendar.getInstance().apply { time = streakActiveFrom.time }

        while (true) {
            val dateStr = dateFormat.format(checkCal.time)
            if (activeDates.contains(dateStr)) {
                streak++
                checkCal.add(Calendar.DAY_OF_YEAR, -1)
            } else {
                break
            }
        }

        return streak
    }

    fun workoutsThisMonth(workouts: List<WorkoutWithExercises>): Int {
        val currentMonth = Calendar.getInstance().get(Calendar.MONTH)
        val currentYear = Calendar.getInstance().get(Calendar.YEAR)
        return workouts.count {
            val cal = Calendar.getInstance().apply { timeInMillis = it.workout.dateMillis }
            cal.get(Calendar.MONTH) == currentMonth && cal.get(Calendar.YEAR) == currentYear
        }
    }
}
