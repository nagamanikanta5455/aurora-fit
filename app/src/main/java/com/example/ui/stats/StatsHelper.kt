package com.example.ui.stats

import com.example.data.model.WorkoutWithExercises
import java.util.Calendar

object StatsHelper {
    fun calculateStreak(workouts: List<WorkoutWithExercises>): Int {
        if (workouts.isEmpty()) return 0
        val sortedDates = workouts.map {
            val cal = Calendar.getInstance().apply { timeInMillis = it.workout.dateMillis }
            cal.set(Calendar.HOUR_OF_DAY, 0)
            cal.set(Calendar.MINUTE, 0)
            cal.set(Calendar.SECOND, 0)
            cal.set(Calendar.MILLISECOND, 0)
            cal.timeInMillis
        }.distinct().sortedDescending()
        
        var streak = 0
        var currentExpected = Calendar.getInstance().apply {
            set(Calendar.HOUR_OF_DAY, 0)
            set(Calendar.MINUTE, 0)
            set(Calendar.SECOND, 0)
            set(Calendar.MILLISECOND, 0)
        }.timeInMillis

        var i = 0
        // check if today is done, if not, maybe yesterday
        if (sortedDates.isNotEmpty() && sortedDates[0] == currentExpected) {
            streak++
            i++
            currentExpected -= 24 * 60 * 60 * 1000
        } else if (sortedDates.isNotEmpty() && sortedDates[0] == currentExpected - 24 * 60 * 60 * 1000) {
            currentExpected -= 24 * 60 * 60 * 1000
        } else {
            return 0
        }
        
        while (i < sortedDates.size) {
            if (sortedDates[i] == currentExpected) {
                streak++
                currentExpected -= 24 * 60 * 60 * 1000
                i++
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
