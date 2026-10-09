package com.example.data.local

import com.example.data.model.Exercise
import com.example.data.model.SetLog
import com.example.data.model.Workout
import com.example.data.model.ExerciseWithSets
import com.example.data.model.WorkoutWithExercises
import kotlinx.coroutines.flow.Flow

class WorkoutRepository(private val workoutDao: WorkoutDao) {
    val allWorkouts: Flow<List<WorkoutWithExercises>> = workoutDao.getAllWorkouts()
    val completedWorkouts: Flow<List<WorkoutWithExercises>> = workoutDao.getCompletedWorkouts()
    val activeWorkout: Flow<Workout?> = workoutDao.getActiveWorkout()

    fun getWorkoutById(id: Long) = workoutDao.getWorkoutById(id)

    suspend fun insertWorkout(workout: Workout): Long = workoutDao.insertWorkout(workout)
    suspend fun updateWorkout(workout: Workout) = workoutDao.updateWorkout(workout)
    suspend fun deleteWorkout(workout: Workout) = workoutDao.deleteWorkout(workout)

    suspend fun insertExercise(exercise: Exercise): Long = workoutDao.insertExercise(exercise)
    suspend fun updateExercise(exercise: Exercise) = workoutDao.updateExercise(exercise)
    suspend fun deleteExercise(exercise: Exercise) = workoutDao.deleteExercise(exercise)

    suspend fun insertSetLog(setLog: SetLog): Long = workoutDao.insertSetLog(setLog)
    suspend fun updateSetLog(setLog: SetLog) = workoutDao.updateSetLog(setLog)
    suspend fun deleteSetLog(setLog: SetLog) = workoutDao.deleteSetLog(setLog)

    suspend fun getPreviousExerciseSession(exerciseName: String, currentWorkoutId: Long): ExerciseWithSets? {
        val prevExercise = workoutDao.getPreviousExerciseSession(exerciseName, currentWorkoutId) ?: return null
        val sets = workoutDao.getSetsForExercise(prevExercise.id)
        return ExerciseWithSets(prevExercise, sets)
    }
}
