package com.example.data.local

import androidx.room.Database
import androidx.room.RoomDatabase
import com.example.data.model.Exercise
import com.example.data.model.SetLog
import com.example.data.model.Workout

@Database(entities = [Workout::class, Exercise::class, SetLog::class], version = 1, exportSchema = false)
abstract class AppDatabase : RoomDatabase() {
    abstract fun workoutDao(): WorkoutDao
}
