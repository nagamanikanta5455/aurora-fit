package com.example.ui.theme

import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color

// Glassmorphism Surfaces
val GlassSurfaceDark = Color(0x1F1E293B) // rgba(30, 41, 59, 0.12)
val GlassSurfaceLight = Color(0xCBF8FAFC) // rgba(248, 250, 252, 0.8)

// Neon & Gradient Accents
val ElectricViolet = Color(0xFF8B5CF6)
val ElectricCyan = Color(0xFF06B6D4)
val FlameOrange = Color(0xFFF97316)
val EmeraldGreen = Color(0xFF10B981)

// Gradient Brushes
val PrimaryAccentGradient = Brush.linearGradient(
    listOf(ElectricViolet, ElectricCyan)
)

val StreakBadgeGradient = Brush.linearGradient(
    listOf(Color(0xFFF97316), Color(0xFFFBBF24))
)

val CompletedBadgeGradient = Brush.linearGradient(
    listOf(Color(0xFF10B981), Color(0xFF34D399))
)

val GlassBorderBrush = Brush.linearGradient(
    listOf(
        Color.White.copy(alpha = 0.18f),
        Color.White.copy(alpha = 0.04f)
    )
)

val DarkMeshBackgroundGradient = Brush.linearGradient(
    colors = listOf(
        Color(0xFF0F172A),
        Color(0xFF1E1B4B),
        Color(0xFF022C22)
    )
)

val LightMeshBackgroundGradient = Brush.linearGradient(
    colors = listOf(
        Color(0xFFF8FAFC),
        Color(0xFFE0E7FF),
        Color(0xFFD1FAE5)
    )
)

// Legacy compatibility values
val LightBg = Color(0xFFF8FAFC)
val LightSurface = Color(0xFFFFFFFF)
val AuroraMint = Color(0xFFD1FAE5)
val AuroraLavender = Color(0xFFE0E7FF)
val AuroraBlue = Color(0xFFE3F2FD)
val TextPrimary = Color(0xFF0F172A)
val TextSecondary = Color(0xFF64748B)
val SpatialBorder = Color(0xFFE2E8F0)
val AccentPrimary = Color(0xFF8B5CF6)
val SuccessGreen = Color(0xFF10B981)
