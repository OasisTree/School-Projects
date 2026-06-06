"""
Main application module for CampusConnect - orchestrates screen management and user sessions.
"""

import tkinter as tk
from core.database import seed
from core.theme import COLORS as C
from screens.login import LoginScreen
from screens.register import RegisterScreen
from screens.dashboards import AdminDashboard
from screens.dashboards_extended import OrgDashboard, StudentDashboard


class App(tk.Tk):
    """Main application window managing screen transitions and user state."""

    def __init__(self):
        super().__init__()
        self.title("CampusConnect – Student Engagement Portal")
        self.geometry("1320x820")
        self.minsize(1100, 700)
        self.configure(bg=C["bg"])
        self.current_user = None
        self._frame = None

        # Initialize database with seed data
        seed()

        # Show login screen
        self._show(LoginScreen)

    def _show(self, Cls, **kw):
        """Switch to a different screen by destroying the current frame and creating a new one."""
        if self._frame:
            self._frame.destroy()
        self._frame = Cls(self, **kw)
        self._frame.pack(fill="both", expand=True)

    def go_login(self):
        """Navigate to login screen."""
        self.current_user = None
        self._show(LoginScreen)

    def go_register(self):
        """Navigate to registration screen."""
        self._show(RegisterScreen)

    def go_dashboard(self):
        """Navigate to the appropriate dashboard based on user role."""
        role = self.current_user["role"]
        if role == "admin":
            self._show(AdminDashboard)
        elif role == "org":
            self._show(OrgDashboard)
        else:
            self._show(StudentDashboard)


if __name__ == "__main__":
    app = App()
    app.mainloop()
