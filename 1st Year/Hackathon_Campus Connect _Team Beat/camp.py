"""
CampusConnect – Campus Engagement Portal
Main entry point for the application.

This application has been refactored into a modular architecture:
- core/: Database, theme, and utility modules
- ui/: UI widgets and popup windows
- screens/: Application screens (login, register, dashboards)
- app.py: Main application orchestrator
"""

from app import App

if __name__ == "__main__":
    app = App()
    app.mainloop()

from tkinter import ttk, messagebox, scrolledtext
import json, hashlib, datetime, uuid
from pathlib import Path

# ─────────────────────────── FILE PATHS ────────────────────────────────────
BASE = Path(__file__).parent
DATA = BASE / "data"
DATA.mkdir(exist_ok=True)

F_USERS = DATA / "users.json"
F_EVENTS = DATA / "events.json"
F_FORMS = DATA / "forms.json"
F_RESPONSES = DATA / "responses.json"
F_GROUPS = DATA / "groups.json"
F_MESSAGES = DATA / "messages.json"
F_ATTENDANCE = DATA / "attendance.json"
F_NOTIFS = DATA / "notifications.json"

# ─────────────────────────── THEME ─────────────────────────────────────────
C = {
    "bg": "#0D1117",
    "surface": "#161B22",
    "card": "#21262D",
    "border": "#30363D",
    "hover": "#2D333B",
    "accent": "#58A6FF",
    "green": "#3FB950",
    "yellow": "#D29922",
    "red": "#F85149",
    "purple": "#BC8CFF",
    "orange": "#F78166",
    "teal": "#39D353",
    "text": "#E6EDF3",
    "muted": "#8B949E",
    "dim": "#484F58",
}
F = {
    "h1": ("Segoe UI", 22, "bold"),
    "h2": ("Segoe UI", 16, "bold"),
    "h3": ("Segoe UI", 13, "bold"),
    "h3i": ("Segoe UI", 13, "italic"),
    "body": ("Segoe UI", 11),
    "sm": ("Segoe UI", 9),
    "bold": ("Segoe UI", 11, "bold"),
    "mono": ("Consolas", 10),
}
CAT_COLOR = {
    "Environmental": C["green"],
    "Academic": C["accent"],
    "Community": C["yellow"],
    "Cultural": C["purple"],
    "Sports": C["orange"],
    "Health": C["teal"],
}


# ─────────────────────────── JSON HELPERS ──────────────────────────────────
def jload(path):
    try:
        if path.exists():
            with open(path, encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def jsave(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()


def now_str():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def today():
    return datetime.datetime.now().strftime("%Y-%m-%d")


def push_notif(user_id, text, kind="info"):
    n = jload(F_NOTIFS)
    if user_id not in n:
        n[user_id] = []
    n[user_id].insert(
        0,
        {
            "id": uuid.uuid4().hex[:8],
            "text": text,
            "kind": kind,
            "time": now_str(),
            "read": False,
        },
    )
    n[user_id] = n[user_id][:30]  # keep last 30
    jsave(F_NOTIFS, n)


# ─────────────────────────── SEED DATA ─────────────────────────────────────
def seed():
    # ── users ──
    users = jload(F_USERS)
    if not users:
        users = {
            "admin1": {
                "id": "admin1",
                "name": "Dr. Maria Santos",
                "email": "admin@campus.edu",
                "password": hash_pw("admin123"),
                "role": "admin",
                "course": "",
                "year": "",
                "joined": today(),
                "avatar": "🏛️",
                "points": 0,
                "bio": "Campus Administrator",
            },
            "org1": {
                "id": "org1",
                "name": "EcoGreen Society",
                "email": "eco@campus.edu",
                "password": hash_pw("org123"),
                "role": "org",
                "course": "Environmental Science",
                "year": "",
                "joined": today(),
                "avatar": "🌿",
                "points": 0,
                "bio": "Promoting sustainability and environmental awareness on campus.",
            },
            "org2": {
                "id": "org2",
                "name": "TechHub Organization",
                "email": "tech@campus.edu",
                "password": hash_pw("org123"),
                "role": "org",
                "course": "Computer Science",
                "year": "",
                "joined": today(),
                "avatar": "💻",
                "points": 0,
                "bio": "Empowering students through technology and innovation.",
            },
            "org3": {
                "id": "org3",
                "name": "CommServe Club",
                "email": "comm@campus.edu",
                "password": hash_pw("org123"),
                "role": "org",
                "course": "Community Development",
                "year": "",
                "joined": today(),
                "avatar": "🤝",
                "points": 0,
                "bio": "Building a stronger community through service.",
            },
            "student1": {
                "id": "student1",
                "name": "Juan dela Cruz",
                "email": "juan@campus.edu",
                "password": hash_pw("student123"),
                "role": "student",
                "course": "BS Computer Science",
                "year": "2nd Year",
                "joined": today(),
                "avatar": "👨‍💻",
                "points": 150,
                "bio": "CS student passionate about open source.",
            },
            "student2": {
                "id": "student2",
                "name": "Ana Reyes",
                "email": "ana@campus.edu",
                "password": hash_pw("student123"),
                "role": "student",
                "course": "BS Environmental Science",
                "year": "3rd Year",
                "joined": today(),
                "avatar": "🌺",
                "points": 320,
                "bio": "Environmentalist and future scientist.",
            },
            "student3": {
                "id": "student3",
                "name": "Carlo Mendoza",
                "email": "carlo@campus.edu",
                "password": hash_pw("student123"),
                "role": "student",
                "course": "BS Information Technology",
                "year": "1st Year",
                "joined": today(),
                "avatar": "🎮",
                "points": 80,
                "bio": "Gamer turned developer.",
            },
        }
        jsave(F_USERS, users)

    # ── events ──
    events = jload(F_EVENTS)
    if not events:
        events = {
            "evt1": {
                "id": "evt1",
                "title": "Campus Tree Planting Drive",
                "org_id": "org1",
                "category": "Environmental",
                "date": "2025-05-15",
                "time": "8:00 AM",
                "location": "Campus Grounds",
                "description": "Join us in planting 500 trees around campus to promote sustainability and a greener environment for future generations.",
                "max_slots": 50,
                "registered": ["student1", "student2"],
                "status": "upcoming",
                "created": today(),
                "form_id": "form1",
                "tags": ["sustainability", "environment"],
                "points": 100,
            },
            "evt2": {
                "id": "evt2",
                "title": "Hackathon 2025",
                "org_id": "org2",
                "category": "Academic",
                "date": "2025-05-20",
                "time": "9:00 AM",
                "location": "IT Building, Room 301",
                "description": "24-hour hackathon open to all CS/IT students. Build innovative solutions for real campus problems. Prizes await the top teams!",
                "max_slots": 30,
                "registered": ["student1", "student3"],
                "status": "upcoming",
                "created": today(),
                "form_id": "form2",
                "tags": ["tech", "coding", "hackathon"],
                "points": 200,
            },
            "evt3": {
                "id": "evt3",
                "title": "Community Clean-Up Drive",
                "org_id": "org3",
                "category": "Community",
                "date": "2025-05-25",
                "time": "7:00 AM",
                "location": "Barangay Hall Plaza",
                "description": "Partner with local barangay officials to clean the surrounding community. Free breakfast provided for all volunteers!",
                "max_slots": 40,
                "registered": ["student2"],
                "status": "upcoming",
                "created": today(),
                "form_id": "form3",
                "tags": ["community", "service"],
                "points": 120,
            },
            "evt4": {
                "id": "evt4",
                "title": "Cultural Night 2025",
                "org_id": "org1",
                "category": "Cultural",
                "date": "2025-06-01",
                "time": "6:00 PM",
                "location": "Campus Amphitheater",
                "description": "Celebrate the diverse cultures of our campus community through music, dance, food, and art. All students are welcome to perform!",
                "max_slots": 100,
                "registered": [],
                "status": "upcoming",
                "created": today(),
                "form_id": None,
                "tags": ["culture", "arts"],
                "points": 60,
            },
        }
        jsave(F_EVENTS, events)

    # ── forms ──
    forms = jload(F_FORMS)
    if not forms:
        forms = {
            "form1": {
                "id": "form1",
                "event_id": "evt1",
                "title": "Tree Planting Registration",
                "questions": [
                    {
                        "id": "q1",
                        "text": "What is your preferred role?",
                        "type": "choice",
                        "options": [
                            "Tree Planter",
                            "Logistics",
                            "Documentation",
                            "First Aid",
                        ],
                        "assigns_to_group": True,
                        "required": True,
                    },
                    {
                        "id": "q2",
                        "text": "Do you have gardening experience?",
                        "type": "choice",
                        "options": ["Yes – regularly", "Yes – occasionally", "No"],
                        "assigns_to_group": False,
                        "required": True,
                    },
                    {
                        "id": "q3",
                        "text": "Shirt size for the event shirt:",
                        "type": "choice",
                        "options": ["XS", "S", "M", "L", "XL", "XXL"],
                        "assigns_to_group": False,
                        "required": True,
                    },
                    {
                        "id": "q4",
                        "text": "Any allergies or health concerns we should know?",
                        "type": "text",
                        "assigns_to_group": False,
                        "required": False,
                    },
                ],
            },
            "form2": {
                "id": "form2",
                "event_id": "evt2",
                "title": "Hackathon 2025 Registration",
                "questions": [
                    {
                        "id": "q1",
                        "text": "Select your track:",
                        "type": "choice",
                        "options": [
                            "Web Development",
                            "Mobile App",
                            "AI / Machine Learning",
                            "IoT / Hardware",
                        ],
                        "assigns_to_group": True,
                        "required": True,
                    },
                    {
                        "id": "q2",
                        "text": "Your primary programming language:",
                        "type": "choice",
                        "options": [
                            "Python",
                            "JavaScript",
                            "Java",
                            "C#",
                            "C++",
                            "Other",
                        ],
                        "assigns_to_group": False,
                        "required": True,
                    },
                    {
                        "id": "q3",
                        "text": "Do you already have a team?",
                        "type": "choice",
                        "options": [
                            "Yes – I have a full team",
                            "Yes – partial team",
                            "No – assign me",
                        ],
                        "assigns_to_group": False,
                        "required": True,
                    },
                    {
                        "id": "q4",
                        "text": "Briefly describe your project idea (optional):",
                        "type": "text",
                        "assigns_to_group": False,
                        "required": False,
                    },
                ],
            },
            "form3": {
                "id": "form3",
                "event_id": "evt3",
                "title": "Clean-Up Drive Sign-Up",
                "questions": [
                    {
                        "id": "q1",
                        "text": "Choose your assignment area:",
                        "type": "choice",
                        "options": [
                            "Street Cleaning",
                            "Park Area",
                            "River Bank",
                            "School Perimeter",
                        ],
                        "assigns_to_group": True,
                        "required": True,
                    },
                    {
                        "id": "q2",
                        "text": "Will you bring your own tools?",
                        "type": "choice",
                        "options": ["Yes", "No – I need equipment", "I'll share tools"],
                        "assigns_to_group": False,
                        "required": True,
                    },
                    {
                        "id": "q3",
                        "text": "Emergency contact number:",
                        "type": "text",
                        "assigns_to_group": False,
                        "required": True,
                    },
                ],
            },
        }
        jsave(F_FORMS, forms)

    # ── groups ──
    groups = jload(F_GROUPS)
    if not groups:
        groups = {
            "grp1": {
                "id": "grp1",
                "event_id": "evt1",
                "name": "Tree Planter",
                "members": ["student1", "org1"],
                "created": today(),
            },
            "grp2": {
                "id": "grp2",
                "event_id": "evt1",
                "name": "Documentation",
                "members": ["student2", "org1"],
                "created": today(),
            },
            "grp3": {
                "id": "grp3",
                "event_id": "evt2",
                "name": "Web Development",
                "members": ["student1", "student3", "org2"],
                "created": today(),
            },
        }
        jsave(F_GROUPS, groups)

    # ── messages ──
    msgs = jload(F_MESSAGES)
    if not msgs:
        msgs = {
            "grp1": [
                {
                    "sender_id": "org1",
                    "sender": "EcoGreen Society",
                    "text": "Welcome to the Tree Planting team! 🌱 Arrive by 7:45 AM sharp.",
                    "time": "2025-05-10 09:00",
                },
                {
                    "sender_id": "student1",
                    "sender": "Juan dela Cruz",
                    "text": "Got it! Should we bring our own gloves?",
                    "time": "2025-05-10 09:15",
                },
                {
                    "sender_id": "org1",
                    "sender": "EcoGreen Society",
                    "text": "Gloves are provided! Just bring water and sunscreen ☀️",
                    "time": "2025-05-10 09:20",
                },
            ],
            "grp2": [
                {
                    "sender_id": "org1",
                    "sender": "EcoGreen Society",
                    "text": "Hi Documentation team 📸 Please bring a camera or use your phone.",
                    "time": "2025-05-10 10:00",
                },
                {
                    "sender_id": "student2",
                    "sender": "Ana Reyes",
                    "text": "I have a DSLR! I'll make sure to take great shots 🎉",
                    "time": "2025-05-10 10:05",
                },
            ],
            "grp3": [
                {
                    "sender_id": "org2",
                    "sender": "TechHub Organization",
                    "text": "Web Dev track is looking strong this year 💻 Start brainstorming your ideas!",
                    "time": "2025-05-11 08:00",
                },
                {
                    "sender_id": "student1",
                    "sender": "Juan dela Cruz",
                    "text": "I was thinking a smart campus map app – real-time room availability?",
                    "time": "2025-05-11 08:15",
                },
                {
                    "sender_id": "student3",
                    "sender": "Carlo Mendoza",
                    "text": "That's fire! I can handle the frontend 🔥",
                    "time": "2025-05-11 08:20",
                },
            ],
        }
        jsave(F_MESSAGES, msgs)

    # ── attendance ──
    if not jload(F_ATTENDANCE):
        jsave(F_ATTENDANCE, {})

    # ── notifications ──
    notifs = jload(F_NOTIFS)
    if not notifs:
        notifs = {
            "student1": [
                {
                    "id": "n1",
                    "text": "You have been added to 'Tree Planter' group chat!",
                    "kind": "success",
                    "time": "2025-05-10 09:00",
                    "read": False,
                },
                {
                    "id": "n2",
                    "text": "New announcement from EcoGreen Society.",
                    "kind": "info",
                    "time": "2025-05-10 09:20",
                    "read": False,
                },
            ],
            "student2": [
                {
                    "id": "n1",
                    "text": "You have been added to 'Documentation' group chat!",
                    "kind": "success",
                    "time": "2025-05-10 10:00",
                    "read": False,
                },
            ],
        }
        jsave(F_NOTIFS, notifs)


# ─────────────────────────── WIDGET HELPERS ────────────────────────────────
def get_bg(widget):
    try:
        return widget.cget("bg")
    except Exception:
        return C["bg"]


def lbl(parent, text, font=None, fg=None, **kw):
    return tk.Label(
        parent,
        text=text,
        font=font or F["body"],
        fg=fg or C["text"],
        bg=get_bg(parent),
        **kw,
    )


def sep(parent, color=None, h=1):
    return tk.Frame(parent, bg=color or C["border"], height=h)


def card_frame(parent, **kw):
    return tk.Frame(parent, bg=C["card"], **kw)


def surface_frame(parent, **kw):
    return tk.Frame(parent, bg=C["surface"], **kw)


def btn(parent, text, cmd=None, bg=None, fg=None, padx=20, pady=8, font=None, **kw):
    bg = bg or C["accent"]
    fg = fg or C["text"]
    b = tk.Button(
        parent,
        text=text,
        command=cmd,
        bg=bg,
        fg=fg,
        activebackground=C["hover"],
        activeforeground=C["text"],
        relief="flat",
        cursor="hand2" if cmd else "default",
        font=font or F["body"],
        padx=padx,
        pady=pady,
        bd=0,
        state="normal" if cmd else "disabled",
        **kw,
    )
    # Update cursor based on command state
    if not cmd:
        b.config(cursor="default")
    return b


def entry(parent, var=None, w=30, show="", **kw):
    e = tk.Entry(
        parent,
        textvariable=var,
        width=w,
        font=F["body"],
        bg=C["surface"],
        fg=C["text"],
        insertbackground=C["text"],
        relief="flat",
        bd=0,
        show=show,
        highlightthickness=1,
        highlightbackground=C["border"],
        highlightcolor=C["accent"],
        **kw,
    )
    return e


def badge(parent, text, color):
    f = tk.Frame(parent, bg=color, padx=6, pady=2)
    tk.Label(
        f,
        text=text,
        font=F["sm"],
        fg=C["bg"] if color not in (C["dim"],) else C["text"],
        bg=color,
    ).pack()
    return f


def scrollable_frame(parent):
    """Returns (outer_frame, inner_frame). Pack outer_frame as needed."""
    outer = tk.Frame(parent, bg=C["bg"])
    sb = ttk.Scrollbar(outer, orient="vertical")
    canvas = tk.Canvas(outer, bg=C["bg"], highlightthickness=0, yscrollcommand=sb.set)
    sb.config(command=canvas.yview)
    sb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    inner = tk.Frame(canvas, bg=C["bg"])
    win_id = canvas.create_window((0, 0), window=inner, anchor="nw")

    def _on_inner(e):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def _on_canvas(e):
        canvas.itemconfig(win_id, width=e.width)

    def _scroll(e):
        canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

    inner.bind("<Configure>", _on_inner)
    canvas.bind("<Configure>", _on_canvas)
    canvas.bind("<MouseWheel>", _scroll)
    canvas.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
    inner.bind("<MouseWheel>", _scroll)
    inner.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    inner.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
    return outer, inner


# ═══════════════════════════════════════════════════════════════════════════
#  APP ROOT
# ═══════════════════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CampusConnect – Student Engagement Portal")
        self.geometry("1320x820")
        self.minsize(1100, 700)
        self.configure(bg=C["bg"])
        self.current_user = None
        self._frame = None
        seed()
        self._show(LoginScreen)

    def _show(self, Cls, **kw):
        if self._frame:
            self._frame.destroy()
        self._frame = Cls(self, **kw)
        self._frame.pack(fill="both", expand=True)

    def go_login(self):
        self.current_user = None
        self._show(LoginScreen)

    def go_register(self):
        self._show(RegisterScreen)

    def go_dashboard(self):
        role = self.current_user["role"]
        if role == "admin":
            self._show(AdminDashboard)
        elif role == "org":
            self._show(OrgDashboard)
        else:
            self._show(StudentDashboard)


# ═══════════════════════════════════════════════════════════════════════════
#  LOGIN
# ═══════════════════════════════════════════════════════════════════════════
class LoginScreen(tk.Frame):
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


# ═══════════════════════════════════════════════════════════════════════════
#  REGISTER
# ═══════════════════════════════════════════════════════════════════════════
class RegisterScreen(tk.Frame):
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
            bg=C["bg"],
        ).pack(anchor="w")
        tk.Label(
            form,
            text="Join the CampusConnect portal",
            font=F["body"],
            fg=C["muted"],
            bg=C["bg"],
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
            tk.Label(col, text=lbl_txt, font=F["body"], fg=C["muted"], bg=C["bg"]).pack(
                anchor="w", pady=(10, 2)
            )
            v = tk.StringVar()
            self._vars[key] = v
            entry(col, var=v, show=show, w=28).pack(ipady=9, fill="x", anchor="w")

        # Year level – full width
        tk.Label(
            form, text="Year Level", font=F["body"], fg=C["muted"], bg=C["bg"]
        ).pack(anchor="w", pady=(14, 2))
        self._year = tk.StringVar(value="1st Year")
        ttk.Combobox(
            form,
            textvariable=self._year,
            values=["1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year"],
            state="readonly",
            font=F["body"],
            width=20,
        ).pack(ipady=6, anchor="w")

        # Bio
        tk.Label(
            form, text="Short Bio (optional)", font=F["body"], fg=C["muted"], bg=C["bg"]
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
            highlightbackground=C["border"],
        )
        self._bio.pack(fill="x")

        tk.Frame(form, bg=C["bg"], height=20).pack()
        btn(form, "Create My Account →", self._register, bg=C["green"], pady=12).pack(
            anchor="w"
        )

        tk.Frame(form, bg=C["bg"], height=12).pack()
        row = tk.Frame(form, bg=C["bg"])
        row.pack(anchor="w")
        tk.Label(
            row,
            text="Already have an account?",
            font=F["body"],
            fg=C["muted"],
            bg=C["bg"],
        ).pack(side="left")
        lb = tk.Label(
            row,
            text=" Sign in",
            font=("Segoe UI", 11, "underline"),
            fg=C["accent"],
            bg=C["bg"],
            cursor="hand2",
        )
        lb.pack(side="left")
        lb.bind("<Button-1>", lambda e: self.master.go_login())

        self._err = tk.Label(form, text="", font=F["sm"], fg=C["red"], bg=C["bg"])
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
        messagebox.showinfo(
            "Account Created!",
            f"Welcome to CampusConnect, {name}!\nYou can now sign in.",
        )
        self.master.go_login()


# ═══════════════════════════════════════════════════════════════════════════
#  BASE DASHBOARD  (shell: sidebar + main area)
# ═══════════════════════════════════════════════════════════════════════════
class BaseDashboard(tk.Frame):
    NAV_ITEMS = []
    ROLE_COLOR = C["accent"]
    ROLE_LABEL = "User"

    def __init__(self, master):
        super().__init__(master, bg=C["bg"])
        self.app = master
        self.user = master.current_user
        self._nav_btns = {}
        self._active = tk.StringVar(value="")
        self._build_shell()
        if self.NAV_ITEMS:
            self._switch(self.NAV_ITEMS[0][1])

    # ── shell ──────────────────────────────────────────────────────────────
    def _build_shell(self):
        # sidebar
        self.sb = tk.Frame(self, bg=C["surface"], width=240)
        self.sb.pack(side="left", fill="y")
        self.sb.pack_propagate(False)
        self._build_sidebar()

        # vertical divider
        tk.Frame(self, bg=C["border"], width=1).pack(side="left", fill="y")

        # main content
        self.main = tk.Frame(self, bg=C["bg"])
        self.main.pack(side="left", fill="both", expand=True)

    def _build_sidebar(self):
        # logo row
        top = tk.Frame(self.sb, bg=C["surface"])
        top.pack(fill="x", padx=16, pady=18)
        tk.Label(
            top, text="🎓", font=("Segoe UI", 22), bg=C["surface"], fg=self.ROLE_COLOR
        ).pack(side="left")
        c = tk.Frame(top, bg=C["surface"])
        c.pack(side="left", padx=8)
        tk.Label(
            c,
            text="CampusConnect",
            font=("Segoe UI", 12, "bold"),
            fg=C["text"],
            bg=C["surface"],
        ).pack(anchor="w")
        tk.Label(
            c, text=self.ROLE_LABEL, font=F["sm"], fg=self.ROLE_COLOR, bg=C["surface"]
        ).pack(anchor="w")

        sep(self.sb).pack(fill="x", padx=12)

        # profile card
        pc = tk.Frame(self.sb, bg=C["card"])
        pc.pack(fill="x", padx=10, pady=10)
        tk.Label(
            pc,
            text=self.user.get("avatar", "👤"),
            font=("Segoe UI", 28),
            bg=C["card"],
            fg=C["text"],
            padx=10,
            pady=8,
        ).pack(side="left")
        pc2 = tk.Frame(pc, bg=C["card"])
        pc2.pack(side="left", pady=8, fill="x", expand=True)
        tk.Label(
            pc2, text=self.user["name"], font=F["bold"], fg=C["text"], bg=C["card"]
        ).pack(anchor="w")
        sub = self.user.get("course") or self.user["role"].capitalize()
        tk.Label(pc2, text=sub[:28], font=F["sm"], fg=C["muted"], bg=C["card"]).pack(
            anchor="w"
        )
        if self.user["role"] == "student":
            pts = self.user.get("points", 0)
            tk.Label(
                pc2, text=f"⭐ {pts} pts", font=F["sm"], fg=C["yellow"], bg=C["card"]
            ).pack(anchor="w")

        sep(self.sb).pack(fill="x", padx=12)

        # nav items
        nav_area = tk.Frame(self.sb, bg=C["surface"])
        nav_area.pack(fill="x", padx=6, pady=6)
        for icon, key, label_text in self.NAV_ITEMS:
            self._make_nav(nav_area, icon, key, label_text)

        # spacer + logout
        tk.Frame(self.sb, bg=C["surface"]).pack(fill="y", expand=True)
        sep(self.sb).pack(fill="x", padx=12, pady=4)

        logout_row = tk.Frame(self.sb, bg=C["surface"], cursor="hand2")
        logout_row.pack(fill="x", padx=6, pady=(0, 10))
        tk.Label(
            logout_row,
            text="⬅",
            font=("Segoe UI", 14),
            bg=C["surface"],
            fg=C["muted"],
            padx=10,
            pady=8,
        ).pack(side="left")
        tk.Label(
            logout_row, text="Log Out", font=F["body"], bg=C["surface"], fg=C["muted"]
        ).pack(side="left", pady=8)
        logout_row.bind("<Button-1>", lambda e: self.app.go_login())
        for w in logout_row.winfo_children():
            w.bind("<Button-1>", lambda e: self.app.go_login())
        logout_row.bind("<Enter>", lambda e: logout_row.config(bg=C["hover"]))
        logout_row.bind("<Leave>", lambda e: logout_row.config(bg=C["surface"]))

    def _make_nav(self, parent, icon, key, text):
        f = tk.Frame(parent, bg=C["surface"], cursor="hand2")
        f.pack(fill="x", pady=1)
        ico_lbl = tk.Label(
            f,
            text=icon,
            font=("Segoe UI", 14),
            bg=C["surface"],
            fg=C["muted"],
            padx=10,
            pady=8,
        )
        ico_lbl.pack(side="left")
        txt_lbl = tk.Label(f, text=text, font=F["body"], bg=C["surface"], fg=C["muted"])
        txt_lbl.pack(side="left", pady=8)
        self._nav_btns[key] = (f, ico_lbl, txt_lbl)

        def click():
            self._switch(key)

        def on_enter(e):
            if self._active.get() != key:
                f.config(bg=C["hover"])
                for w in [ico_lbl, txt_lbl]:
                    w.config(bg=C["hover"])

        def on_leave(e):
            if self._active.get() != key:
                f.config(bg=C["surface"])
                for w in [ico_lbl, txt_lbl]:
                    w.config(bg=C["surface"])

        for w in [f, ico_lbl, txt_lbl]:
            w.bind("<Button-1>", lambda e, fn=click: fn())
            w.bind("<Enter>", on_enter)
            w.bind("<Leave>", on_leave)

    def _switch(self, key):
        # deactivate previous
        prev = self._active.get()
        if prev and prev in self._nav_btns:
            f, ic, tl = self._nav_btns[prev]
            f.config(bg=C["surface"])
            ic.config(bg=C["surface"], fg=C["muted"])
            tl.config(bg=C["surface"], fg=C["muted"])

        self._active.set(key)
        if key in self._nav_btns:
            f, ic, tl = self._nav_btns[key]
            f.config(bg=C["hover"])
            ic.config(bg=C["hover"], fg=self.ROLE_COLOR)
            tl.config(bg=C["hover"], fg=C["text"])

        # clear main
        for w in self.main.winfo_children():
            w.destroy()

        fn = getattr(self, f"page_{key}", None)
        if fn:
            try:
                fn()
            except Exception as ex:
                import traceback

                traceback.print_exc()
                tk.Label(
                    self.main,
                    text=f"⚠ Error loading page: {ex}",
                    font=F["body"],
                    fg=C["red"],
                    bg=C["bg"],
                    wraplength=600,
                ).pack(padx=40, pady=40)

    # ── shared page building blocks ────────────────────────────────────────
    def _scrollable_page(self):
        outer, inner = scrollable_frame(self.main)
        outer.pack(fill="both", expand=True)
        return inner

    def _page_header(self, parent, title, subtitle="", action_txt=None, action_fn=None):
        row = tk.Frame(parent, bg=C["bg"])
        row.pack(fill="x", padx=32, pady=(28, 6))
        left = tk.Frame(row, bg=C["bg"])
        left.pack(side="left", fill="x", expand=True)
        tk.Label(left, text=title, font=F["h1"], fg=C["text"], bg=C["bg"]).pack(
            anchor="w"
        )
        if subtitle:
            tk.Label(
                left, text=subtitle, font=F["body"], fg=C["muted"], bg=C["bg"]
            ).pack(anchor="w", pady=(2, 0))
        if action_txt and action_fn:
            btn(row, action_txt, action_fn, bg=self.ROLE_COLOR, pady=10).pack(
                side="right"
            )
        sep(parent).pack(fill="x", padx=32, pady=(8, 4))

    def _stat_card(self, parent, icon, value, label_text, color=None):
        f = tk.Frame(parent, bg=C["card"], padx=20, pady=16)
        top = tk.Frame(f, bg=C["card"])
        top.pack(fill="x")
        tk.Label(
            top, text=icon, font=("Segoe UI", 22), bg=C["card"], fg=color or C["accent"]
        ).pack(side="left")
        tk.Label(
            f,
            text=str(value),
            font=("Segoe UI", 28, "bold"),
            fg=color or C["accent"],
            bg=C["card"],
        ).pack(anchor="w", pady=(4, 0))
        tk.Label(f, text=label_text, font=F["sm"], fg=C["muted"], bg=C["card"]).pack(
            anchor="w"
        )
        return f

    def _stat_row(self, parent, items):
        """items = list of (icon, value, label, color)"""
        row = tk.Frame(parent, bg=C["bg"])
        row.pack(fill="x", padx=32, pady=16)
        for i, (ico, val, lbl_txt, col) in enumerate(items):
            c = self._stat_card(row, ico, val, lbl_txt, col)
            c.grid(row=0, column=i, padx=6, sticky="ew")
        for i in range(len(items)):
            row.columnconfigure(i, weight=1)

    def _event_card(self, parent, evt, btn_text=None, btn_cmd=None, btn_color=None):
        users = jload(F_USERS)
        org = users.get(evt["org_id"], {})
        col = CAT_COLOR.get(evt.get("category", ""), C["muted"])

        f = card_frame(parent)
        f.pack(fill="x", padx=32, pady=5)

        # accent bar on left
        tk.Frame(f, bg=col, width=4).pack(side="left", fill="y")

        body = tk.Frame(f, bg=C["card"])
        body.pack(side="left", fill="x", expand=True, padx=16, pady=14)

        # top row: category + points
        top_row = tk.Frame(body, bg=C["card"])
        top_row.pack(fill="x")
        tk.Label(
            top_row,
            text=f"● {evt.get('category','General')}",
            font=F["sm"],
            fg=col,
            bg=C["card"],
        ).pack(side="left")
        tk.Label(
            top_row,
            text=f"  ★ {evt.get('points',0)} pts",
            font=F["sm"],
            fg=C["yellow"],
            bg=C["card"],
        ).pack(side="left")
        slots_left = evt["max_slots"] - len(evt["registered"])
        status_col = (
            C["green"]
            if slots_left > 5
            else C["yellow"] if slots_left > 0 else C["red"]
        )
        tk.Label(
            top_row,
            text=f"  {slots_left} slots left",
            font=F["sm"],
            fg=status_col,
            bg=C["card"],
        ).pack(side="left")

        tk.Label(
            body, text=evt["title"], font=F["h2"], fg=C["text"], bg=C["card"]
        ).pack(anchor="w", pady=(4, 6))

        info = tk.Frame(body, bg=C["card"])
        info.pack(fill="x")
        for ico, val in [
            ("📅", evt["date"]),
            ("🕐", evt["time"]),
            ("📍", evt["location"]),
            ("🏢", org.get("name", "")),
        ]:
            tk.Label(
                info,
                text=f"{ico} {val}",
                font=F["sm"],
                fg=C["muted"],
                bg=C["card"],
                padx=4,
            ).pack(side="left")

        if evt.get("description"):
            desc = evt["description"][:140] + (
                "…" if len(evt["description"]) > 140 else ""
            )
            tk.Label(
                body,
                text=desc,
                font=F["sm"],
                fg=C["muted"],
                bg=C["card"],
                wraplength=780,
                justify="left",
            ).pack(anchor="w", pady=(6, 0))

        # tags
        if evt.get("tags"):
            tag_row = tk.Frame(body, bg=C["card"])
            tag_row.pack(anchor="w", pady=(6, 0))
            for tag in evt["tags"][:4]:
                t = tk.Frame(tag_row, bg=C["border"], padx=6, pady=2)
                t.pack(side="left", padx=(0, 4))
                tk.Label(
                    t, text=f"#{tag}", font=F["sm"], fg=C["muted"], bg=C["border"]
                ).pack()

        # action button
        if btn_text:
            btn(
                body, btn_text, btn_cmd, bg=btn_color or C["accent"], pady=6, padx=14
            ).pack(anchor="e", pady=(8, 0))
        return f


# ═══════════════════════════════════════════════════════════════════════════
#  ADMIN DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════
class AdminDashboard(BaseDashboard):
    ROLE_COLOR = C["yellow"]
    ROLE_LABEL = "Administrator"
    NAV_ITEMS = [
        ("📊", "overview", "Overview"),
        ("📅", "events", "All Events"),
        ("👥", "users", "User Management"),
        ("📈", "analytics", "Analytics"),
        ("✅", "attendance", "Attendance"),
        ("📢", "announce", "Announcements"),
    ]

    # ── overview ────────────────────────────────────────────────────────────
    def page_overview(self):
        p = self._scrollable_page()
        users = jload(F_USERS)
        events = jload(F_EVENTS)
        students = [u for u in users.values() if u["role"] == "student"]
        orgs = [u for u in users.values() if u["role"] == "org"]
        total_reg = sum(len(e["registered"]) for e in events.values())

        self._page_header(p, "Admin Overview", f"System snapshot — {today()}")
        self._stat_row(
            p,
            [
                ("👤", len(students), "Total Students", C["accent"]),
                ("🏢", len(orgs), "Organizations", C["purple"]),
                ("📅", len(events), "Events", C["green"]),
                ("✍️", total_reg, "Registrations", C["yellow"]),
            ],
        )

        # ── recent events list ──
        tk.Label(p, text="All Events", font=F["h2"], fg=C["text"], bg=C["bg"]).pack(
            anchor="w", padx=32, pady=(8, 8)
        )
        for evt in list(events.values())[:5]:
            self._event_card(
                p,
                evt,
                btn_text="📋 Attendance",
                btn_cmd=lambda e=evt: self._attendance_popup(e),
                btn_color=C["yellow"],
            )

        # ── course distribution ──
        tk.Label(
            p,
            text="Student Enrollment by Course",
            font=F["h2"],
            fg=C["text"],
            bg=C["bg"],
        ).pack(anchor="w", padx=32, pady=(20, 8))
        bc = card_frame(p)
        bc.pack(fill="x", padx=32, pady=(0, 32))
        by_course = {}
        for s in students:
            k = s.get("course", "Unknown")
            by_course[k] = by_course.get(k, 0) + 1
        mx = max(by_course.values(), default=1)
        for i, (course, cnt) in enumerate(
            sorted(by_course.items(), key=lambda x: -x[1])[:8]
        ):
            row = tk.Frame(bc, bg=C["card"])
            row.pack(fill="x", padx=16, pady=4)
            tk.Label(
                row,
                text=course[:32],
                font=F["body"],
                fg=C["text"],
                bg=C["card"],
                width=34,
                anchor="w",
            ).pack(side="left")
            bar_bg = tk.Frame(row, bg=C["border"], height=14, width=320)
            bar_bg.pack(side="left", padx=8)
            bar_bg.pack_propagate(False)
            bw = max(4, int(320 * cnt / mx))
            tk.Frame(bar_bg, bg=C["accent"], width=bw, height=14).place(x=0, y=0)
            tk.Label(
                row, text=str(cnt), font=F["sm"], fg=C["muted"], bg=C["card"]
            ).pack(side="left")

    # ── all events ──────────────────────────────────────────────────────────
    def page_events(self):
        p = self._scrollable_page()
        events = jload(F_EVENTS)
        self._page_header(p, "All Events", f"{len(events)} events in the system")
        for evt in events.values():
            self._event_card(
                p,
                evt,
                btn_text="📋 Mark Attendance",
                btn_cmd=lambda e=evt: self._attendance_popup(e),
                btn_color=C["yellow"],
            )

    def _attendance_popup(self, evt):
        win = tk.Toplevel(self)
        win.title(f"Attendance — {evt['title']}")
        win.geometry("620x520")
        win.configure(bg=C["bg"])

        tk.Label(
            win, text=f"📋 {evt['title']}", font=F["h2"], fg=C["text"], bg=C["bg"]
        ).pack(pady=16, padx=20, anchor="w")
        tk.Label(
            win,
            text=f"📅 {evt['date']}  📍 {evt['location']}",
            font=F["sm"],
            fg=C["muted"],
            bg=C["bg"],
        ).pack(padx=20, anchor="w")
        sep(win).pack(fill="x", padx=20, pady=12)

        users = jload(F_USERS)
        att = jload(F_ATTENDANCE)
        eid = evt["id"]
        if eid not in att:
            att[eid] = {}

        outer, inner = scrollable_frame(win)
        outer.pack(fill="both", expand=True, padx=20)

        checks = {}
        if not evt["registered"]:
            tk.Label(
                inner,
                text="No students registered yet.",
                font=F["body"],
                fg=C["muted"],
                bg=C["bg"],
            ).pack(padx=8, pady=16)
        for uid in evt["registered"]:
            u = users.get(uid, {})
            if not u:
                continue
            v = tk.BooleanVar(value=att[eid].get(uid, False))
            checks[uid] = v
            row = tk.Frame(inner, bg=C["card"])
            row.pack(fill="x", pady=2)
            tk.Checkbutton(
                row,
                variable=v,
                bg=C["card"],
                fg=C["text"],
                activebackground=C["card"],
                activeforeground=C["accent"],
                selectcolor=C["accent"],
                highlightthickness=0,
            ).pack(side="left", padx=10, pady=10)
            tk.Label(
                row,
                text=f"{u.get('avatar','👤')} {u['name']}",
                font=F["bold"],
                fg=C["text"],
                bg=C["card"],
            ).pack(side="left")
            tk.Label(
                row,
                text=f"  {u.get('course','')} · {u.get('year','')}",
                font=F["sm"],
                fg=C["muted"],
                bg=C["card"],
            ).pack(side="left")

        def save_att():
            try:
                # Track what changed
                newly_marked = []
                newly_unmarked = []

                for uid, v in checks.items():
                    was_present = att[eid].get(uid, False)
                    is_now_present = v.get()

                    # Track transitions
                    if not was_present and is_now_present:
                        newly_marked.append(uid)
                    elif was_present and not is_now_present:
                        newly_unmarked.append(uid)

                    att[eid][uid] = is_now_present

                jsave(F_ATTENDANCE, att)

                # IMPORTANT: Only award points for NEW marks (not already marked)
                users2 = jload(F_USERS)
                points_awarded_count = 0

                for uid in newly_marked:
                    if uid in users2:
                        old_pts = users2[uid].get("points", 0)
                        new_pts = old_pts + evt.get("points", 0)
                        users2[uid]["points"] = new_pts
                        points_awarded_count += 1
                        push_notif(
                            uid,
                            f"✅ Attendance confirmed for '{evt['title']}'! +{evt.get('points',0)} pts (Total: {new_pts} 🌟)",
                            "success",
                        )

                # Remove points if unmarking (shouldn't happen but handle it)
                for uid in newly_unmarked:
                    if uid in users2:
                        old_pts = users2[uid].get("points", 0)
                        new_pts = max(0, old_pts - evt.get("points", 0))
                        users2[uid]["points"] = new_pts
                        push_notif(
                            uid,
                            f"⚠️ Attendance removed from '{evt['title']}'  -{evt.get('points',0)} pts (Total: {new_pts})",
                            "warning",
                        )

                jsave(F_USERS, users2)

                msg = "✓ Attendance saved!"
                if points_awarded_count > 0:
                    msg += f"\n  • {points_awarded_count} student(s) received +{evt.get('points',0)} pts"
                if newly_unmarked:
                    msg += f"\n  • {len(newly_unmarked)} student(s) had points removed"
                if not newly_marked and not newly_unmarked:
                    msg += "\n  • No changes made"

                messagebox.showinfo("Saved ✓", msg)
                win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save attendance: {str(e)}")
                import traceback

                traceback.print_exc()

        sep(win).pack(fill="x", padx=20, pady=6)
        btn(win, "💾  Save Attendance", save_att, bg=C["green"], pady=10).pack(
            padx=20, pady=10, anchor="w"
        )

    # ── user management ─────────────────────────────────────────────────────
    def page_users(self):
        p = self._scrollable_page()
        users = jload(F_USERS)
        self._page_header(
            p,
            "User Management",
            f"{len(users)} accounts registered",
            "➕ Add Demo Student",
            lambda: self._add_demo_student(),
        )

        for role, col in [
            ("admin", C["yellow"]),
            ("org", C["purple"]),
            ("student", C["accent"]),
        ]:
            role_users = [u for u in users.values() if u["role"] == role]
            if not role_users:
                continue
            tk.Label(
                p,
                text=f"  {role.capitalize()}s  ({len(role_users)})",
                font=F["h2"],
                fg=col,
                bg=C["bg"],
            ).pack(anchor="w", padx=32, pady=(20, 6))
            for u in role_users:
                f = card_frame(p)
                f.pack(fill="x", padx=32, pady=3)
                row = tk.Frame(f, bg=C["card"])
                row.pack(fill="x", padx=16, pady=12)
                tk.Label(
                    row,
                    text=u.get("avatar", "👤"),
                    font=("Segoe UI", 24),
                    bg=C["card"],
                    fg=C["text"],
                ).pack(side="left")
                c2 = tk.Frame(row, bg=C["card"])
                c2.pack(side="left", padx=10, fill="x", expand=True)
                tk.Label(
                    c2, text=u["name"], font=F["h3"], fg=C["text"], bg=C["card"]
                ).pack(anchor="w")
                info_txt = f"{u['email']}  •  Joined: {u.get('joined','')}  •  {u.get('course','')} {u.get('year','')}"
                tk.Label(
                    c2, text=info_txt, font=F["sm"], fg=C["muted"], bg=C["card"]
                ).pack(anchor="w")
                if u["role"] == "student":
                    tk.Label(
                        c2,
                        text=f"⭐ {u.get('points',0)} pts  •  {u.get('bio','')[:50]}",
                        font=F["sm"],
                        fg=C["yellow"],
                        bg=C["card"],
                    ).pack(anchor="w")
                tk.Label(
                    row, text=role.upper(), font=F["sm"], fg=col, bg=C["card"]
                ).pack(side="right")
                btn(
                    row,
                    "Remove",
                    lambda uid=u["id"]: self._remove_user(uid),
                    bg=C["red"],
                    pady=4,
                    padx=8,
                    font=F["sm"],
                ).pack(side="right", padx=8)

    def _remove_user(self, uid):
        if uid == self.user["id"]:
            messagebox.showwarning(
                "Action Blocked", "You cannot remove your own account."
            )
            return
        if messagebox.askyesno("Confirm", "Remove this user? This cannot be undone."):
            users = jload(F_USERS)
            users.pop(uid, None)
            jsave(F_USERS, users)
            self._switch("users")

    def _add_demo_student(self):
        users = jload(F_USERS)
        i = sum(1 for u in users.values() if u["role"] == "student") + 1
        uid = f"demo_{i}"
        users[uid] = {
            "id": uid,
            "name": f"Demo Student {i}",
            "email": f"demo{i}@campus.edu",
            "password": hash_pw("demo123"),
            "role": "student",
            "course": "BS General Studies",
            "year": "1st Year",
            "joined": today(),
            "avatar": "🧑‍🎓",
            "points": 0,
            "bio": "Demo account",
        }
        jsave(F_USERS, users)
        messagebox.showinfo("Done", f"Created demo{i} / demo123")
        self._switch("users")

    # ── analytics ───────────────────────────────────────────────────────────
    def page_analytics(self):
        p = self._scrollable_page()
        events = jload(F_EVENTS)
        att = jload(F_ATTENDANCE)
        users = jload(F_USERS)
        self._page_header(p, "Analytics & Reports", "Engagement insights")

        # ── registrations per event ──
        tk.Label(
            p, text="Registrations per Event", font=F["h2"], fg=C["text"], bg=C["bg"]
        ).pack(anchor="w", padx=32, pady=(16, 8))
        f1 = card_frame(p)
        f1.pack(fill="x", padx=32, pady=(0, 16))
        sorted_evts = sorted(
            events.values(), key=lambda e: len(e["registered"]), reverse=True
        )
        mx = max((len(e["registered"]) for e in sorted_evts), default=1)
        for evt in sorted_evts[:8]:
            row = tk.Frame(f1, bg=C["card"])
            row.pack(fill="x", padx=16, pady=5)
            col = CAT_COLOR.get(evt.get("category", ""), C["muted"])
            tk.Label(
                row,
                text=evt["title"][:32],
                font=F["body"],
                fg=C["text"],
                bg=C["card"],
                width=32,
                anchor="w",
            ).pack(side="left")
            bar_bg = tk.Frame(row, bg=C["border"], height=16, width=320)
            bar_bg.pack(side="left", padx=8)
            bar_bg.pack_propagate(False)
            bw = max(4, int(320 * len(evt["registered"]) / mx))
            tk.Frame(bar_bg, bg=col, width=bw, height=16).place(x=0, y=0)
            tk.Label(
                row,
                text=str(len(evt["registered"])),
                font=F["sm"],
                fg=C["muted"],
                bg=C["card"],
            ).pack(side="left")

        # ── attendance rates ──
        tk.Label(
            p, text="Attendance Rates", font=F["h2"], fg=C["text"], bg=C["bg"]
        ).pack(anchor="w", padx=32, pady=(16, 8))
        f2 = card_frame(p)
        f2.pack(fill="x", padx=32, pady=(0, 16))
        for evt in sorted_evts:
            total = len(evt["registered"])
            present = sum(1 for uid, v in att.get(evt["id"], {}).items() if v)
            pct = int(100 * present / total) if total else 0
            row = tk.Frame(f2, bg=C["card"])
            row.pack(fill="x", padx=16, pady=5)
            tk.Label(
                row,
                text=evt["title"][:32],
                font=F["body"],
                fg=C["text"],
                bg=C["card"],
                width=32,
                anchor="w",
            ).pack(side="left")
            bar_bg = tk.Frame(row, bg=C["border"], height=14, width=280)
            bar_bg.pack(side="left", padx=8)
            bar_bg.pack_propagate(False)
            tk.Frame(
                bar_bg, bg=C["green"], width=int(280 * pct / 100), height=14
            ).place(x=0, y=0)
            tk.Label(
                row,
                text=f"{present}/{total} ({pct}%)",
                font=F["sm"],
                fg=C["muted"],
                bg=C["card"],
            ).pack(side="left")

        # ── points leaderboard ──
        tk.Label(
            p, text="Top Students by Points", font=F["h2"], fg=C["text"], bg=C["bg"]
        ).pack(anchor="w", padx=32, pady=(16, 8))
        f3 = card_frame(p)
        f3.pack(fill="x", padx=32, pady=(0, 32))
        students = sorted(
            [u for u in users.values() if u["role"] == "student"],
            key=lambda u: u.get("points", 0),
            reverse=True,
        )[:10]
        medals = ["🥇", "🥈", "🥉"] + ["  "] * 10
        for i, s in enumerate(students):
            row = tk.Frame(f3, bg=C["card"])
            row.pack(fill="x", padx=16, pady=4)
            tk.Label(
                row, text=medals[i], font=("Segoe UI", 16), bg=C["card"], fg=C["text"]
            ).pack(side="left", padx=8, pady=8)
            tk.Label(
                row,
                text=s["name"],
                font=F["bold"],
                fg=C["text"],
                bg=C["card"],
                width=22,
                anchor="w",
            ).pack(side="left")
            tk.Label(
                row, text=s.get("course", ""), font=F["sm"], fg=C["muted"], bg=C["card"]
            ).pack(side="left")
            tk.Label(
                row,
                text=f"⭐ {s.get('points',0)} pts",
                font=F["bold"],
                fg=C["yellow"],
                bg=C["card"],
            ).pack(side="right", padx=16)

    # ── attendance log ───────────────────────────────────────────────────────
    def page_attendance(self):
        p = self._scrollable_page()
        events = jload(F_EVENTS)
        att = jload(F_ATTENDANCE)
        users = jload(F_USERS)
        self._page_header(p, "Attendance Records", "All event attendance logs")

        for evt in events.values():
            tk.Label(
                p,
                text=f"📅 {evt['title']} — {evt['date']}",
                font=F["h3"],
                fg=C["text"],
                bg=C["bg"],
            ).pack(anchor="w", padx=32, pady=(16, 4))
            f = card_frame(p)
            f.pack(fill="x", padx=32, pady=(0, 8))
            if not evt["registered"]:
                tk.Label(
                    f,
                    text="No registrations.",
                    font=F["sm"],
                    fg=C["muted"],
                    bg=C["card"],
                ).pack(padx=16, pady=8, anchor="w")
                continue
            for uid in evt["registered"]:
                u = users.get(uid, {})
                present = att.get(evt["id"], {}).get(uid, False)
                row = tk.Frame(f, bg=C["card"])
                row.pack(fill="x", padx=16, pady=3)
                tk.Label(
                    row,
                    text=u.get("name", uid),
                    font=F["body"],
                    fg=C["text"],
                    bg=C["card"],
                    width=24,
                    anchor="w",
                ).pack(side="left")
                tk.Label(
                    row,
                    text=u.get("course", ""),
                    font=F["sm"],
                    fg=C["muted"],
                    bg=C["card"],
                ).pack(side="left")
                status = "✅ Present" if present else "❌ Absent"
                clr = C["green"] if present else C["red"]
                tk.Label(row, text=status, font=F["sm"], fg=clr, bg=C["card"]).pack(
                    side="right", padx=16
                )

    # ── announcements ────────────────────────────────────────────────────────
    def page_announce(self):
        p = self._scrollable_page()
        self._page_header(p, "Send Announcement", "Broadcast a message to all students")

        f = card_frame(p)
        f.pack(fill="x", padx=32, pady=16)
        inner = tk.Frame(f, bg=C["card"])
        inner.pack(fill="x", padx=24, pady=20)

        tk.Label(inner, text="Title", font=F["body"], fg=C["muted"], bg=C["card"]).pack(
            anchor="w", pady=(0, 2)
        )
        title_v = tk.StringVar()
        entry(inner, var=title_v, w=50).pack(ipady=8, anchor="w", fill="x")

        tk.Label(
            inner, text="Message", font=F["body"], fg=C["muted"], bg=C["card"]
        ).pack(anchor="w", pady=(12, 2))
        msg_box = scrolledtext.ScrolledText(
            inner,
            height=4,
            font=F["body"],
            bg=C["surface"],
            fg=C["text"],
            insertbackground=C["text"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=C["border"],
        )
        msg_box.pack(fill="x")

        tk.Label(
            inner, text="Target Audience", font=F["body"], fg=C["muted"], bg=C["card"]
        ).pack(anchor="w", pady=(12, 2))
        aud_v = tk.StringVar(value="All Students")
        ttk.Combobox(
            inner,
            textvariable=aud_v,
            values=["All Students", "All Organizations", "Everyone"],
            state="readonly",
            font=F["body"],
            width=20,
        ).pack(ipady=6, anchor="w")

        def send_ann():
            title = title_v.get().strip()
            msg = msg_box.get("1.0", "end").strip()
            aud = aud_v.get()
            if not title or not msg:
                messagebox.showwarning("Missing", "Fill in title and message.")
                return
            users = jload(F_USERS)
            sent = 0
            for u in users.values():
                if aud == "All Students" and u["role"] != "student":
                    continue
                if aud == "All Organizations" and u["role"] != "org":
                    continue
                push_notif(u["id"], f"📢 [{title}]: {msg[:80]}", "info")
                sent += 1
            messagebox.showinfo("Sent!", f"Announcement sent to {sent} users.")
            title_v.set("")
            msg_box.delete("1.0", "end")

        btn(
            inner,
            "📢  Broadcast Announcement",
            send_ann,
            bg=C["yellow"],
            fg=C["bg"],
            pady=12,
        ).pack(anchor="w", pady=(16, 0))


# ═══════════════════════════════════════════════════════════════════════════
#  ORG DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════
class OrgDashboard(BaseDashboard):
    ROLE_COLOR = C["green"]
    ROLE_LABEL = "Organization"
    NAV_ITEMS = [
        ("🏠", "overview", "Overview"),
        ("📅", "my_events", "My Events"),
        ("➕", "create_event", "Create Event"),
        ("📋", "forms", "Form Builder"),
        ("💬", "chats", "Group Chats"),
        ("👥", "members", "Members"),
    ]

    def _my_events(self):
        return [e for e in jload(F_EVENTS).values() if e["org_id"] == self.user["id"]]

    def page_overview(self):
        p = self._scrollable_page()
        my_evts = self._my_events()
        total_reg = sum(len(e["registered"]) for e in my_evts)
        groups = jload(F_GROUPS)
        my_grps = [
            g for g in groups.values() if any(e["id"] == g["event_id"] for e in my_evts)
        ]

        self._page_header(
            p, f"Welcome, {self.user['name'].split()[0]}! 🏢", self.user.get("bio", "")
        )
        self._stat_row(
            p,
            [
                ("📅", len(my_evts), "My Events", C["green"]),
                ("👥", total_reg, "Registrations", C["accent"]),
                ("💬", len(my_grps), "Active Groups", C["yellow"]),
            ],
        )

        tk.Label(
            p, text="My Recent Events", font=F["h2"], fg=C["text"], bg=C["bg"]
        ).pack(anchor="w", padx=32, pady=(8, 8))
        if not my_evts:
            tk.Label(
                p,
                text="No events yet. Create your first event!",
                font=F["body"],
                fg=C["muted"],
                bg=C["bg"],
            ).pack(padx=32)
        for e in my_evts[:3]:
            self._event_card(
                p,
                e,
                btn_text="👥 Registrants",
                btn_cmd=lambda ev=e: self._registrants_popup(ev),
                btn_color=C["green"],
            )

    def page_my_events(self):
        p = self._scrollable_page()
        my_evts = self._my_events()
        self._page_header(
            p,
            "My Events",
            f"{len(my_evts)} events",
            "➕ Create New",
            lambda: self._switch("create_event"),
        )
        for evt in my_evts:
            self._event_card(
                p,
                evt,
                btn_text="👥 View Registrants",
                btn_cmd=lambda e=evt: self._registrants_popup(e),
                btn_color=C["green"],
            )
        if not my_evts:
            tk.Label(
                p, text="No events yet.", font=F["body"], fg=C["muted"], bg=C["bg"]
            ).pack(padx=32)

    def _registrants_popup(self, evt):
        win = tk.Toplevel(self)
        win.title(f"Registrants — {evt['title']}")
        win.geometry("640x520")
        win.configure(bg=C["bg"])
        users = jload(F_USERS)
        resps = jload(F_RESPONSES)

        tk.Label(
            win, text=f"👥 {evt['title']}", font=F["h2"], fg=C["text"], bg=C["bg"]
        ).pack(pady=16, padx=20, anchor="w")
        tk.Label(
            win,
            text=f"{len(evt['registered'])} registrants",
            font=F["body"],
            fg=C["muted"],
            bg=C["bg"],
        ).pack(padx=20, anchor="w")
        sep(win).pack(fill="x", padx=20, pady=10)

        outer, inner = scrollable_frame(win)
        outer.pack(fill="both", expand=True, padx=20)

        if not evt["registered"]:
            tk.Label(
                inner,
                text="No registrations yet.",
                font=F["body"],
                fg=C["muted"],
                bg=C["bg"],
            ).pack(pady=20)
        for uid in evt["registered"]:
            u = users.get(uid, {})
            if not u:
                continue
            f = card_frame(inner)
            f.pack(fill="x", pady=4)
            row = tk.Frame(f, bg=C["card"])
            row.pack(fill="x", padx=12, pady=10)
            tk.Label(
                row,
                text=u.get("avatar", "👤"),
                font=("Segoe UI", 22),
                bg=C["card"],
                fg=C["text"],
            ).pack(side="left")
            c2 = tk.Frame(row, bg=C["card"])
            c2.pack(side="left", padx=10)
            tk.Label(
                c2, text=u.get("name", uid), font=F["h3"], fg=C["text"], bg=C["card"]
            ).pack(anchor="w")
            tk.Label(
                c2,
                text=f"{u.get('course','')} · {u.get('year','')}",
                font=F["sm"],
                fg=C["muted"],
                bg=C["card"],
            ).pack(anchor="w")
            resp_key = f"{evt['id']}_{uid}"
            resp = resps.get(resp_key, {})
            if resp:
                short = "  |  ".join(
                    f"{k[:20]}: {str(v)[:20]}" for k, v in resp.items() if k != "group"
                )
                tk.Label(
                    c2,
                    text=f"📋 {short[:80]}",
                    font=F["sm"],
                    fg=C["purple"],
                    bg=C["card"],
                ).pack(anchor="w")

    def page_create_event(self):
        p = self._scrollable_page()
        self._page_header(p, "Create New Event", "Fill in the details below")

        f = card_frame(p)
        f.pack(fill="x", padx=32, pady=16)
        inner = tk.Frame(f, bg=C["card"])
        inner.pack(fill="x", padx=24, pady=20)

        # two-column grid of fields
        cols = tk.Frame(inner, bg=C["card"])
        cols.pack(fill="x")
        lc = tk.Frame(cols, bg=C["card"])
        lc.pack(side="left", fill="x", expand=True, padx=(0, 16))
        rc = tk.Frame(cols, bg=C["card"])
        rc.pack(side="left", fill="x", expand=True)

        fields = {}
        for col, flds in [
            (
                lc,
                [
                    ("Event Title", "title", 40),
                    ("Date (YYYY-MM-DD)", "date", 20),
                    ("Time", "time", 20),
                ],
            ),
            (
                rc,
                [
                    ("Location", "location", 36),
                    ("Max Slots", "max_slots", 10),
                    ("Points Reward", "points", 10),
                ],
            ),
        ]:
            for lbl_txt, key, w in flds:
                tk.Label(
                    col, text=lbl_txt, font=F["body"], fg=C["muted"], bg=C["card"]
                ).pack(anchor="w", pady=(10, 2))
                v = tk.StringVar()
                fields[key] = v
                entry(col, var=v, w=w).pack(ipady=8, anchor="w", fill="x")

        # category
        tk.Label(
            inner, text="Category", font=F["body"], fg=C["muted"], bg=C["card"]
        ).pack(anchor="w", pady=(14, 2))
        cat_v = tk.StringVar(value="Environmental")
        ttk.Combobox(
            inner,
            textvariable=cat_v,
            values=list(CAT_COLOR.keys()),
            state="readonly",
            font=F["body"],
            width=24,
        ).pack(ipady=6, anchor="w")

        # tags
        tk.Label(
            inner,
            text="Tags (comma-separated)",
            font=F["body"],
            fg=C["muted"],
            bg=C["card"],
        ).pack(anchor="w", pady=(12, 2))
        tags_v = tk.StringVar()
        entry(inner, var=tags_v, w=50).pack(ipady=8, anchor="w", fill="x")

        # description
        tk.Label(
            inner, text="Description", font=F["body"], fg=C["muted"], bg=C["card"]
        ).pack(anchor="w", pady=(12, 2))
        desc_box = scrolledtext.ScrolledText(
            inner,
            height=4,
            font=F["body"],
            bg=C["surface"],
            fg=C["text"],
            insertbackground=C["text"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=C["border"],
        )
        desc_box.pack(fill="x")

        def create():
            events = jload(F_EVENTS)
            title = fields["title"].get().strip()
            if not title:
                messagebox.showwarning("Missing", "Event title is required.")
                return
            eid = f"evt_{uuid.uuid4().hex[:8]}"
            try:
                slots = int(fields["max_slots"].get())
                if slots <= 0:
                    slots = 20
            except:
                slots = 20
            try:
                pts = int(fields["points"].get())
                if pts < 0:
                    pts = 50
            except:
                pts = 50
            tags_raw = [t.strip() for t in tags_v.get().split(",") if t.strip()]
            events[eid] = {
                "id": eid,
                "title": title,
                "org_id": self.user["id"],
                "category": cat_v.get(),
                "date": fields["date"].get().strip() or "TBD",
                "time": fields["time"].get().strip() or "TBD",
                "location": fields["location"].get().strip() or "TBD",
                "description": desc_box.get("1.0", "end").strip(),
                "max_slots": slots,
                "registered": [],
                "status": "upcoming",
                "created": today(),
                "form_id": None,
                "tags": tags_raw,
                "points": pts,
            }
            jsave(F_EVENTS, events)
            messagebox.showinfo(
                "Created!", f"Event '{title}' published with {pts} points reward!"
            )
            self._switch("my_events")

        btn(inner, "🚀  Publish Event", create, bg=C["green"], pady=12).pack(
            anchor="w", pady=(20, 0)
        )

    def page_forms(self):
        p = self._scrollable_page()
        forms = jload(F_FORMS)
        events = jload(F_EVENTS)
        my_ids = {e["id"] for e in events.values() if e["org_id"] == self.user["id"]}
        my_forms = {k: v for k, v in forms.items() if v.get("event_id") in my_ids}
        self._page_header(
            p,
            "Form Builder",
            f"{len(my_forms)} forms",
            "➕ Create Form",
            lambda: self._form_builder_popup(),
        )

        if not my_forms:
            tk.Label(
                p,
                text="No forms created yet. Create an event first, then build a form for it.",
                font=F["body"],
                fg=C["muted"],
                bg=C["bg"],
            ).pack(padx=32, pady=32)
            return

        for fid, frm in my_forms.items():
            evt = events.get(frm.get("event_id", ""), {})
            f = card_frame(p)
            f.pack(fill="x", padx=32, pady=8)

            # Header with form title and event name
            top = tk.Frame(f, bg=C["card"])
            top.pack(fill="x", padx=16, pady=(14, 2))
            tk.Label(
                top, text=f"📋 {frm['title']}", font=F["h2"], fg=C["text"], bg=C["card"]
            ).pack(side="left")
            tk.Label(top, text="", bg=C["card"]).pack(side="left", expand=True)
            tk.Label(
                top,
                text=f"📅 {evt.get('title','?')}",
                font=F["sm"],
                fg=C["accent"],
                bg=C["card"],
            ).pack(side="right")

            info_row = tk.Frame(f, bg=C["card"])
            info_row.pack(fill="x", padx=16, pady=(2, 8))
            tk.Label(
                info_row,
                text=f"❓ {len(frm['questions'])} questions",
                font=F["sm"],
                fg=C["muted"],
                bg=C["card"],
            ).pack(side="left")
            assigned = sum(1 for q in frm["questions"] if q.get("assigns_to_group"))
            if assigned:
                tk.Label(
                    info_row,
                    text=f"  •  🎯 {assigned} group assignments",
                    font=F["sm"],
                    fg=C["green"],
                    bg=C["card"],
                ).pack(side="left")
            required = sum(1 for q in frm["questions"] if q.get("required"))
            if required:
                tk.Label(
                    info_row,
                    text=f"  •  ⚠️ {required} required fields",
                    font=F["sm"],
                    fg=C["yellow"],
                    bg=C["card"],
                ).pack(side="left")

            # Questions preview
            for i, q in enumerate(frm["questions"], 1):
                qf = tk.Frame(f, bg=C["hover"])
                qf.pack(fill="x", padx=16, pady=2)
                tp = "🔘" if q["type"] == "choice" else "✏️"
                req = " *" if q.get("required") else ""
                grp = " [GROUP]" if q.get("assigns_to_group") else ""
                tk.Label(
                    qf,
                    text=f"  Q{i}: {tp} {q['text']}{req}{grp}",
                    font=F["sm"],
                    fg=C["text"],
                    bg=C["hover"],
                    wraplength=600,
                    justify="left",
                ).pack(side="left", pady=4, padx=2, anchor="w")
                if q["type"] == "choice":
                    opts = ", ".join(q.get("options", [])[:3])
                    more = (
                        f" +{len(q.get('options', []))-3} more"
                        if len(q.get("options", [])) > 3
                        else ""
                    )
                    tk.Label(
                        qf,
                        text=f"  → {opts}{more}",
                        font=F["sm"],
                        fg=C["dim"],
                        bg=C["hover"],
                    ).pack(side="left", padx=4)
            tk.Frame(f, bg=C["card"], height=4).pack()

    def _form_builder_popup(self):
        win = tk.Toplevel(self)
        win.title("Create Registration Form")
        win.geometry("720x640")
        win.configure(bg=C["bg"])

        events = jload(F_EVENTS)
        my_evts = {
            e["id"]: e["title"]
            for e in events.values()
            if e["org_id"] == self.user["id"]
        }

        tk.Label(
            win, text="📋 Form Builder", font=F["h1"], fg=C["text"], bg=C["bg"]
        ).pack(pady=(20, 4), padx=24, anchor="w")
        sep(win).pack(fill="x", padx=24, pady=(0, 16))

        tk.Label(
            win, text="Form Title", font=F["body"], fg=C["muted"], bg=C["bg"]
        ).pack(anchor="w", padx=24, pady=(0, 2))
        title_v = tk.StringVar()
        entry(win, var=title_v, w=52).pack(ipady=8, padx=24, anchor="w")

        tk.Label(
            win, text="Link to Event", font=F["body"], fg=C["muted"], bg=C["bg"]
        ).pack(anchor="w", padx=24, pady=(12, 2))
        evt_v = tk.StringVar()
        evt_titles = list(my_evts.values())
        ttk.Combobox(
            win,
            textvariable=evt_v,
            values=evt_titles,
            state="readonly",
            font=F["body"],
            width=50,
        ).pack(padx=24, anchor="w", ipady=6)

        tk.Label(win, text="Questions", font=F["h3"], fg=C["text"], bg=C["bg"]).pack(
            anchor="w", padx=24, pady=(16, 4)
        )

        questions = []
        q_list = tk.Frame(win, bg=C["bg"])
        q_list.pack(fill="x", padx=24)

        def refresh():
            for w in q_list.winfo_children():
                w.destroy()
            for i, q in enumerate(questions):
                qf = tk.Frame(q_list, bg=C["card"])
                qf.pack(fill="x", pady=2)
                tp = "🔘" if q["type"] == "choice" else "✏️"
                grp = " [group]" if q.get("assigns_to_group") else ""
                req = " *" if q.get("required") else ""
                tk.Label(
                    qf,
                    text=f"  Q{i+1}: {tp} {q['text']}{req}{grp}",
                    font=F["sm"],
                    fg=C["text"],
                    bg=C["card"],
                ).pack(side="left", padx=8, pady=6)
                btn(
                    qf,
                    "✕",
                    lambda idx=i: (questions.pop(idx), refresh()),
                    bg=C["red"],
                    pady=2,
                    padx=6,
                    font=F["sm"],
                ).pack(side="right", padx=8)

        def add_q_popup():
            qw = tk.Toplevel(win)
            qw.title("Add Question")
            qw.geometry("480x400")
            qw.configure(bg=C["bg"])

            tk.Label(
                qw, text="Question Text", font=F["body"], fg=C["muted"], bg=C["bg"]
            ).pack(anchor="w", padx=20, pady=(16, 2))
            qt_v = tk.StringVar()
            entry(qw, var=qt_v, w=48).pack(ipady=8, padx=20, anchor="w", fill="x")

            tk.Label(qw, text="Type", font=F["body"], fg=C["muted"], bg=C["bg"]).pack(
                anchor="w", padx=20, pady=(10, 2)
            )
            type_v = tk.StringVar(value="choice")
            ttk.Combobox(
                qw,
                textvariable=type_v,
                values=["choice", "text"],
                state="readonly",
                font=F["body"],
                width=16,
            ).pack(padx=20, anchor="w", ipady=6)

            tk.Label(
                qw,
                text="Options (comma-separated — for 'choice' type)",
                font=F["body"],
                fg=C["muted"],
                bg=C["bg"],
            ).pack(anchor="w", padx=20, pady=(10, 2))
            opts_v = tk.StringVar()
            entry(qw, var=opts_v, w=48).pack(ipady=8, padx=20, anchor="w", fill="x")

            grp_v = tk.BooleanVar()
            req_v = tk.BooleanVar(value=True)
            ck_row = tk.Frame(qw, bg=C["bg"])
            ck_row.pack(anchor="w", padx=20, pady=10)
            tk.Checkbutton(
                ck_row,
                text="Assigns student to a group chat",
                variable=grp_v,
                bg=C["bg"],
                fg=C["text"],
                activebackground=C["bg"],
                activeforeground=C["accent"],
                selectcolor=C["accent"],
                highlightthickness=0,
                font=F["body"],
            ).pack(side="left")
            tk.Checkbutton(
                ck_row,
                text="Required",
                variable=req_v,
                bg=C["bg"],
                fg=C["text"],
                activebackground=C["bg"],
                activeforeground=C["accent"],
                selectcolor=C["accent"],
                highlightthickness=0,
                font=F["body"],
            ).pack(side="left", padx=16)

            def save_q():
                text = qt_v.get().strip()
                if not text:
                    messagebox.showwarning("Missing", "Question text is required.")
                    return

                q_type = type_v.get()
                options = (
                    [o.strip() for o in opts_v.get().split(",") if o.strip()]
                    if opts_v.get().strip()
                    else []
                )

                # Validate that choice type has options
                if q_type == "choice":
                    if not options:
                        messagebox.showwarning(
                            "Missing", "Choice questions must have at least one option."
                        )
                        return

                questions.append(
                    {
                        "id": f"q{len(questions)+1}",
                        "text": text,
                        "type": q_type,
                        "options": options,
                        "assigns_to_group": grp_v.get(),
                        "required": req_v.get(),
                    }
                )
                refresh()
                qw.destroy()

            btn(qw, "✔ Add Question", save_q, bg=C["green"], pady=10).pack(
                padx=20, pady=16, anchor="w"
            )

        btn(win, "➕ Add Question", add_q_popup, bg=C["accent"], pady=6, padx=12).pack(
            padx=24, anchor="w", pady=(0, 8)
        )

        def save_form():
            sel_title = evt_v.get()
            sel_eid = next(
                (eid for eid, et in my_evts.items() if et == sel_title), None
            )
            if not sel_eid:
                messagebox.showwarning("Missing", "Select an event.")
                return
            if not title_v.get().strip():
                messagebox.showwarning("Missing", "Form title is required.")
                return
            if not questions:
                messagebox.showwarning("Missing", "Add at least one question.")
                return

            try:
                forms = jload(F_FORMS)
                events2 = jload(F_EVENTS)
                fid = f"form_{uuid.uuid4().hex[:8]}"
                forms[fid] = {
                    "id": fid,
                    "event_id": sel_eid,
                    "title": title_v.get().strip(),
                    "questions": questions,
                }
                events2[sel_eid]["form_id"] = fid
                jsave(F_FORMS, forms)
                jsave(F_EVENTS, events2)
                messagebox.showinfo(
                    "✓ Saved!",
                    f"Form '{title_v.get().strip()}' created with {len(questions)} questions!",
                )
                win.destroy()
                self._switch("forms")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save form: {e}")

        sep(win).pack(fill="x", padx=24, pady=10)
        btn(win, "💾  Save Form", save_form, bg=C["green"], pady=10).pack(
            padx=24, anchor="w"
        )

    def page_chats(self):
        p = self._scrollable_page()
        groups = jload(F_GROUPS)
        events = jload(F_EVENTS)
        my_ids = {e["id"] for e in events.values() if e["org_id"] == self.user["id"]}
        my_grps = {k: v for k, v in groups.items() if v.get("event_id") in my_ids}
        self._page_header(p, "Group Chats", f"{len(my_grps)} active groups")

        if not my_grps:
            tk.Label(
                p,
                text="No groups yet. Create events and build forms to auto-generate groups.",
                font=F["body"],
                fg=C["muted"],
                bg=C["bg"],
            ).pack(padx=32, pady=16)

        msgs_all = jload(F_MESSAGES)
        for gid, grp in my_grps.items():
            evt = events.get(grp["event_id"], {})
            msgs = msgs_all.get(gid, [])
            last = (msgs[-1]["text"][:55] + "…") if msgs else "No messages yet"
            f = card_frame(p)
            f.pack(fill="x", padx=32, pady=5)
            row = tk.Frame(f, bg=C["card"])
            row.pack(fill="x", padx=16, pady=12)
            tk.Label(
                row, text="💬", font=("Segoe UI", 24), bg=C["card"], fg=C["green"]
            ).pack(side="left")
            c2 = tk.Frame(row, bg=C["card"])
            c2.pack(side="left", padx=10, fill="x", expand=True)
            tk.Label(
                c2, text=grp["name"], font=F["h3"], fg=C["text"], bg=C["card"]
            ).pack(anchor="w")
            tk.Label(
                c2,
                text=f"{evt.get('title','')}  •  {len(grp['members'])} members",
                font=F["sm"],
                fg=C["muted"],
                bg=C["card"],
            ).pack(anchor="w")
            tk.Label(c2, text=last, font=F["sm"], fg=C["dim"], bg=C["card"]).pack(
                anchor="w", pady=(2, 0)
            )
            btn(
                row,
                "Open Chat →",
                lambda g=gid: ChatWindow(self, g, self.user),
                bg=C["green"],
                pady=6,
                padx=12,
            ).pack(side="right")

    def page_members(self):
        p = self._scrollable_page()
        groups = jload(F_GROUPS)
        events = jload(F_EVENTS)
        users = jload(F_USERS)
        my_evts = {
            e["id"]: e["title"]
            for e in events.values()
            if e["org_id"] == self.user["id"]
        }
        self._page_header(
            p, "Members by Group", "Students assigned to your event groups"
        )

        for gid, grp in groups.items():
            if grp["event_id"] not in my_evts:
                continue
            tk.Label(
                p,
                text=f"💬 {grp['name']}  —  {my_evts[grp['event_id']]}",
                font=F["h3"],
                fg=C["text"],
                bg=C["bg"],
            ).pack(anchor="w", padx=32, pady=(16, 4))
            f = card_frame(p)
            f.pack(fill="x", padx=32, pady=(0, 8))
            if not grp["members"]:
                tk.Label(
                    f, text="No members yet.", font=F["sm"], fg=C["muted"], bg=C["card"]
                ).pack(padx=16, pady=8, anchor="w")
                continue
            for uid in grp["members"]:
                u = users.get(uid, {})
                if not u:
                    continue
                row = tk.Frame(f, bg=C["card"])
                row.pack(fill="x", padx=16, pady=4)
                tk.Label(
                    row,
                    text=u.get("avatar", "👤"),
                    font=("Segoe UI", 18),
                    bg=C["card"],
                    fg=C["text"],
                ).pack(side="left", padx=4)
                tk.Label(
                    row,
                    text=u.get("name", uid),
                    font=F["bold"],
                    fg=C["text"],
                    bg=C["card"],
                ).pack(side="left", padx=6)
                tk.Label(
                    row,
                    text=f"{u.get('course','')} · {u.get('year','')}",
                    font=F["sm"],
                    fg=C["muted"],
                    bg=C["card"],
                ).pack(side="left")
                role_col = C["muted"] if u["role"] == "org" else C["accent"]
                tk.Label(
                    row, text=u["role"].upper(), font=F["sm"], fg=role_col, bg=C["card"]
                ).pack(side="right", padx=16)


# ═══════════════════════════════════════════════════════════════════════════
#  STUDENT DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════
class StudentDashboard(BaseDashboard):
    ROLE_COLOR = C["accent"]
    ROLE_LABEL = "Student"
    NAV_ITEMS = [
        ("🏠", "overview", "My Dashboard"),
        ("🔍", "discover", "Discover Events"),
        ("📅", "my_events", "My Events"),
        ("💬", "chats", "Group Chats"),
        ("🔔", "notifs", "Notifications"),
        ("🏆", "rewards", "Rewards"),
        ("👤", "profile", "My Profile"),
    ]

    def _joined_events(self):
        return [
            e for e in jload(F_EVENTS).values() if self.user["id"] in e["registered"]
        ]

    def _total_pts(self):
        # refresh from file to get latest points
        users = jload(F_USERS)
        current_user = users.get(self.user["id"], {})
        pts = current_user.get("points", 0)
        # Also update the session user object
        self.user = current_user
        self.app.current_user = current_user
        return pts

    def _my_groups(self):
        return {
            k: v for k, v in jload(F_GROUPS).items() if self.user["id"] in v["members"]
        }

    def page_overview(self):
        p = self._scrollable_page()

        # ALWAYS refresh user data to get latest points from disk
        users = jload(F_USERS)
        self.user = users.get(self.user["id"], self.user)
        self.app.current_user = self.user

        joined = self._joined_events()
        pts = self.user.get("points", 0)
        grps = self._my_groups()

        level, lv_col = _get_level(pts)
        self._page_header(
            p,
            f"Welcome back, {self.user['name'].split()[0]}! 👋",
            f"{self.user.get('course','')} · {self.user.get('year','')}",
        )

        self._stat_row(
            p,
            [
                ("📅", len(joined), "Events Joined", C["accent"]),
                ("⭐", pts, "Total Points", C["yellow"]),
                ("💬", len(grps), "My Group Chats", C["green"]),
            ],
        )

        # level banner
        lv_f = card_frame(p)
        lv_f.pack(fill="x", padx=32, pady=(0, 16))
        lv_r = tk.Frame(lv_f, bg=C["card"])
        lv_r.pack(fill="x", padx=16, pady=14)
        tk.Label(
            lv_r, text=f"🎖️  {level} Member", font=F["h3"], fg=lv_col, bg=C["card"]
        ).pack(side="left")
        next_pts = {"Bronze": 200, "Silver": 500, "Gold": 1000, "Platinum": 99999}
        rem = next_pts[level] - pts
        tk.Label(
            lv_r,
            text=f"  —  {rem} pts to next level  •  Keep participating!",
            font=F["sm"],
            fg=C["muted"],
            bg=C["card"],
        ).pack(side="left")

        # upcoming joined events
        tk.Label(
            p, text="My Upcoming Events", font=F["h2"], fg=C["text"], bg=C["bg"]
        ).pack(anchor="w", padx=32, pady=(8, 8))
        if not joined:
            tk.Label(
                p,
                text="You haven't joined any events yet. Browse Discover Events →",
                font=F["body"],
                fg=C["muted"],
                bg=C["bg"],
            ).pack(padx=32, pady=8)
        for e in joined[:3]:
            self._event_card(
                p,
                e,
                btn_text="💬 Open Chat",
                btn_cmd=lambda ev=e: self._open_event_chat(ev),
                btn_color=C["green"],
            )

        # notifications preview
        notifs = jload(F_NOTIFS).get(self.user["id"], [])
        unread = [n for n in notifs if not n["read"]]
        if unread:
            tk.Label(
                p,
                text=f"🔔 Notifications ({len(unread)} unread)",
                font=F["h2"],
                fg=C["text"],
                bg=C["bg"],
            ).pack(anchor="w", padx=32, pady=(16, 8))
            for n in unread[:3]:
                kind_col = {
                    "success": C["green"],
                    "info": C["accent"],
                    "warning": C["yellow"],
                    "error": C["red"],
                }.get(n.get("kind", "info"), C["muted"])
                nf = card_frame(p)
                nf.pack(fill="x", padx=32, pady=3)
                nr = tk.Frame(nf, bg=C["card"])
                nr.pack(fill="x", padx=16, pady=10)
                tk.Frame(nf, bg=kind_col, width=4).place(x=0, y=0, relheight=1)
                tk.Label(
                    nr,
                    text=n["text"],
                    font=F["body"],
                    fg=C["text"],
                    bg=C["card"],
                    wraplength=700,
                    justify="left",
                ).pack(side="left", fill="x", expand=True)
                tk.Label(
                    nr, text=n["time"], font=F["sm"], fg=C["muted"], bg=C["card"]
                ).pack(side="right")

    def _open_event_chat(self, evt):
        grps = jload(F_GROUPS)
        for gid, g in grps.items():
            if g["event_id"] == evt["id"] and self.user["id"] in g["members"]:
                ChatWindow(self, gid, self.user)
                return
        messagebox.showinfo("No Group", "You don't have a group for this event yet.")

    def page_discover(self):
        p = self._scrollable_page()
        events = jload(F_EVENTS)
        uid = self.user["id"]

        self._page_header(p, "Discover Events", "Find and register for upcoming events")

        # filter bar
        fb = tk.Frame(p, bg=C["bg"])
        fb.pack(fill="x", padx=32, pady=(8, 4))
        tk.Label(fb, text="Category:", font=F["body"], fg=C["muted"], bg=C["bg"]).pack(
            side="left"
        )
        cat_v = tk.StringVar(value="All")
        cat_cb = ttk.Combobox(
            fb,
            textvariable=cat_v,
            values=["All"] + list(CAT_COLOR.keys()),
            state="readonly",
            font=F["body"],
            width=16,
        )
        cat_cb.pack(side="left", padx=(6, 16), ipady=4)

        tk.Label(fb, text="Search:", font=F["body"], fg=C["muted"], bg=C["bg"]).pack(
            side="left"
        )
        search_v = tk.StringVar()
        entry(fb, var=search_v, w=24).pack(side="left", ipady=6, padx=(4, 0))

        list_frame = tk.Frame(p, bg=C["bg"])
        list_frame.pack(fill="x")

        def render(evts_to_show):
            for w in list_frame.winfo_children():
                w.destroy()
            if not evts_to_show:
                tk.Label(
                    list_frame,
                    text="No events match your filter.",
                    font=F["body"],
                    fg=C["muted"],
                    bg=C["bg"],
                ).pack(padx=32, pady=16)
                return
            for evt in evts_to_show:
                already = uid in evt["registered"]
                slots_left = evt["max_slots"] - len(evt["registered"])
                if already:
                    bt, bc, bc_fn = "✓ Registered", C["dim"], None
                elif slots_left <= 0:
                    bt, bc, bc_fn = "⊘ Full", C["red"], None
                else:
                    bt = "Register →"
                    bc = C["accent"]
                    bc_fn = lambda e=evt: self._register_event(e, render_all)
                self._event_card(
                    list_frame, evt, btn_text=bt, btn_cmd=bc_fn, btn_color=bc
                )

        def render_all():
            query = search_v.get().strip().lower()
            cat = cat_v.get()
            all_evts = list(events.values())
            filtered = [
                e
                for e in all_evts
                if (cat == "All" or e.get("category") == cat)
                and (
                    not query
                    or query in e["title"].lower()
                    or query in e.get("description", "").lower()
                )
            ]
            render(filtered)

        btn(fb, "Search", render_all, bg=C["accent"], pady=6, padx=12).pack(
            side="left", padx=8
        )
        render_all()

    def _register_event(self, evt, refresh_fn=None):
        forms = jload(F_FORMS)
        if evt.get("form_id") and evt["form_id"] in forms:
            FormFillWindow(
                self,
                evt,
                forms[evt["form_id"]],
                self.user,
                on_done=lambda: (
                    self._switch("discover") if refresh_fn is None else refresh_fn()
                ),
            )
        else:
            # Register without form - still create group chat
            events = jload(F_EVENTS)
            groups = jload(F_GROUPS)
            msgs = jload(F_MESSAGES)
            users = jload(F_USERS)

            if self.user["id"] not in events[evt["id"]]["registered"]:
                events[evt["id"]]["registered"].append(self.user["id"])
                jsave(F_EVENTS, events)

            # Create default group for this event if it doesn't exist
            target_gid = None
            default_group_name = f"{evt['title']} - Participants"
            for gid, g in groups.items():
                if g["event_id"] == evt["id"] and g["name"] == default_group_name:
                    target_gid = gid
                    break

            if not target_gid:
                target_gid = f"grp_{uuid.uuid4().hex[:8]}"
                groups[target_gid] = {
                    "id": target_gid,
                    "event_id": evt["id"],
                    "name": default_group_name,
                    "members": [],
                    "created": today(),
                }

            if self.user["id"] not in groups[target_gid]["members"]:
                groups[target_gid]["members"].append(self.user["id"])

            # Add org to group
            org_id = evt["org_id"]
            if org_id not in groups[target_gid]["members"]:
                groups[target_gid]["members"].append(org_id)

            # Create welcome message if it's a new group
            if target_gid not in msgs:
                msgs[target_gid] = []
                org = users.get(org_id, {})
                msgs[target_gid].append(
                    {
                        "sender_id": org_id,
                        "sender": org.get("name", "Organization"),
                        "text": f"👋 Welcome {self.user['name']}! You've joined the event. Looking forward to seeing you there!",
                        "time": now_str(),
                    }
                )

            jsave(F_EVENTS, events)
            jsave(F_GROUPS, groups)
            jsave(F_MESSAGES, msgs)

            push_notif(
                self.user["id"],
                f"✅ You registered for '{evt['title']}'! 💬 Join the group chat.",
                "success",
            )
            messagebox.showinfo(
                "Registered! 🎉",
                f"You joined '{evt['title']}'!\n\nA group chat has been created for you.",
            )
            self._switch("discover")

    def page_my_events(self):
        p = self._scrollable_page()
        joined = self._joined_events()
        self._page_header(p, "My Events", f"You have joined {len(joined)} event(s)")
        if not joined:
            tk.Label(
                p,
                text="No events joined yet.",
                font=F["body"],
                fg=C["muted"],
                bg=C["bg"],
            ).pack(padx=32, pady=16)
        for evt in joined:
            self._event_card(
                p,
                evt,
                btn_text="💬 Open Chat",
                btn_cmd=lambda e=evt: self._open_event_chat(e),
                btn_color=C["green"],
            )

    def page_chats(self):
        p = self._scrollable_page()
        grps = self._my_groups()
        events = jload(F_EVENTS)
        msgs_all = jload(F_MESSAGES)
        self._page_header(p, "My Group Chats", f"{len(grps)} group(s)")

        if not grps:
            tk.Label(
                p,
                text="No group chats yet. Register for events to get assigned to groups!",
                font=F["body"],
                fg=C["muted"],
                bg=C["bg"],
            ).pack(padx=32, pady=16)
        for gid, g in grps.items():
            evt = events.get(g["event_id"], {})
            msgs = msgs_all.get(gid, [])
            last = (msgs[-1]["text"][:60] + "…") if msgs else "No messages yet"
            unread_cnt = 0  # could track per-user read pointer

            f = card_frame(p)
            f.pack(fill="x", padx=32, pady=5)
            row = tk.Frame(f, bg=C["card"])
            row.pack(fill="x", padx=16, pady=12)
            tk.Label(
                row, text="💬", font=("Segoe UI", 26), bg=C["card"], fg=C["accent"]
            ).pack(side="left")
            c2 = tk.Frame(row, bg=C["card"])
            c2.pack(side="left", padx=10, fill="x", expand=True)
            tk.Label(c2, text=g["name"], font=F["h3"], fg=C["text"], bg=C["card"]).pack(
                anchor="w"
            )
            tk.Label(
                c2,
                text=f"📅 {evt.get('title','?')}  •  👥 {len(g['members'])} members",
                font=F["sm"],
                fg=C["muted"],
                bg=C["card"],
            ).pack(anchor="w")
            tk.Label(c2, text=last, font=F["sm"], fg=C["dim"], bg=C["card"]).pack(
                anchor="w", pady=(3, 0)
            )
            btn(
                row,
                "Open →",
                lambda g_id=gid: ChatWindow(self, g_id, self.user),
                bg=C["accent"],
                pady=6,
                padx=12,
            ).pack(side="right")

    def page_notifs(self):
        p = self._scrollable_page()
        notifs = jload(F_NOTIFS)
        my_notifs = notifs.get(self.user["id"], [])
        unread_cnt = sum(1 for n in my_notifs if not n["read"])
        self._page_header(
            p, "Notifications", f"{unread_cnt} unread  •  {len(my_notifs)} total"
        )

        def mark_all_read():
            for n in my_notifs:
                n["read"] = True
            notifs[self.user["id"]] = my_notifs
            jsave(F_NOTIFS, notifs)
            self._switch("notifs")

        btn(p, "✔ Mark all as read", mark_all_read, bg=C["dim"], pady=6, padx=12).pack(
            anchor="e", padx=32, pady=(8, 4)
        )

        if not my_notifs:
            tk.Label(
                p,
                text="No notifications yet.",
                font=F["body"],
                fg=C["muted"],
                bg=C["bg"],
            ).pack(padx=32, pady=16)

        kind_map = {
            "success": C["green"],
            "info": C["accent"],
            "warning": C["yellow"],
            "error": C["red"],
        }
        for n in my_notifs:
            col = kind_map.get(n.get("kind", "info"), C["muted"])
            f = card_frame(p)
            f.pack(fill="x", padx=32, pady=3)
            # color left bar
            tk.Frame(f, bg=col, width=5).pack(side="left", fill="y")
            body = tk.Frame(f, bg=C["card"] if not n["read"] else C["surface"])
            body.pack(side="left", fill="x", expand=True, padx=14, pady=10)
            tk.Label(
                body,
                text=n["text"],
                font=F["body"],
                fg=C["text"] if not n["read"] else C["muted"],
                bg=body.cget("bg"),
                wraplength=750,
                justify="left",
            ).pack(anchor="w")
            tk.Label(
                body, text=n["time"], font=F["sm"], fg=C["dim"], bg=body.cget("bg")
            ).pack(anchor="w", pady=(4, 0))
            if not n["read"]:
                tk.Frame(f, bg=col, width=10, height=10).place(
                    relx=1, rely=0, x=-16, y=8
                )

    def page_rewards(self):
        p = self._scrollable_page()

        # Refresh user data to get latest points
        users = jload(F_USERS)
        self.user = users.get(self.user["id"], self.user)
        self.app.current_user = self.user

        pts = self.user.get("points", 0)
        joined = self._joined_events()
        level, lv_col = _get_level(pts)

        self._page_header(p, "Rewards & Points", "Your engagement journey")

        # big points display
        pf = card_frame(p)
        pf.pack(fill="x", padx=32, pady=16)
        pi = tk.Frame(pf, bg=C["card"])
        pi.pack(fill="x", padx=24, pady=20)
        tk.Label(
            pi, text="⭐ Total Points", font=F["h2"], fg=C["yellow"], bg=C["card"]
        ).pack(anchor="w")
        tk.Label(
            pi,
            text=str(pts),
            font=("Segoe UI", 52, "bold"),
            fg=C["yellow"],
            bg=C["card"],
        ).pack(anchor="w")
        tk.Label(
            pi, text=f"Current Level: {level}", font=F["h3"], fg=lv_col, bg=C["card"]
        ).pack(anchor="w", pady=(4, 0))

        # progress bar to next level
        thresholds = {"Bronze": 0, "Silver": 200, "Gold": 500, "Platinum": 1000}
        next_map = {"Bronze": 200, "Silver": 500, "Gold": 1000, "Platinum": 9999}
        lo = thresholds[level]
        hi = next_map[level]
        pct = min(100, int(100 * (pts - lo) / (hi - lo))) if hi > lo else 100
        pb_row = tk.Frame(pi, bg=C["card"])
        pb_row.pack(anchor="w", pady=(10, 0), fill="x")
        tk.Label(
            pb_row,
            text=f"Progress to next level: {pct}%",
            font=F["sm"],
            fg=C["muted"],
            bg=C["card"],
        ).pack(anchor="w", pady=(0, 4))
        pb_bg = tk.Frame(pb_row, bg=C["border"], height=12, width=500)
        pb_bg.pack(anchor="w")
        pb_bg.pack_propagate(False)
        tk.Frame(pb_bg, bg=lv_col, width=int(500 * pct / 100), height=12).place(
            x=0, y=0
        )

        # level tiers
        tk.Label(p, text="Level Tiers", font=F["h2"], fg=C["text"], bg=C["bg"]).pack(
            anchor="w", padx=32, pady=(16, 8)
        )
        tier_row = tk.Frame(p, bg=C["bg"])
        tier_row.pack(fill="x", padx=32)
        tiers = [
            ("🥉 Bronze", "0 – 199 pts", C["orange"], 0, 200),
            ("🥈 Silver", "200 – 499 pts", C["muted"], 200, 500),
            ("🥇 Gold", "500 – 999 pts", C["yellow"], 500, 1000),
            ("💎 Platinum", "1000+ pts", C["purple"], 1000, 99999),
        ]
        for name, rng, col, lo2, hi2 in tiers:
            tf = card_frame(tier_row)
            tf.pack(side="left", fill="x", expand=True, padx=4)
            tk.Label(tf, text=name, font=F["h3"], fg=col, bg=C["card"]).pack(
                padx=14, pady=(14, 2), anchor="w"
            )
            tk.Label(tf, text=rng, font=F["sm"], fg=C["muted"], bg=C["card"]).pack(
                padx=14, anchor="w"
            )
            here = lo2 <= pts < hi2 or (level == "Platinum" and name == "💎 Platinum")
            if here:
                tk.Label(
                    tf,
                    text="← You're here",
                    font=("Segoe UI", 9, "bold"),
                    fg=col,
                    bg=C["card"],
                ).pack(padx=14, pady=(2, 14), anchor="w")
            else:
                tk.Frame(tf, bg=C["card"], height=14).pack()

        # contribution log
        tk.Label(
            p, text="Event Contribution Log", font=F["h2"], fg=C["text"], bg=C["bg"]
        ).pack(anchor="w", padx=32, pady=(20, 8))
        if not joined:
            tk.Label(
                p,
                text="Join events to earn points!",
                font=F["body"],
                fg=C["muted"],
                bg=C["bg"],
            ).pack(padx=32)
        for e in joined:
            f = card_frame(p)
            f.pack(fill="x", padx=32, pady=4)
            row = tk.Frame(f, bg=C["card"])
            row.pack(fill="x", padx=16, pady=10)
            cat_col = CAT_COLOR.get(e.get("category", ""), C["muted"])
            tk.Label(
                row,
                text=f"● {e.get('category','')}",
                font=F["sm"],
                fg=cat_col,
                bg=C["card"],
            ).pack(side="left")
            tk.Label(
                row, text=f"  {e['title']}", font=F["bold"], fg=C["text"], bg=C["card"]
            ).pack(side="left")
            tk.Label(
                row, text=f"📅 {e['date']}", font=F["sm"], fg=C["muted"], bg=C["card"]
            ).pack(side="left", padx=16)
            tk.Label(
                row,
                text=f"+{e.get('points',0)} pts",
                font=F["h3"],
                fg=C["yellow"],
                bg=C["card"],
            ).pack(side="right", padx=16)

    def page_profile(self):
        p = self._scrollable_page()
        users = jload(F_USERS)
        u = users.get(self.user["id"], self.user)
        # Keep session user in sync
        self.user = u
        self.app.current_user = u
        self._page_header(p, "My Profile", "View and edit your information")

        # profile card
        pf = card_frame(p)
        pf.pack(fill="x", padx=32, pady=16)
        pi = tk.Frame(pf, bg=C["card"])
        pi.pack(fill="x", padx=24, pady=20)

        left_p = tk.Frame(pi, bg=C["card"])
        left_p.pack(side="left")
        tk.Label(
            left_p,
            text=u.get("avatar", "👤"),
            font=("Segoe UI", 64),
            bg=C["card"],
            fg=C["text"],
        ).pack()
        level, lv_col = _get_level(u.get("points", 0))
        tk.Label(left_p, text=f"🎖️ {level}", font=F["h3"], fg=lv_col, bg=C["card"]).pack(
            pady=(4, 0)
        )

        right_p = tk.Frame(pi, bg=C["card"])
        right_p.pack(side="left", padx=32, fill="x", expand=True)
        tk.Label(
            right_p,
            text=u["name"],
            font=("Segoe UI", 22, "bold"),
            fg=C["text"],
            bg=C["card"],
        ).pack(anchor="w")
        tk.Label(
            right_p,
            text=f"@{u['id']}  •  {u['email']}",
            font=F["body"],
            fg=C["muted"],
            bg=C["card"],
        ).pack(anchor="w", pady=(2, 0))
        tk.Label(
            right_p,
            text=f"{u.get('course','')} · {u.get('year','')}",
            font=F["body"],
            fg=C["accent"],
            bg=C["card"],
        ).pack(anchor="w", pady=(4, 0))
        tk.Label(
            right_p,
            text=u.get("bio", "No bio yet."),
            font=F["body"],
            fg=C["muted"],
            bg=C["card"],
            wraplength=500,
        ).pack(anchor="w", pady=(6, 0))
        tk.Label(
            right_p,
            text=f"⭐ {u.get('points',0)} pts  •  Joined: {u.get('joined','')}",
            font=F["body"],
            fg=C["yellow"],
            bg=C["card"],
        ).pack(anchor="w", pady=(8, 0))

        # edit form
        tk.Label(p, text="Edit Profile", font=F["h2"], fg=C["text"], bg=C["bg"]).pack(
            anchor="w", padx=32, pady=(16, 8)
        )
        ef = card_frame(p)
        ef.pack(fill="x", padx=32, pady=(0, 32))
        ei = tk.Frame(ef, bg=C["card"])
        ei.pack(fill="x", padx=24, pady=20)

        ev = {}
        for lbl_txt, key in [
            ("Display Name", "name"),
            ("Email", "email"),
            ("Course", "course"),
        ]:
            tk.Label(
                ei, text=lbl_txt, font=F["body"], fg=C["muted"], bg=C["card"]
            ).pack(anchor="w", pady=(10, 2))
            v = tk.StringVar(value=u.get(key, ""))
            ev[key] = v
            entry(ei, var=v, w=40).pack(ipady=8, anchor="w", fill="x")

        tk.Label(
            ei, text="Year Level", font=F["body"], fg=C["muted"], bg=C["card"]
        ).pack(anchor="w", pady=(10, 2))
        yr_v = tk.StringVar(value=u.get("year", "1st Year"))
        ttk.Combobox(
            ei,
            textvariable=yr_v,
            values=["1st Year", "2nd Year", "3rd Year", "4th Year", "5th Year"],
            state="readonly",
            font=F["body"],
            width=20,
        ).pack(ipady=6, anchor="w")

        tk.Label(ei, text="Bio", font=F["body"], fg=C["muted"], bg=C["card"]).pack(
            anchor="w", pady=(10, 2)
        )
        bio_box = scrolledtext.ScrolledText(
            ei,
            height=3,
            width=50,
            font=F["body"],
            bg=C["surface"],
            fg=C["text"],
            insertbackground=C["text"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=C["border"],
        )
        bio_box.insert("1.0", u.get("bio", ""))
        bio_box.pack(fill="x")

        def save_profile():
            users2 = jload(F_USERS)
            uid = self.user["id"]
            users2[uid]["name"] = ev["name"].get().strip() or users2[uid]["name"]
            users2[uid]["email"] = ev["email"].get().strip() or users2[uid]["email"]
            users2[uid]["course"] = ev["course"].get().strip()
            users2[uid]["year"] = yr_v.get()
            users2[uid]["bio"] = bio_box.get("1.0", "end").strip()
            jsave(F_USERS, users2)
            self.user = users2[uid]
            self.app.current_user = users2[uid]
            messagebox.showinfo("Saved", "Profile updated!")
            self._switch("profile")

        btn(ei, "💾  Save Changes", save_profile, bg=C["green"], pady=12).pack(
            anchor="w", pady=(16, 0)
        )


# ═══════════════════════════════════════════════════════════════════════════
#  FORM FILL POPUP  (student registers for event with custom form)
# ═══════════════════════════════════════════════════════════════════════════
class FormFillWindow(tk.Toplevel):
    def __init__(self, master, evt, form, user, on_done=None):
        super().__init__(master)
        self.evt = evt
        self.form = form
        self.user = user
        self.on_done = on_done
        self.title(f"Register: {evt['title']}")
        self.geometry("640x580")
        self.configure(bg=C["bg"])
        self._answers = {}
        self._build()

    def _build(self):
        tk.Label(
            self,
            text=f"📋 {self.form['title']}",
            font=F["h2"],
            fg=C["text"],
            bg=C["bg"],
        ).pack(pady=(20, 2), padx=24, anchor="w")
        tk.Label(
            self,
            text=f"For: {self.evt['title']}  •  {self.evt['date']}  •  {self.evt['location']}",
            font=F["sm"],
            fg=C["muted"],
            bg=C["bg"],
        ).pack(padx=24, anchor="w")
        tk.Label(
            self,
            text="* Required fields are marked with an asterisk",
            font=F["sm"],
            fg=C["dim"],
            bg=C["bg"],
        ).pack(padx=24, anchor="w", pady=(2, 0))
        sep(self).pack(fill="x", padx=24, pady=12)

        outer, inner = scrollable_frame(self)
        outer.pack(fill="both", expand=True, padx=24)

        for q in self.form["questions"]:
            qf = tk.Frame(inner, bg=C["bg"])
            qf.pack(fill="x", pady=12)
            req_star = " *" if q.get("required") else ""
            grp_note = (
                "  (determines your group chat)" if q.get("assigns_to_group") else ""
            )
            lbl_row = tk.Frame(qf, bg=C["bg"])
            lbl_row.pack(fill="x")
            tk.Label(
                lbl_row,
                text=f"{q['text']}{req_star}",
                font=F["h3"],
                fg=C["text"],
                bg=C["bg"],
            ).pack(side="left")
            if grp_note:
                tk.Label(
                    lbl_row, text=grp_note, font=F["sm"], fg=C["green"], bg=C["bg"]
                ).pack(side="left")

            if q["type"] == "choice":
                opts = q.get("options", [])
                v = tk.StringVar(value=opts[0] if opts else "")
                self._answers[q["id"]] = v
                opt_row = tk.Frame(qf, bg=C["bg"])
                opt_row.pack(anchor="w", padx=8, pady=(4, 0))
                for opt in opts:
                    tk.Radiobutton(
                        opt_row,
                        text=opt,
                        variable=v,
                        value=opt,
                        bg=C["bg"],
                        fg=C["text"],
                        activebackground=C["bg"],
                        activeforeground=C["text"],
                        selectcolor=C["accent"],
                        highlightthickness=0,
                        font=F["body"],
                        cursor="hand2",
                    ).pack(side="left", padx=12, pady=4)
            else:
                v = tk.StringVar()
                self._answers[q["id"]] = v
                entry(qf, var=v, w=56).pack(ipady=8, anchor="w", padx=4)

        sep(self).pack(fill="x", padx=24, pady=12)

        def submit():
            # check required
            for q in self.form["questions"]:
                if q.get("required"):
                    val = self._answers[q["id"]].get().strip()
                    if not val:
                        messagebox.showwarning(
                            "Required", f"Please answer: {q['text']}"
                        )
                        return

            events = jload(F_EVENTS)
            groups = jload(F_GROUPS)
            responses = jload(F_RESPONSES)
            msgs = jload(F_MESSAGES)
            users = jload(F_USERS)

            resp_data = {}
            assigned_group = None
            for q in self.form["questions"]:
                val = self._answers[q["id"]].get().strip()
                resp_data[q["text"]] = val
                if q.get("assigns_to_group") and val:
                    assigned_group = val

            resp_key = f"{self.evt['id']}_{self.user['id']}"
            responses[resp_key] = resp_data

            if self.user["id"] not in events[self.evt["id"]]["registered"]:
                events[self.evt["id"]]["registered"].append(self.user["id"])

            if assigned_group:
                target_gid = None
                for gid, g in groups.items():
                    if g["event_id"] == self.evt["id"] and g["name"] == assigned_group:
                        target_gid = gid
                        break
                if not target_gid:
                    target_gid = f"grp_{uuid.uuid4().hex[:8]}"
                    groups[target_gid] = {
                        "id": target_gid,
                        "event_id": self.evt["id"],
                        "name": assigned_group,
                        "members": [],
                        "created": today(),
                    }
                if self.user["id"] not in groups[target_gid]["members"]:
                    groups[target_gid]["members"].append(self.user["id"])
                # also add the org
                org_id = self.evt["org_id"]
                if org_id not in groups[target_gid]["members"]:
                    groups[target_gid]["members"].append(org_id)

                # Create welcome message
                if target_gid not in msgs:
                    msgs[target_gid] = []

                org = users.get(org_id, {})
                # Only add welcome if this is the first message (new group)
                first_msg_exists = any(
                    m.get("sender_id") == org_id and "Welcome" in m.get("text", "")
                    for m in msgs[target_gid]
                )
                if not first_msg_exists:
                    msgs[target_gid].insert(
                        0,
                        {
                            "sender_id": org_id,
                            "sender": org.get("name", "Organization"),
                            "text": f"👋 Welcome {self.user['name']}! You've been assigned to the **{assigned_group}** team. Excited to have you!",
                            "time": now_str(),
                        },
                    )

                push_notif(
                    self.user["id"],
                    f"💬 You've been added to the '{assigned_group}' group chat for '{self.evt['title']}'!",
                    "success",
                )
            else:
                # No group assignment, but create default group for event
                default_group_name = f"{self.evt['title']} - Participants"
                target_gid = None
                for gid, g in groups.items():
                    if (
                        g["event_id"] == self.evt["id"]
                        and g["name"] == default_group_name
                    ):
                        target_gid = gid
                        break

                if not target_gid:
                    target_gid = f"grp_{uuid.uuid4().hex[:8]}"
                    groups[target_gid] = {
                        "id": target_gid,
                        "event_id": self.evt["id"],
                        "name": default_group_name,
                        "members": [],
                        "created": today(),
                    }

                if self.user["id"] not in groups[target_gid]["members"]:
                    groups[target_gid]["members"].append(self.user["id"])

                org_id = self.evt["org_id"]
                if org_id not in groups[target_gid]["members"]:
                    groups[target_gid]["members"].append(org_id)

                # Create welcome message
                if target_gid not in msgs:
                    msgs[target_gid] = []
                    org = users.get(org_id, {})
                    msgs[target_gid].append(
                        {
                            "sender_id": org_id,
                            "sender": org.get("name", "Organization"),
                            "text": f"👋 Welcome {self.user['name']}! You've registered for the event. See you there!",
                            "time": now_str(),
                        }
                    )

            jsave(F_EVENTS, events)
            jsave(F_GROUPS, groups)
            jsave(F_RESPONSES, responses)
            jsave(F_MESSAGES, msgs)

            grp_msg = (
                f"\n\n💬 Group Chat: '{assigned_group}'"
                if assigned_group
                else "\n\n💬 Group Chat: Event Participants"
            )
            reg_msg = f"Successfully registered for '{self.evt['title']}'!{grp_msg}\n\n⭐ Points awarded upon attendance!"
            messagebox.showinfo("Registered! 🎉", reg_msg)
            self.destroy()
            if self.on_done:
                self.on_done()

        btn(self, "✅  Confirm Registration", submit, bg=C["green"], pady=12).pack(
            padx=24, pady=8, anchor="w"
        )
        btn(self, "Cancel", self.destroy, bg=C["dim"], pady=8, padx=12).pack(
            padx=24, anchor="w"
        )


# ═══════════════════════════════════════════════════════════════════════════
#  CHAT WINDOW
# ═══════════════════════════════════════════════════════════════════════════
class ChatWindow(tk.Toplevel):
    def __init__(self, master, gid, user):
        super().__init__(master)
        self.gid = gid
        self.user = user
        groups = jload(F_GROUPS)
        events = jload(F_EVENTS)
        self.grp = groups.get(gid, {})
        self.evt = events.get(self.grp.get("event_id", ""), {})
        self.title(f"💬 {self.grp.get('name','')} — {self.evt.get('title','')}")
        self.geometry("680x580")
        self.configure(bg=C["bg"])
        self._build()
        self._load()

    def _build(self):
        # header
        hdr = tk.Frame(self, bg=C["surface"])
        hdr.pack(fill="x")
        tk.Label(
            hdr,
            text=f"💬  {self.grp.get('name','Group')}",
            font=F["h3"],
            fg=C["text"],
            bg=C["surface"],
        ).pack(side="left", padx=16, pady=12)
        users = jload(F_USERS)
        members = [
            users.get(m, {}).get("name", "?") for m in self.grp.get("members", [])
        ]
        tk.Label(
            hdr,
            text=f"👥 {', '.join(members[:4])}{'...' if len(members)>4 else ''}",
            font=F["sm"],
            fg=C["muted"],
            bg=C["surface"],
        ).pack(side="left")
        tk.Label(
            hdr,
            text=f"📅 {self.evt.get('title','')}",
            font=F["sm"],
            fg=C["dim"],
            bg=C["surface"],
        ).pack(side="right", padx=16)
        sep(self).pack(fill="x")

        # scrollable message area
        outer, self.msg_frame = scrollable_frame(self)
        outer.pack(fill="both", expand=True)

        # store canvas ref for scroll-to-bottom
        # Find the canvas inside outer
        self._msg_canvas = None
        for child in outer.winfo_children():
            if isinstance(child, tk.Canvas):
                self._msg_canvas = child
                break

        # input bar
        sep(self).pack(fill="x")
        inp = tk.Frame(self, bg=C["surface"])
        inp.pack(fill="x", side="bottom")
        row = tk.Frame(inp, bg=C["surface"])
        row.pack(fill="x", padx=12, pady=10)
        self._msg_var = tk.StringVar()
        e = entry(row, var=self._msg_var, w=52)
        e.pack(side="left", fill="x", expand=True, ipady=9, padx=(0, 8))
        e.bind("<Return>", lambda ev: self._send())
        btn(row, "Send ➤", self._send, bg=C["accent"], pady=8, padx=16).pack(
            side="left"
        )

    def _load(self):
        for w in self.msg_frame.winfo_children():
            w.destroy()
        msgs = jload(F_MESSAGES).get(self.gid, [])
        if not msgs:
            tk.Label(
                self.msg_frame,
                text="No messages yet. Say hello! 👋",
                font=F["body"],
                fg=C["dim"],
                bg=C["bg"],
            ).pack(pady=24)

        for m in msgs:
            is_me = m["sender_id"] == self.user["id"]
            outer = tk.Frame(self.msg_frame, bg=C["bg"])
            outer.pack(fill="x", padx=12, pady=3)

            bubble = tk.Frame(outer, bg=C["accent"] if is_me else C["card"])
            bubble.pack(
                side="right" if is_me else "left",
                padx=(60 if is_me else 0, 0 if is_me else 60),
            )

            if not is_me:
                tk.Label(
                    bubble,
                    text=m.get("sender", ""),
                    font=F["sm"],
                    fg=C["muted"],
                    bg=C["card"],
                ).pack(anchor="w", padx=10, pady=(6, 0))
            tk.Label(
                bubble,
                text=m["text"],
                font=F["body"],
                fg=C["bg"] if is_me else C["text"],
                bg=C["accent"] if is_me else C["card"],
                wraplength=420,
                justify="left",
            ).pack(padx=10, pady=(4, 2))
            tk.Label(
                bubble,
                text=m.get("time", ""),
                font=F["sm"],
                fg=(C["bg"] if is_me else C["dim"]),
                bg=C["accent"] if is_me else C["card"],
            ).pack(padx=10, pady=(0, 6), anchor="e")

        self.msg_frame.update_idletasks()
        if self._msg_canvas:
            self._msg_canvas.yview_moveto(1.0)

    def _send(self):
        txt = self._msg_var.get().strip()
        if not txt:
            return
        msgs = jload(F_MESSAGES)
        if self.gid not in msgs:
            msgs[self.gid] = []
        msgs[self.gid].append(
            {
                "sender_id": self.user["id"],
                "sender": self.user["name"],
                "text": txt,
                "time": now_str(),
            }
        )
        jsave(F_MESSAGES, msgs)
        self._msg_var.set("")
        self._load()


# ─────────────────────────── UTILITY ───────────────────────────────────────
def _get_level(pts):
    if pts >= 1000:
        return "Platinum", C["purple"]
    if pts >= 500:
        return "Gold", C["yellow"]
    if pts >= 200:
        return "Silver", C["muted"]
    return "Bronze", C["orange"]


# ═══════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()
