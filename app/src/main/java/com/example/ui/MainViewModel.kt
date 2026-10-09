package com.example.ui

import android.content.Context
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.example.Graph
import com.example.data.local.WorkoutRepository
import com.example.data.model.Exercise
import com.example.data.model.ExerciseType
import com.example.data.model.ExerciseWithSets
import com.example.data.model.SetLog
import com.example.data.model.Workout
import com.example.data.model.WorkoutWithExercises
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class MainViewModel(private val repository: WorkoutRepository) : ViewModel() {

    private val prefs = Graph.appContext.getSharedPreferences("theme_prefs", Context.MODE_PRIVATE)
    private val _isDarkMode = MutableStateFlow(prefs.getBoolean("is_dark_mode", false))
    val isDarkMode: StateFlow<Boolean> = _isDarkMode.asStateFlow()

    fun toggleTheme() {
        val newValue = !_isDarkMode.value
        _isDarkMode.value = newValue
        prefs.edit().putBoolean("is_dark_mode", newValue).apply()
    }


    val allWorkouts: StateFlow<List<WorkoutWithExercises>> = repository.allWorkouts
        .stateIn(viewModelScope, SharingStarted.Lazily, emptyList())

    val activeWorkout: StateFlow<Workout?> = repository.activeWorkout
        .stateIn(viewModelScope, SharingStarted.Lazily, null)

    private val _activeWorkoutDetails = MutableStateFlow<WorkoutWithExercises?>(null)
    val activeWorkoutDetails: StateFlow<WorkoutWithExercises?> = _activeWorkoutDetails.asStateFlow()

    private val _previousSessions = MutableStateFlow<Map<Long, ExerciseWithSets>>(emptyMap())
    val previousSessions: StateFlow<Map<Long, ExerciseWithSets>> = _previousSessions.asStateFlow()

    private var detailsJob: kotlinx.coroutines.Job? = null

    init {
        viewModelScope.launch {
            activeWorkout.collect { workout ->
                detailsJob?.cancel()
                if (workout != null) {
                    val cal = java.util.Calendar.getInstance()
                    cal.timeInMillis = workout.dateMillis
                    val now = java.util.Calendar.getInstance()
                    if (cal.get(java.util.Calendar.YEAR) != now.get(java.util.Calendar.YEAR) || cal.get(java.util.Calendar.DAY_OF_YEAR) != now.get(java.util.Calendar.DAY_OF_YEAR)) {
                        cancelWorkout(workout)
                        return@collect
                    }
                    
                    detailsJob = launch {
                        repository.getWorkoutById(workout.id).collect { details ->
                            _activeWorkoutDetails.value = details
                            if (details != null) {
                                val newMap = mutableMapOf<Long, ExerciseWithSets>()
                                details.exercises.forEach { exWithSets ->
                                    val prev = repository.getPreviousExerciseSession(exWithSets.exercise.name, details.workout.id)
                                    if (prev != null) {
                                        newMap[exWithSets.exercise.id] = prev
                                    }
                                }
                                _previousSessions.value = newMap
                            }
                        }
                    }
                } else {
                    _activeWorkoutDetails.value = null
                    _previousSessions.value = emptyMap()
                }
            }
        }
    }

    fun startNewWorkout(isWeights: Boolean) {
        viewModelScope.launch {
            val name = if (isWeights) "Weights Workout" else "Bodyweight Workout"
            val workout = Workout(name = name)
            val id = repository.insertWorkout(workout)
        }
    }

    fun finishWorkout(workout: Workout) {
        viewModelScope.launch {
            repository.updateWorkout(workout.copy(isCompleted = true))
        }
    }
    
    fun cancelWorkout(workout: Workout) {
        viewModelScope.launch {
            repository.deleteWorkout(workout)
        }
    }

    fun addExerciseToActive(name: String, type: ExerciseType) {
        val currentWorkout = activeWorkout.value ?: return
        val currentDetails = activeWorkoutDetails.value ?: return
        val orderIndex = currentDetails.exercises.size
        viewModelScope.launch {
            repository.insertExercise(
                Exercise(workoutId = currentWorkout.id, name = name, type = type, orderIndex = orderIndex)
            )
        }
    }
    
    // Old fetch methods removed.

    fun updateExercise(exercise: Exercise) {
        viewModelScope.launch {
            repository.updateExercise(exercise)
        }
    }

    fun deleteExercise(exercise: Exercise) {
        viewModelScope.launch {
            repository.deleteExercise(exercise)
        }
    }

    fun addSetLog(exerciseId: Long, setNumber: Int) {
        viewModelScope.launch {
            repository.insertSetLog(
                SetLog(exerciseId = exerciseId, setNumber = setNumber)
            )
        }
    }

    fun updateSetLog(setLog: SetLog) {
        viewModelScope.launch {
            repository.updateSetLog(setLog)
        }
    }
    
    fun deleteSetLog(setLog: SetLog) {
        viewModelScope.launch {
            repository.deleteSetLog(setLog)
        }
    }
    
    fun deleteWorkout(workout: Workout) {
        viewModelScope.launch {
            repository.deleteWorkout(workout)
        }
    }

    companion object {
        val Factory: ViewModelProvider.Factory = object : ViewModelProvider.Factory {
            @Suppress("UNCHECKED_CAST")
            override fun <T : ViewModel> create(modelClass: Class<T>): T {
                return MainViewModel(Graph.repository) as T
            }
        }
    }
}
