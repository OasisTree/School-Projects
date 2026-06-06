"""
Dashboard screens for CampusConnect - Admin, Organization, and Student views.
This is a large module containing all dashboard functionality.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import uuid
from core.database import (
    jload, jsave, F_USERS, F_EVENTS, F_FORMS, F_GROUPS, F_MESSAGES, F_RESPONSES,
    F_ATTENDANCE, F_NOTIFS, now_str, today, push_notif
)
from core.theme import COLORS as C, FONTS as F, CATEGORY_COLORS as CAT_COLOR
from core.utils import get_bg, get_level
from ui.widgets import lbl, sep, card_frame, btn, entry, scrollable_frame, badge
from ui.windows import FormFillWindow, ChatWindow


class BaseDashboard(tk.Frame):
    """Base class for all dashboard views."""
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
        tk.Label(top, text="🎓", font=("Segoe UI", 22),
                 bg=C["surface"], fg=self.ROLE_COLOR).pack(side="left")
        c = tk.Frame(top, bg=C["surface"])
        c.pack(side="left", padx=8)
        tk.Label(c, text="CampusConnect",
                 font=("Segoe UI", 12, "bold"), fg=C["text"], bg=C["surface"]).pack(anchor="w")
        tk.Label(c, text=self.ROLE_LABEL, font=F["sm"],
                 fg=self.ROLE_COLOR, bg=C["surface"]).pack(anchor="w")

        sep(self.sb).pack(fill="x", padx=12)

        # profile card
        pc = tk.Frame(self.sb, bg=C["card"])
        pc.pack(fill="x", padx=10, pady=10)
        tk.Label(pc, text=self.user.get("avatar", "👤"),
                 font=("Segoe UI", 28), bg=C["card"], fg=C["text"],
                 padx=10, pady=8).pack(side="left")
        pc2 = tk.Frame(pc, bg=C["card"])
        pc2.pack(side="left", pady=8, fill="x", expand=True)
        tk.Label(pc2, text=self.user["name"], font=F["bold"],
                 fg=C["text"], bg=C["card"]).pack(anchor="w")
        sub = self.user.get("course") or self.user["role"].capitalize()
        tk.Label(pc2, text=sub[:28], font=F["sm"],
                 fg=C["muted"], bg=C["card"]).pack(anchor="w")
        if self.user["role"] == "student":
            pts = self.user.get("points", 0)
            tk.Label(pc2, text=f"⭐ {pts} pts",
                     font=F["sm"], fg=C["yellow"], bg=C["card"]).pack(anchor="w")

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
        tk.Label(logout_row, text="⬅", font=("Segoe UI", 14),
                 bg=C["surface"], fg=C["muted"], padx=10, pady=8).pack(side="left")
        tk.Label(logout_row, text="Log Out", font=F["body"],
                 bg=C["surface"], fg=C["muted"]).pack(side="left", pady=8)
        logout_row.bind("<Button-1>", lambda e: self.app.go_login())
        for w in logout_row.winfo_children():
            w.bind("<Button-1>", lambda e: self.app.go_login())
        logout_row.bind("<Enter>", lambda e: logout_row.config(bg=C["hover"]))
        logout_row.bind("<Leave>", lambda e: logout_row.config(bg=C["surface"]))

    def _make_nav(self, parent, icon, key, text):
        f = tk.Frame(parent, bg=C["surface"], cursor="hand2")
        f.pack(fill="x", pady=1)
        ico_lbl = tk.Label(f, text=icon, font=("Segoe UI", 14),
                           bg=C["surface"], fg=C["muted"], padx=10, pady=8)
        ico_lbl.pack(side="left")
        txt_lbl = tk.Label(f, text=text, font=F["body"],
                           bg=C["surface"], fg=C["muted"])
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
                tk.Label(self.main,
                         text=f"⚠ Error loading page: {ex}",
                         font=F["body"], fg=C["red"], bg=C["bg"],
                         wraplength=600).pack(padx=40, pady=40)

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
        tk.Label(left, text=title, font=F["h1"],
                 fg=C["text"], bg=C["bg"]).pack(anchor="w")
        if subtitle:
            tk.Label(left, text=subtitle, font=F["body"],
                     fg=C["muted"], bg=C["bg"]).pack(anchor="w", pady=(2, 0))
        if action_txt and action_fn:
            btn(row, action_txt, action_fn,
                bg=self.ROLE_COLOR, pady=10).pack(side="right")
        sep(parent).pack(fill="x", padx=32, pady=(8, 4))

    def _stat_card(self, parent, icon, value, label_text, color=None):
        f = tk.Frame(parent, bg=C["card"], padx=20, pady=16)
        top = tk.Frame(f, bg=C["card"])
        top.pack(fill="x")
        tk.Label(top, text=icon, font=("Segoe UI", 22),
                 bg=C["card"], fg=color or C["accent"]).pack(side="left")
        tk.Label(f, text=str(value), font=("Segoe UI", 28, "bold"),
                 fg=color or C["accent"], bg=C["card"]).pack(anchor="w", pady=(4, 0))
        tk.Label(f, text=label_text, font=F["sm"],
                 fg=C["muted"], bg=C["card"]).pack(anchor="w")
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
        tk.Label(top_row, text=f"● {evt.get('category','General')}",
                 font=F["sm"], fg=col, bg=C["card"]).pack(side="left")
        tk.Label(top_row, text=f"  ★ {evt.get('points',0)} pts",
                 font=F["sm"], fg=C["yellow"], bg=C["card"]).pack(side="left")
        slots_left = evt["max_slots"] - len(evt["registered"])
        status_col = C["green"] if slots_left > 5 else C["yellow"] if slots_left > 0 else C["red"]
        tk.Label(top_row, text=f"  {slots_left} slots left",
                 font=F["sm"], fg=status_col, bg=C["card"]).pack(side="left")

        tk.Label(body, text=evt["title"], font=F["h2"],
                 fg=C["text"], bg=C["card"]).pack(anchor="w", pady=(4, 6))

        info = tk.Frame(body, bg=C["card"])
        info.pack(fill="x")
        for ico, val in [("📅", evt["date"]), ("🕐", evt["time"]),
                         ("📍", evt["location"]), ("🏢", org.get("name",""))]:
            tk.Label(info, text=f"{ico} {val}",
                     font=F["sm"], fg=C["muted"], bg=C["card"], padx=4).pack(side="left")

        if evt.get("description"):
            desc = evt["description"][:140] + ("…" if len(evt["description"]) > 140 else "")
            tk.Label(body, text=desc, font=F["sm"], fg=C["muted"],
                     bg=C["card"], wraplength=780, justify="left").pack(
                         anchor="w", pady=(6, 0))

        # tags
        if evt.get("tags"):
            tag_row = tk.Frame(body, bg=C["card"])
            tag_row.pack(anchor="w", pady=(6, 0))
            for tag in evt["tags"][:4]:
                t = tk.Frame(tag_row, bg=C["border"], padx=6, pady=2)
                t.pack(side="left", padx=(0, 4))
                tk.Label(t, text=f"#{tag}", font=F["sm"],
                         fg=C["muted"], bg=C["border"]).pack()

        # action button
        if btn_text:
            btn(body, btn_text, btn_cmd,
                bg=btn_color or C["accent"], pady=6, padx=14).pack(
                    anchor="e", pady=(8, 0))
        return f


# ═══════════════════════════════════════════════════════════════════════════
# ADMIN DASHBOARD
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

    def page_overview(self):
        p = self._scrollable_page()
        users = jload(F_USERS)
        events = jload(F_EVENTS)
        students = [u for u in users.values() if u["role"] == "student"]
        orgs = [u for u in users.values() if u["role"] == "org"]
        total_reg = sum(len(e["registered"]) for e in events.values())

        self._page_header(p, "Admin Overview",
                          f"System snapshot — {today()}")
        self._stat_row(p, [
            ("👤", len(students), "Total Students", C["accent"]),
            ("🏢", len(orgs), "Organizations", C["purple"]),
            ("📅", len(events), "Events", C["green"]),
            ("✍️", total_reg, "Registrations", C["yellow"]),
        ])

        # ── recent events list ──
        tk.Label(p, text="All Events", font=F["h2"],
                 fg=C["text"], bg=C["bg"]).pack(anchor="w", padx=32, pady=(8, 8))
        for evt in list(events.values())[:5]:
            self._event_card(p, evt,
                             btn_text="📋 Attendance",
                             btn_cmd=lambda e=evt: self._attendance_popup(e),
                             btn_color=C["yellow"])

        # ── course distribution ──
        tk.Label(p, text="Student Enrollment by Course",
                 font=F["h2"], fg=C["text"], bg=C["bg"]).pack(
                     anchor="w", padx=32, pady=(20, 8))
        bc = card_frame(p)
        bc.pack(fill="x", padx=32, pady=(0, 32))
        by_course = {}
        for s in students:
            k = s.get("course", "Unknown")
            by_course[k] = by_course.get(k, 0) + 1
        mx = max(by_course.values(), default=1)
        for i, (course, cnt) in enumerate(sorted(by_course.items(), key=lambda x: -x[1])[:8]):
            row = tk.Frame(bc, bg=C["card"])
            row.pack(fill="x", padx=16, pady=4)
            tk.Label(row, text=course[:32], font=F["body"],
                     fg=C["text"], bg=C["card"], width=34, anchor="w").pack(side="left")
            bar_bg = tk.Frame(row, bg=C["border"], height=14, width=320)
            bar_bg.pack(side="left", padx=8)
            bar_bg.pack_propagate(False)
            bw = max(4, int(320 * cnt / mx))
            tk.Frame(bar_bg, bg=C["accent"], width=bw, height=14).place(x=0, y=0)
            tk.Label(row, text=str(cnt), font=F["sm"],
                     fg=C["muted"], bg=C["card"]).pack(side="left")

    def page_events(self):
        p = self._scrollable_page()
        events = jload(F_EVENTS)
        self._page_header(p, "All Events", f"{len(events)} events in the system")
        for evt in events.values():
            self._event_card(p, evt,
                             btn_text="📋 Mark Attendance",
                             btn_cmd=lambda e=evt: self._attendance_popup(e),
                             btn_color=C["yellow"])

    def _attendance_popup(self, evt):
        win = tk.Toplevel(self)
        win.title(f"Attendance — {evt['title']}")
        win.geometry("620x520")
        win.configure(bg=C["bg"])

        tk.Label(win, text=f"📋 {evt['title']}",
                 font=F["h2"], fg=C["text"], bg=C["bg"]).pack(pady=16, padx=20, anchor="w")
        tk.Label(win, text=f"📅 {evt['date']}  📍 {evt['location']}",
                 font=F["sm"], fg=C["muted"], bg=C["bg"]).pack(padx=20, anchor="w")
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
            tk.Label(inner, text="No students registered yet.",
                     font=F["body"], fg=C["muted"], bg=C["bg"]).pack(padx=8, pady=16)
        for uid in evt["registered"]:
            u = users.get(uid, {})
            if not u:
                continue
            v = tk.BooleanVar(value=att[eid].get(uid, False))
            checks[uid] = v
            row = tk.Frame(inner, bg=C["card"])
            row.pack(fill="x", pady=2)
            tk.Checkbutton(row, variable=v, bg=C["card"], fg=C["text"],
                           activebackground=C["card"],
                           activeforeground=C["accent"],
                           selectcolor=C["accent"],
                           highlightthickness=0).pack(side="left", padx=10, pady=10)
            tk.Label(row,
                     text=f"{u.get('avatar','👤')} {u['name']}",
                     font=F["bold"], fg=C["text"], bg=C["card"]).pack(side="left")
            tk.Label(row,
                     text=f"  {u.get('course','')} · {u.get('year','')}",
                     font=F["sm"], fg=C["muted"], bg=C["card"]).pack(side="left")

        def save_att():
            try:
                newly_marked = []
                newly_unmarked = []

                for uid, v in checks.items():
                    was_present = att[eid].get(uid, False)
                    is_now_present = v.get()

                    if not was_present and is_now_present:
                        newly_marked.append(uid)
                    elif was_present and not is_now_present:
                        newly_unmarked.append(uid)

                    att[eid][uid] = is_now_present

                jsave(F_ATTENDANCE, att)

                users2 = jload(F_USERS)
                points_awarded_count = 0

                for uid in newly_marked:
                    if uid in users2:
                        old_pts = users2[uid].get("points", 0)
                        new_pts = old_pts + evt.get("points", 0)
                        users2[uid]["points"] = new_pts
                        points_awarded_count += 1
                        push_notif(uid,
                                   f"✅ Attendance confirmed for '{evt['title']}'! +{evt.get('points',0)} pts (Total: {new_pts} 🌟)",
                                   "success")

                for uid in newly_unmarked:
                    if uid in users2:
                        old_pts = users2[uid].get("points", 0)
                        new_pts = max(0, old_pts - evt.get("points", 0))
                        users2[uid]["points"] = new_pts
                        push_notif(uid,
                                   f"⚠️ Attendance removed from '{evt['title']}'  -{evt.get('points',0)} pts (Total: {new_pts})",
                                   "warning")

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
        btn(win, "💾  Save Attendance", save_att,
            bg=C["green"], pady=10).pack(padx=20, pady=10, anchor="w")

    def page_users(self):
        p = self._scrollable_page()
        users = jload(F_USERS)
        self._page_header(p, "User Management",
                          f"{len(users)} accounts registered",
                          "➕ Add Demo Student", lambda: self._add_demo_student())

        for role, col in [("admin", C["yellow"]), ("org", C["purple"]), ("student", C["accent"])]:
            role_users = [u for u in users.values() if u["role"] == role]
            if not role_users:
                continue
            tk.Label(p, text=f"  {role.capitalize()}s  ({len(role_users)})",
                     font=F["h2"], fg=col, bg=C["bg"]).pack(
                         anchor="w", padx=32, pady=(20, 6))
            for u in role_users:
                f = card_frame(p)
                f.pack(fill="x", padx=32, pady=3)
                row = tk.Frame(f, bg=C["card"])
                row.pack(fill="x", padx=16, pady=12)
                tk.Label(row, text=u.get("avatar", "👤"),
                         font=("Segoe UI", 24), bg=C["card"], fg=C["text"]).pack(side="left")
                c2 = tk.Frame(row, bg=C["card"])
                c2.pack(side="left", padx=10, fill="x", expand=True)
                tk.Label(c2, text=u["name"], font=F["h3"],
                         fg=C["text"], bg=C["card"]).pack(anchor="w")
                info_txt = f"{u['email']}  •  Joined: {u.get('joined','')}  •  {u.get('course','')} {u.get('year','')}"
                tk.Label(c2, text=info_txt, font=F["sm"],
                         fg=C["muted"], bg=C["card"]).pack(anchor="w")
                if u["role"] == "student":
                    tk.Label(c2, text=f"⭐ {u.get('points',0)} pts  •  {u.get('bio','')[:50]}",
                             font=F["sm"], fg=C["yellow"], bg=C["card"]).pack(anchor="w")
                tk.Label(row, text=role.upper(), font=F["sm"],
                         fg=col, bg=C["card"]).pack(side="right")
                btn(row, "Remove", lambda uid=u["id"]: self._remove_user(uid),
                    bg=C["red"], pady=4, padx=8,
                    font=F["sm"]).pack(side="right", padx=8)

    def _remove_user(self, uid):
        if uid == self.user["id"]:
            messagebox.showwarning("Action Blocked", "You cannot remove your own account.")
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
            "password": jload(F_USERS).get("student1", {}).get("password"),
            "role": "student",
            "course": "BS General Studies",
            "year": "1st Year",
            "joined": today(),
            "avatar": "🧑‍🎓",
            "points": 0,
            "bio": "Demo account"
        }
        jsave(F_USERS, users)
        messagebox.showinfo("Done", f"Created demo{i} / demo123")
        self._switch("users")

    def page_analytics(self):
        p = self._scrollable_page()
        events = jload(F_EVENTS)
        att = jload(F_ATTENDANCE)
        users = jload(F_USERS)
        self._page_header(p, "Analytics & Reports", "Engagement insights")

        # ── registrations per event ──
        tk.Label(p, text="Registrations per Event",
                 font=F["h2"], fg=C["text"], bg=C["bg"]).pack(anchor="w", padx=32, pady=(16, 8))
        f1 = card_frame(p)
        f1.pack(fill="x", padx=32, pady=(0, 16))
        sorted_evts = sorted(events.values(), key=lambda e: len(e["registered"]), reverse=True)
        mx = max((len(e["registered"]) for e in sorted_evts), default=1)
        for evt in sorted_evts[:8]:
            row = tk.Frame(f1, bg=C["card"])
            row.pack(fill="x", padx=16, pady=5)
            col = CAT_COLOR.get(evt.get("category", ""), C["muted"])
            tk.Label(row, text=evt["title"][:32], font=F["body"],
                     fg=C["text"], bg=C["card"], width=32, anchor="w").pack(side="left")
            bar_bg = tk.Frame(row, bg=C["border"], height=16, width=320)
            bar_bg.pack(side="left", padx=8)
            bar_bg.pack_propagate(False)
            bw = max(4, int(320 * len(evt["registered"]) / mx))
            tk.Frame(bar_bg, bg=col, width=bw, height=16).place(x=0, y=0)
            tk.Label(row, text=str(len(evt["registered"])),
                     font=F["sm"], fg=C["muted"], bg=C["card"]).pack(side="left")

        # ── attendance rates ──
        tk.Label(p, text="Attendance Rates",
                 font=F["h2"], fg=C["text"], bg=C["bg"]).pack(anchor="w", padx=32, pady=(16, 8))
        f2 = card_frame(p)
        f2.pack(fill="x", padx=32, pady=(0, 16))
        for evt in sorted_evts:
            total = len(evt["registered"])
            present = sum(1 for uid, v in att.get(evt["id"], {}).items() if v)
            pct = int(100 * present / total) if total else 0
            row = tk.Frame(f2, bg=C["card"])
            row.pack(fill="x", padx=16, pady=5)
            tk.Label(row, text=evt["title"][:32], font=F["body"],
                     fg=C["text"], bg=C["card"], width=32, anchor="w").pack(side="left")
            bar_bg = tk.Frame(row, bg=C["border"], height=14, width=280)
            bar_bg.pack(side="left", padx=8)
            bar_bg.pack_propagate(False)
            tk.Frame(bar_bg, bg=C["green"], width=int(280 * pct / 100), height=14).place(x=0, y=0)
            tk.Label(row, text=f"{present}/{total} ({pct}%)",
                     font=F["sm"], fg=C["muted"], bg=C["card"]).pack(side="left")

        # ── points leaderboard ──
        tk.Label(p, text="Top Students by Points",
                 font=F["h2"], fg=C["text"], bg=C["bg"]).pack(anchor="w", padx=32, pady=(16, 8))
        f3 = card_frame(p)
        f3.pack(fill="x", padx=32, pady=(0, 32))
        students = sorted(
            [u for u in users.values() if u["role"] == "student"],
            key=lambda u: u.get("points", 0), reverse=True
        )[:10]
        medals = ["🥇", "🥈", "🥉"] + ["  "] * 10
        for i, s in enumerate(students):
            row = tk.Frame(f3, bg=C["card"])
            row.pack(fill="x", padx=16, pady=4)
            tk.Label(row, text=medals[i], font=("Segoe UI", 16),
                     bg=C["card"], fg=C["text"]).pack(side="left", padx=8, pady=8)
            tk.Label(row, text=s["name"], font=F["bold"],
                     fg=C["text"], bg=C["card"], width=22, anchor="w").pack(side="left")
            tk.Label(row, text=s.get("course", ""), font=F["sm"],
                     fg=C["muted"], bg=C["card"]).pack(side="left")
            tk.Label(row, text=f"⭐ {s.get('points',0)} pts",
                     font=F["bold"], fg=C["yellow"], bg=C["card"]).pack(side="right", padx=16)

    def page_attendance(self):
        p = self._scrollable_page()
        events = jload(F_EVENTS)
        att = jload(F_ATTENDANCE)
        users = jload(F_USERS)
        self._page_header(p, "Attendance Records", "All event attendance logs")

        for evt in events.values():
            tk.Label(p, text=f"📅 {evt['title']} — {evt['date']}",
                     font=F["h3"], fg=C["text"], bg=C["bg"]).pack(
                         anchor="w", padx=32, pady=(16, 4))
            f = card_frame(p)
            f.pack(fill="x", padx=32, pady=(0, 8))
            if not evt["registered"]:
                tk.Label(f, text="No registrations.",
                         font=F["sm"], fg=C["muted"], bg=C["card"]).pack(padx=16, pady=8, anchor="w")
                continue
            for uid in evt["registered"]:
                u = users.get(uid, {})
                present = att.get(evt["id"], {}).get(uid, False)
                row = tk.Frame(f, bg=C["card"])
                row.pack(fill="x", padx=16, pady=3)
                tk.Label(row, text=u.get("name", uid), font=F["body"],
                         fg=C["text"], bg=C["card"], width=24, anchor="w").pack(side="left")
                tk.Label(row, text=u.get("course", ""), font=F["sm"],
                         fg=C["muted"], bg=C["card"]).pack(side="left")
                status = "✅ Present" if present else "❌ Absent"
                clr = C["green"] if present else C["red"]
                tk.Label(row, text=status, font=F["sm"],
                         fg=clr, bg=C["card"]).pack(side="right", padx=16)

    def page_announce(self):
        p = self._scrollable_page()
        self._page_header(p, "Send Announcement",
                          "Broadcast a message to all students")

        f = card_frame(p)
        f.pack(fill="x", padx=32, pady=16)
        inner = tk.Frame(f, bg=C["card"])
        inner.pack(fill="x", padx=24, pady=20)

        tk.Label(inner, text="Title", font=F["body"],
                 fg=C["muted"], bg=C["card"]).pack(anchor="w", pady=(0, 2))
        title_v = tk.StringVar()
        entry(inner, var=title_v, w=50).pack(ipady=8, anchor="w", fill="x")

        tk.Label(inner, text="Message", font=F["body"],
                 fg=C["muted"], bg=C["card"]).pack(anchor="w", pady=(12, 2))
        msg_box = scrolledtext.ScrolledText(inner, height=4, font=F["body"],
                                            bg=C["surface"], fg=C["text"],
                                            insertbackground=C["text"],
                                            relief="flat", highlightthickness=1,
                                            highlightbackground=C["border"])
        msg_box.pack(fill="x")

        tk.Label(inner, text="Target Audience", font=F["body"],
                 fg=C["muted"], bg=C["card"]).pack(anchor="w", pady=(12, 2))
        aud_v = tk.StringVar(value="All Students")
        ttk.Combobox(inner, textvariable=aud_v,
                     values=["All Students", "All Organizations", "Everyone"],
                     state="readonly", font=F["body"], width=20).pack(ipady=6, anchor="w")

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

        btn(inner, "📢  Broadcast Announcement", send_ann,
            bg=C["yellow"], fg=C["bg"], pady=12).pack(anchor="w", pady=(16, 0))


# ═══════════════════════════════════════════════════════════════════════════
# ORG DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════

# Due to length limitations, OrgDashboard and StudentDashboard will be in a separate file
# Please see dashboards_extended.py for complete implementation
