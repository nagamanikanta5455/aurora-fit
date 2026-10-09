package com.example

import android.app.Application

class AuroraFitApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        Graph.provide(this)
    }
}
