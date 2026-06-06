"""
Utility functions for CampusConnect application.
"""

from core.theme import COLORS, FONTS, CATEGORY_COLORS


def get_level(pts):
    """Get user level and color based on points."""
    if pts >= 1000:
        return "Platinum", COLORS["purple"]
    if pts >= 500:
        return "Gold", COLORS["yellow"]
    if pts >= 200:
        return "Silver", COLORS["muted"]
    return "Bronze", COLORS["orange"]


def get_bg(widget):
    """Get background color of a widget."""
    try:
        return widget.cget("bg")
    except Exception:
        return COLORS["bg"]
