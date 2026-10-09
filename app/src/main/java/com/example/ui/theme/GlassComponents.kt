package com.example.ui.theme

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp

@Composable
fun GlassCard(
    modifier: Modifier = Modifier,
    cornerRadius: Dp = 28.dp,
    elevation: Dp = 12.dp,
    content: @Composable () -> Unit
) {
    val isDark = isSystemInDarkTheme()
    val containerColor = if (isDark) GlassSurfaceDark else GlassSurfaceLight
    val borderBrush = if (isDark) {
        Brush.linearGradient(
            listOf(
                Color.White.copy(alpha = 0.15f),
                Color.Transparent
            )
        )
    } else {
        Brush.linearGradient(
            listOf(
                Color.White.copy(alpha = 0.8f),
                Color(0xFFE2E8F0).copy(alpha = 0.5f)
            )
        )
    }

    Card(
        modifier = modifier.shadow(
            elevation = elevation,
            shape = RoundedCornerShape(cornerRadius),
            spotColor = Color(0x40000000),
            ambientColor = Color(0x1A000000)
        ),
        shape = RoundedCornerShape(cornerRadius),
        colors = CardDefaults.cardColors(containerColor = containerColor),
        border = BorderStroke(1.dp, borderBrush)
    ) {
        content()
    }
}
