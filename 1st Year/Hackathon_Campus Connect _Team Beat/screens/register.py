"""
Registration screen for CampusConnect application.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from core.database import jload, jsave, F_USERS, hash_pw, today
from core.theme import COLORS as C, FONTS as F
from ui.widgets import entry, btn, sep, scrollable_frame, lbl


class RegisterScreen(tk.Frame):
    """Registration screen for new user accounts."""

    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self._build()

    def _build(self):
        outer, inner = scrollable_frame(self)
        outer.pack(fill="both", expand=True)

        form = tk.Frame(inner, bg=C["bg"])
        form.pack(pady=40, padx=80, anchor="n", fill="x")

        tk.Label(
            form,
            text="🎓 Create Account",
            font=("Segoe UI", 24, "bold"),
            fg=C["accent"],
            bg=C["bg"]
        ).pack(anchor="w")
        tk.Label(
            form,
            text="Join the CampusConnect portal",
            font=F["body"],
            fg=C["muted"],
            bg=C["bg"]
        ).pack(anchor="w", pady=(4, 24))

        self._vars = {}
        fields = [
            ("Full Name", "name", ""),
            ("Username", "username", ""),
            ("Email Address", "email", ""),
            ("Password", "password", "*"),
            ("Course / Program", "course", ""),
        ]
        # two-column layout
        cols = tk.Frame(form, bg=C["bg"])
        cols.pack(fill="x")
        left_col = tk.Frame(cols, bg=C["bg"])
        left_col.pack(side="left", fill="x", expand=True, padx=(0, 20))
        right_col = tk.Frame(cols, bg=C["bg"])
        right_col.pack(side="left", fill="x", expand=True)

        for i, (lbl_txt, key, show) in enumerate(fields):
            col = left_col if i % 2 == 0 else right_col
            tk.Label(
                col,
                text=lbl_txt,
                font=F["body"],
                fg=C["muted"],
                bg=C["bg"]
            ).pack(anchor="w", pady=(10, 2))
            v = tk.StringVar()
            self._vars[key] = v
            entry(col, var=v, show=show, w=28).pack(ipady=9, fill="x", anchor="w")

        # Year level – full width
        tk.Label(
            form,
            text="Year Level",
            font=F["body"],
            fg=C["muted"],
            bg=C["bg"]
        ).pack(anchor="w", pady=(14, 2))
        self._year = tk.StringVar(value="1st Year")
        ttk.Combobox(
            form,
            textvariable=self._year,
            values=["1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year"],
            state="readonly",
            font=F["body"],
            width=20
        ).pack(ipady=6, anchor="w")

        # Bio
        tk.Label(
            form,
            text="Short Bio (optional)",
            font=F["body"],
            fg=C["muted"],
            bg=C["bg"]
        ).pack(anchor="w", pady=(14, 2))
        self._bio = scrolledtext.ScrolledText(
            form,
            height=2,
            width=60,
            font=F["body"],
            bg=C["surface"],
            fg=C["text"],
            insertbackground=C["text"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=C["border"]
        )
        self._bio.pack(fill="x")

        tk.Frame(form, bg=C["bg"], height=20).pack()
        btn(form, "Create My Account →", self._register,
            bg=C["green"], pady=12).pack(anchor="w")

        tk.Frame(form, bg=C["bg"], height=12).pack()
        row = tk.Frame(form, bg=C["bg"])
        row.pack(anchor="w")
        tk.Label(
            row,
            text="Already have an account?",
            font=F["body"],
            fg=C["muted"],
            bg=C["bg"]
        ).pack(side="left")
        lb = tk.Label(
            row,
            text=" Sign in",
            font=("Segoe UI", 11, "underline"),
            fg=C["accent"],
            bg=C["bg"],
            cursor="hand2"
        )
        lb.pack(side="left")
        lb.bind("<Button-1>", lambda e: self.master.go_login())

        self._err = tk.Label(
            form,
            text="",
            font=F["sm"],
            fg=C["red"],
            bg=C["bg"]
        )
        self._err.pack(anchor="w", pady=(10, 0))

    def _register(self):
        users = jload(F_USERS)
        v = self._vars
        name = v["name"].get().strip()
        un = v["username"].get().strip()
        email = v["email"].get().strip()
        pw = v["password"].get().strip()
        course = v["course"].get().strip()
        bio = self._bio.get("1.0", "end").strip()

        if not all([name, un, email, pw, course]):
            self._err.config(text="⚠  All fields except bio are required")
            return
        if un in users:
            self._err.config(text="⚠  Username already taken")
            return
        if "@" not in email:
            self._err.config(text="⚠  Enter a valid email address")
            return
        if len(pw) < 6:
            self._err.config(text="⚠  Password must be at least 6 characters")
            return

        users[un] = {
            "id": un,
            "name": name,
            "email": email,
            "password": hash_pw(pw),
            "role": "student",
            "course": course,
            "year": self._year.get(),
            "joined": today(),
            "avatar": "👤",
            "points": 0,
            "bio": bio,
        }
        jsave(F_USERS, users)
        messagebox.showinfo("Account Created!", f"Welcome to CampusConnect, {name}!\nYou can now sign in.")
        self.master.go_login()
