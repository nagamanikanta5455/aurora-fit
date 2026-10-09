package com.example

import android.content.Context
import androidx.room.Room
import com.example.data.local.AppDatabase
import com.example.data.local.WorkoutRepository

object Graph {
    lateinit var database: AppDatabase
        private set
    lateinit var appContext: Context
        private set

    val repository by lazy {
        WorkoutRepository(database.workoutDao())
    }

    fun provide(context: Context) {
        appContext = context.applicationContext
        database = Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "aurorafit.db"
        ).fallbackToDestructiveMigration().build()
    }
}
