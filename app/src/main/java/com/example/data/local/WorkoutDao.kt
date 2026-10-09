package com.example.data.local

import androidx.room.Dao
import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Transaction
import androidx.room.Update
import com.example.data.model.Exercise
import com.example.data.model.SetLog
import com.example.data.model.Workout
import com.example.data.model.WorkoutWithExercises
import kotlinx.coroutines.flow.Flow

@Dao
interface WorkoutDao {
    @Transaction
    @Query("SELECT * FROM workouts ORDER BY dateMillis DESC")
    fun getAllWorkouts(): Flow<List<WorkoutWithExercises>>

    @Transaction
    @Query("SELECT * FROM workouts WHERE id = :workoutId")
    fun getWorkoutById(workoutId: Long): Flow<WorkoutWithExercises?>

    @Query("SELECT * FROM workouts WHERE isCompleted = 0 ORDER BY dateMillis DESC LIMIT 1")
    fun getActiveWorkout(): Flow<Workout?>

    @Transaction
    @Query("SELECT * FROM workouts WHERE isCompleted = 1 ORDER BY dateMillis DESC")
    fun getCompletedWorkouts(): Flow<List<WorkoutWithExercises>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertWorkout(workout: Workout): Long

    @Update
    suspend fun updateWorkout(workout: Workout)

    @Delete
    suspend fun deleteWorkout(workout: Workout)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertExercise(exercise: Exercise): Long

    @Update
    suspend fun updateExercise(exercise: Exercise)

    @Delete
    suspend fun deleteExercise(exercise: Exercise)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertSetLog(setLog: SetLog): Long

    @Update
    suspend fun updateSetLog(setLog: SetLog)

    @Delete
    suspend fun deleteSetLog(setLog: SetLog)
    
    // For comparing previous performance
    @Transaction
    @Query("""
        SELECT e.* FROM exercises e
        INNER JOIN workouts w ON e.workoutId = w.id
        WHERE e.name = :exerciseName AND w.isCompleted = 1 AND w.id != :currentWorkoutId
        ORDER BY w.dateMillis DESC LIMIT 1
    """)
    suspend fun getPreviousExerciseSession(exerciseName: String, currentWorkoutId: Long): Exercise?
    
    @Query("SELECT * FROM set_logs WHERE exerciseId = :exerciseId ORDER BY setNumber ASC")
    suspend fun getSetsForExercise(exerciseId: Long): List<SetLog>
}
