"""
Theme module for CampusConnect - colors, fonts, and style constants.
"""

# ─────────────────────────── COLORS ────────────────────────────────────────
COLORS = {
    "bg": "#0D1117",  # Main background
    "surface": "#161B22",  # Secondary background
    "card": "#21262D",  # Card background
    "border": "#30363D",  # Border color
    "hover": "#2D333B",  # Hover state
    "accent": "#58A6FF",  # Primary accent (blue)
    "green": "#3FB950",  # Success/positive
    "yellow": "#D29922",  # Warning/attention
    "red": "#F85149",  # Error/danger
    "purple": "#BC8CFF",  # Tertiary accent
    "orange": "#F78166",  # Secondary accent
    "teal": "#39D353",  # Health/wellness
    "text": "#E6EDF3",  # Main text
    "muted": "#8B949E",  # Muted text
    "dim": "#484F58",  # Very muted text
}

# ─────────────────────────── FONTS ─────────────────────────────────────────
FONTS = {
    "h1": ("Segoe UI", 22, "bold"),  # Headings level 1
    "h2": ("Segoe UI", 16, "bold"),  # Headings level 2
    "h3": ("Segoe UI", 13, "bold"),  # Headings level 3
    "h3i": ("Segoe UI", 13, "italic"),  # Headings level 3 italic
    "body": ("Segoe UI", 11),  # Body text
    "sm": ("Segoe UI", 9),  # Small text
    "bold": ("Segoe UI", 11, "bold"),  # Bold body
    "mono": ("Consolas", 10),  # Monospace
}

# ─────────────────────────── CATEGORY COLORS ───────────────────────────────
CATEGORY_COLORS = {
    "Environmental": COLORS["green"],
    "Academic": COLORS["accent"],
    "Community": COLORS["yellow"],
    "Cultural": COLORS["purple"],
    "Sports": COLORS["orange"],
    "Health": COLORS["teal"],
}

# Aliases for convenience
C = COLORS
F = FONTS
CAT_COLOR = CATEGORY_COLORS
