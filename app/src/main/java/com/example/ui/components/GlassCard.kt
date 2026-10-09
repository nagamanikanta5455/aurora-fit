package com.example.ui.components

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.shadow
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Shape
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp

/**
 * Clean GlassCard component implementing unified dark glassmorphic styling
 * Container color: Color(0x1F1E293B) in dark mode, Color(0xF0F8FAFC) in light mode.
 * Border: BorderStroke(1.dp, Color.White.copy(alpha = 0.1f)).
 * Corner radius: 24.dp.
 * Soft shadow: elevation = 6.dp, spotColor = Color(0x40000000).
 */
@Composable
fun GlassCard(
    modifier: Modifier = Modifier,
    shape: Shape = RoundedCornerShape(24.dp),
    elevation: Dp = 6.dp,
    content: @Composable () -> Unit
) {
    val isDark = isSystemInDarkTheme()
    val containerColor = if (isDark) Color(0x1F1E293B) else Color(0xF0F8FAFC)
    val borderColor = if (isDark) Color.White.copy(alpha = 0.1f) else Color(0xFFCBD5E1).copy(alpha = 0.4f)

    Card(
        modifier = modifier.shadow(
            elevation = elevation,
            shape = shape,
            spotColor = Color(0x40000000),
            ambientColor = Color(0x1A000000)
        ),
        shape = shape,
        colors = CardDefaults.cardColors(containerColor = containerColor),
        border = BorderStroke(1.dp, borderColor)
    ) {
        content()
    }
}
