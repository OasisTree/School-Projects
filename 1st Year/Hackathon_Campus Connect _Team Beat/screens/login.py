"""
Login screen for CampusConnect application.
"""

import tkinter as tk
from core.database import jload, F_USERS, hash_pw
from core.theme import COLORS as C, FONTS as F
from ui.widgets import entry, btn, sep, lbl


class LoginScreen(tk.Frame):
    """Login screen with demo account quick-access panel."""

    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self._build()

    def _build(self):
        # ── left decorative panel ──
        left = tk.Frame(self, bg=C["surface"], width=440)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        tk.Frame(left, bg=C["surface"], height=60).pack()
        tk.Label(
            left, text="🎓", font=("Segoe UI", 72), bg=C["surface"], fg=C["accent"]
        ).pack(pady=(40, 8))
        tk.Label(
            left,
            text="CampusConnect",
            font=("Segoe UI", 26, "bold"),
            fg=C["text"],
            bg=C["surface"],
        ).pack()
        tk.Label(
            left,
            text="Student Engagement Portal",
            font=F["body"],
            fg=C["muted"],
            bg=C["surface"],
        ).pack(pady=(4, 32))
        sep(left).pack(fill="x", padx=40)
        tk.Frame(left, bg=C["surface"], height=16).pack()

        tk.Label(
            left,
            text="DEMO ACCOUNTS",
            font=("Segoe UI", 9, "bold"),
            fg=C["dim"],
            bg=C["surface"],
        ).pack(anchor="w", padx=40, pady=(8, 4))

        demo_accounts = [
            ("🏛️", "Admin", "admin1", "admin123", C["yellow"]),
            ("🌿", "Org – EcoGreen", "org1", "org123", C["green"]),
            ("💻", "Org – TechHub", "org2", "org123", C["purple"]),
            ("👨‍💻", "Student – Juan", "student1", "student123", C["accent"]),
            ("🌺", "Student – Ana", "student2", "student123", C["accent"]),
        ]
        for ico, role, un, pw, col in demo_accounts:
            row = tk.Frame(left, bg=C["card"], cursor="hand2")
            row.pack(fill="x", padx=32, pady=3)
            tk.Label(
                row,
                text=ico,
                font=("Segoe UI", 18),
                bg=C["card"],
                fg=C["text"],
                padx=10,
                pady=7,
            ).pack(side="left")
            c = tk.Frame(row, bg=C["card"])
            c.pack(side="left", pady=6)
            tk.Label(c, text=role, font=F["bold"], fg=C["text"], bg=C["card"]).pack(
                anchor="w"
            )
            tk.Label(
                c, text=f"{un} / {pw}", font=F["sm"], fg=C["muted"], bg=C["card"]
            ).pack(anchor="w")
            tk.Frame(row, bg=col, width=4).pack(side="right", fill="y")

            def _click(u=un, p=pw, r=row):
                self._un.set(u)
                self._pw.set(p)

            for w in [row] + list(row.winfo_children()):
                w.bind("<Button-1>", lambda e, fn=_click: fn())
                w.bind("<Enter>", lambda e, r=row: r.config(bg=C["hover"]))
                w.bind("<Leave>", lambda e, r=row: r.config(bg=C["card"]))

        # ── right login form ──
        right = tk.Frame(self, bg=C["bg"])
        right.pack(side="left", fill="both", expand=True)

        form = tk.Frame(right, bg=C["bg"])
        form.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            form,
            text="Welcome back",
            font=("Segoe UI", 28, "bold"),
            fg=C["text"],
            bg=C["bg"],
        ).pack(anchor="w")
        tk.Label(
            form,
            text="Sign in to access your portal",
            font=F["body"],
            fg=C["muted"],
            bg=C["bg"],
        ).pack(anchor="w", pady=(4, 32))

        self._un = tk.StringVar()
        self._pw = tk.StringVar()

        tk.Label(form, text="Username", font=F["body"], fg=C["muted"], bg=C["bg"]).pack(
            anchor="w"
        )
        un_e = entry(form, var=self._un, w=34)
        un_e.pack(ipady=10, fill="x", pady=(2, 14))

        tk.Label(form, text="Password", font=F["body"], fg=C["muted"], bg=C["bg"]).pack(
            anchor="w"
        )
        pw_e = entry(form, var=self._pw, w=34, show="*")
        pw_e.pack(ipady=10, fill="x", pady=(2, 0))
        pw_e.bind("<Return>", lambda e: self._login())

        tk.Frame(form, bg=C["bg"], height=24).pack()
        btn(form, "  Sign In  →", self._login, bg=C["accent"], padx=0, pady=12).pack(
            fill="x"
        )

        tk.Frame(form, bg=C["bg"], height=12).pack()
        row2 = tk.Frame(form, bg=C["bg"])
        row2.pack()
        tk.Label(
            row2,
            text="Don't have an account?",
            font=F["body"],
            fg=C["muted"],
            bg=C["bg"],
        ).pack(side="left")
        rb = tk.Label(
            row2,
            text=" Register here",
            font=("Segoe UI", 11, "underline"),
            fg=C["accent"],
            bg=C["bg"],
            cursor="hand2",
        )
        rb.pack(side="left")
        rb.bind("<Button-1>", lambda e: self.master.go_register())

        self._err = tk.Label(form, text="", font=F["sm"], fg=C["red"], bg=C["bg"])
        self._err.pack(pady=(12, 0))

    def _login(self):
        users = jload(F_USERS)
        un = self._un.get().strip()
        pw = self._pw.get().strip()
        if un in users and users[un]["password"] == hash_pw(pw):
            self.master.current_user = users[un]
            self.master.go_dashboard()
        else:
            self._err.config(text="⚠  Invalid username or password")
