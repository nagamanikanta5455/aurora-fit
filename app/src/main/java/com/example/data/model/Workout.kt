package com.example.data.model

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "workouts")
data class Workout(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val name: String = "New Workout",
    val dateMillis: Long = System.currentTimeMillis(),
    val notes: String = "",
    val isCompleted: Boolean = false
)
