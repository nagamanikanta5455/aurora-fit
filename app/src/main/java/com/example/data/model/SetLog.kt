package com.example.data.model

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.PrimaryKey
import androidx.room.Index

@Entity(
    tableName = "set_logs",
    foreignKeys = [
        ForeignKey(
            entity = Exercise::class,
            parentColumns = ["id"],
            childColumns = ["exerciseId"],
            onDelete = ForeignKey.CASCADE
        )
    ],
    indices = [Index("exerciseId")]
)
data class SetLog(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val exerciseId: Long,
    val setNumber: Int,
    val weight: Float? = null,
    val reps: Int? = null,
    val addedWeight: Float? = null,
    val durationSeconds: Int? = null,
    val isCompleted: Boolean = false
) {
    fun getVolume(): Float {
        val w = weight ?: 0f
        val aw = addedWeight ?: 0f
        val r = reps ?: 0
        return (w + aw) * r
    }
}
