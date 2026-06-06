"""
Database module for CampusConnect - handles JSON data persistence.
"""

import json
import hashlib
import datetime
import uuid
from pathlib import Path


# ─────────────────────────── FILE PATHS ────────────────────────────────────
BASE = Path(__file__).parent.parent
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


# ─────────────────────────── JSON HELPERS ──────────────────────────────────
def jload(path):
    """Load JSON data from file, return empty dict if not exists."""
    try:
        if path.exists():
            with open(path, encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def jsave(path, data):
    """Save data as JSON to file."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ─────────────────────────── CRYPTOGRAPHY ──────────────────────────────────
def hash_pw(pw):
    """Hash password using SHA256."""
    return hashlib.sha256(pw.encode()).hexdigest()


# ─────────────────────────── TIME & DATE ───────────────────────────────────
def now_str():
    """Get current timestamp as string."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def today():
    """Get today's date as string."""
    return datetime.datetime.now().strftime("%Y-%m-%d")


# ─────────────────────────── NOTIFICATIONS ─────────────────────────────────
def push_notif(user_id, text, kind="info"):
    """Push a notification to a user."""
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
    """Initialize database with seed data if empty."""
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
