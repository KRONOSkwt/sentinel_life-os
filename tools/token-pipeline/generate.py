#!/usr/bin/env python3
"""Generate CSS custom properties and Compose theme from tokens.json"""
import json
import sys
from pathlib import Path

def rgba_to_hex(rgba: str) -> str:
    """Convert rgba(...) or rgb(...) to 8-char hex (ARGB)."""
    import re
    if rgba.startswith('#'):
        # Already hex, assume full opacity
        if len(rgba) == 7:
            return 'ff' + rgba[1:]
        return rgba[1:]  # remove #
    match = re.match(r'rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)', rgba)
    if not match:
        raise ValueError(f"Cannot convert {rgba} to hex")
    r, g, b = map(int, match.groups()[:3])
    alpha_str = match.groups()[3]
    if alpha_str is None:
        a = 255
    else:
        a = int(float(alpha_str) * 255)
    return f'{a:02x}{r:02x}{g:02x}{b:02x}'

def generate_css(tokens: dict) -> str:
    lines = [":root {"]
    # Colors
    for group, values in tokens["colors"].items():
        for key, value in values.items():
            var_name = f"--{group}-{key}"
            lines.append(f"  {var_name}: {value};")
    # Spacing
    for key, value in tokens["spacing"].items():
        lines.append(f"  --spacing-{key}: {value}px;")
    # Radius
    for key, value in tokens["radius"].items():
        lines.append(f"  --radius-{key}: {value}px;")
    # Typography
    lines.append(f"  --font-family: {tokens['typography']['fontFamily']};")
    for key, value in tokens["typography"]["sizes"].items():
        lines.append(f"  --font-size-{key}: {value}px;")
    for key, value in tokens["typography"]["weights"].items():
        lines.append(f"  --font-weight-{key}: {value};")
    lines.append("}")
    return "\n".join(lines)

def generate_compose_theme(tokens: dict) -> str:
    """Generate Kotlin Theme.kt from tokens.json"""
    colors = tokens["colors"]
    spacing = tokens["spacing"]
    radius = tokens["radius"]

    # Convert glass colors to hex for Compose (they are rgba strings)
    glass_background_hex = rgba_to_hex(colors["glass"]["background"])
    glass_card_background_hex = rgba_to_hex(colors["glass"]["background-card"])
    glass_border_hex = rgba_to_hex(colors["glass"]["border"])
    
    return f'''package com.sentinel.lifeos.ui.theme

import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

// Generated from design tokens — DO NOT EDIT
object TokenColors {{
    val GlassBackground = Color(0x{glass_background_hex})
    val GlassCardBackground = Color(0x{glass_card_background_hex})
    val GlassBorder = Color(0x{glass_border_hex})
    val AccentPrimary = Color.parseColor("{colors["accent"]["primary"]}")
    val AccentSecondary = Color.parseColor("{colors["accent"]["secondary"]}")
    val SurfaceBackground = Color.parseColor("{colors["surface"]["background"]}")
    val SurfaceCard = Color.parseColor("{colors["surface"]["card"]}")
    val TextPrimary = Color.parseColor("{colors["surface"]["text"]}")
    val TextSecondary = Color.parseColor("{colors["surface"]["text-secondary"]}")
}}

object TokenSpacing {{
    val Xs = {spacing["xs"]}.dp
    val Sm = {spacing["sm"]}.dp
    val Md = {spacing["md"]}.dp
    val Lg = {spacing["lg"]}.dp
    val Xl = {spacing["xl"]}.dp
}}

object TokenRadius {{
    val Sm = {radius["sm"]}.dp
    val Md = {radius["md"]}.dp
    val Lg = {radius["lg"]}.dp
    val Xl = {radius["xl"]}.dp
}}
'''

if __name__ == "__main__":
    # Assume script runs from project root
    tokens_path = Path("libs/shared/tokens/tokens.json")
    if not tokens_path.exists():
        print(f"Error: {tokens_path} not found", file=sys.stderr)
        sys.exit(1)
    
    with open(tokens_path) as f:
        tokens = json.load(f)
    
    # Generate CSS
    css = generate_css(tokens)
    css_output = Path("apps/web/src/styles/_tokens.css")
    css_output.parent.mkdir(parents=True, exist_ok=True)
    with open(css_output, "w") as f:
        f.write(css)
    print(f"Generated {css_output}")
    
    # Generate Compose theme
    compose = generate_compose_theme(tokens)
    compose_output = Path("apps/android/app/src/main/java/com/sentinel/lifeos/ui/theme/Theme.kt")
    with open(compose_output, "w") as f:
        f.write(compose)
    print(f"Generated {compose_output}")