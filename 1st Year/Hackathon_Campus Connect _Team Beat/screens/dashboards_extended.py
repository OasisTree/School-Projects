"""
Extended Dashboard screens - Organization and Student dashboards.
This module contains the remaining dashboard implementations.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import uuid
from core.database import (
    jload, jsave, F_USERS, F_EVENTS, F_FORMS, F_GROUPS, F_MESSAGES, F_RESPONSES,
    F_ATTENDANCE, F_NOTIFS, now_str, today, push_notif
)
from core.theme import COLORS as C, FONTS as F, CATEGORY_COLORS as CAT_COLOR
from core.utils import get_level
from ui.widgets import sep, card_frame, btn, entry, scrollable_frame
from ui.windows import FormFillWindow, ChatWindow
from screens.dashboards import BaseDashboard


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
        return [e for e in jload(F_EVENTS).values()
                if e["org_id"] == self.user["id"]]

    def page_overview(self):
        p = self._scrollable_page()
        my_evts = self._my_events()
        total_reg = sum(len(e["registered"]) for e in my_evts)
        groups = jload(F_GROUPS)
        my_grps = [g for g in groups.values()
                   if any(e["id"] == g["event_id"] for e in my_evts)]

        self._page_header(p, f"Welcome, {self.user['name'].split()[0]}! 🏢",
                          self.user.get("bio", ""))
        self._stat_row(p, [
            ("📅", len(my_evts), "My Events", C["green"]),
            ("👥", total_reg, "Registrations", C["accent"]),
            ("💬", len(my_grps), "Active Groups", C["yellow"]),
        ])

        tk.Label(p, text="My Recent Events", font=F["h2"],
                 fg=C["text"], bg=C["bg"]).pack(anchor="w", padx=32, pady=(8, 8))
        if not my_evts:
            tk.Label(p, text="No events yet. Create your first event!",
                     font=F["body"], fg=C["muted"], bg=C["bg"]).pack(padx=32)
        for e in my_evts[:3]:
            self._event_card(p, e,
                             btn_text="👥 Registrants",
                             btn_cmd=lambda ev=e: self._registrants_popup(ev),
                             btn_color=C["green"])

    def page_my_events(self):
        p = self._scrollable_page()
        my_evts = self._my_events()
        self._page_header(p, "My Events", f"{len(my_evts)} events",
                          "➕ Create New", lambda: self._switch("create_event"))
        for evt in my_evts:
            self._event_card(p, evt,
                             btn_text="👥 View Registrants",
                             btn_cmd=lambda e=evt: self._registrants_popup(e),
                             btn_color=C["green"])
        if not my_evts:
            tk.Label(p, text="No events yet.", font=F["body"],
                     fg=C["muted"], bg=C["bg"]).pack(padx=32)

    def _registrants_popup(self, evt):
        win = tk.Toplevel(self)
        win.title(f"Registrants — {evt['title']}")
        win.geometry("640x520")
        win.configure(bg=C["bg"])
        users = jload(F_USERS)
        resps = jload(F_RESPONSES)

        tk.Label(win, text=f"👥 {evt['title']}",
                 font=F["h2"], fg=C["text"], bg=C["bg"]).pack(pady=16, padx=20, anchor="w")
        tk.Label(win, text=f"{len(evt['registered'])} registrants",
                 font=F["body"], fg=C["muted"], bg=C["bg"]).pack(padx=20, anchor="w")
        sep(win).pack(fill="x", padx=20, pady=10)

        outer, inner = scrollable_frame(win)
        outer.pack(fill="both", expand=True, padx=20)

        if not evt["registered"]:
            tk.Label(inner, text="No registrations yet.",
                     font=F["body"], fg=C["muted"], bg=C["bg"]).pack(pady=20)
        for uid in evt["registered"]:
            u = users.get(uid, {})
            if not u:
                continue
            f = card_frame(inner)
            f.pack(fill="x", pady=4)
            row = tk.Frame(f, bg=C["card"])
            row.pack(fill="x", padx=12, pady=10)
            tk.Label(row, text=u.get("avatar", "👤"),
                     font=("Segoe UI", 22), bg=C["card"], fg=C["text"]).pack(side="left")
            c2 = tk.Frame(row, bg=C["card"])
            c2.pack(side="left", padx=10)
            tk.Label(c2, text=u.get("name", uid), font=F["h3"],
                     fg=C["text"], bg=C["card"]).pack(anchor="w")
            tk.Label(c2, text=f"{u.get('course','')} · {u.get('year','')}",
                     font=F["sm"], fg=C["muted"], bg=C["card"]).pack(anchor="w")
            resp_key = f"{evt['id']}_{uid}"
            resp = resps.get(resp_key, {})
            if resp:
                short = "  |  ".join(f"{k[:20]}: {str(v)[:20]}"
                                     for k, v in resp.items() if k != "group")
                tk.Label(c2, text=f"📋 {short[:80]}",
                         font=F["sm"], fg=C["purple"], bg=C["card"]).pack(anchor="w")

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
        for col, flds in [(lc, [("Event Title", "title", 40),
                                 ("Date (YYYY-MM-DD)", "date", 20),
                                 ("Time", "time", 20)]),
                          (rc, [("Location", "location", 36),
                                ("Max Slots", "max_slots", 10),
                                ("Points Reward", "points", 10)])]:
            for lbl_txt, key, w in flds:
                tk.Label(col, text=lbl_txt, font=F["body"],
                         fg=C["muted"], bg=C["card"]).pack(anchor="w", pady=(10, 2))
                v = tk.StringVar()
                fields[key] = v
                entry(col, var=v, w=w).pack(ipady=8, anchor="w", fill="x")

        # category
        tk.Label(inner, text="Category", font=F["body"],
                 fg=C["muted"], bg=C["card"]).pack(anchor="w", pady=(14, 2))
        cat_v = tk.StringVar(value="Environmental")
        ttk.Combobox(inner, textvariable=cat_v,
                     values=list(CAT_COLOR.keys()),
                     state="readonly", font=F["body"], width=24).pack(ipady=6, anchor="w")

        # tags
        tk.Label(inner, text="Tags (comma-separated)", font=F["body"],
                 fg=C["muted"], bg=C["card"]).pack(anchor="w", pady=(12, 2))
        tags_v = tk.StringVar()
        entry(inner, var=tags_v, w=50).pack(ipady=8, anchor="w", fill="x")

        # description
        tk.Label(inner, text="Description", font=F["body"],
                 fg=C["muted"], bg=C["card"]).pack(anchor="w", pady=(12, 2))
        desc_box = scrolledtext.ScrolledText(inner, height=4, font=F["body"],
                                             bg=C["surface"], fg=C["text"],
                                             insertbackground=C["text"],
                                             relief="flat", highlightthickness=1,
                                             highlightbackground=C["border"])
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
            messagebox.showinfo("Created!", f"Event '{title}' published with {pts} points reward!")
            self._switch("my_events")

        btn(inner, "🚀  Publish Event", create,
            bg=C["green"], pady=12).pack(anchor="w", pady=(20, 0))

    def page_forms(self):
        p = self._scrollable_page()
        forms = jload(F_FORMS)
        events = jload(F_EVENTS)
        my_ids = {e["id"] for e in events.values() if e["org_id"] == self.user["id"]}
        my_forms = {k: v for k, v in forms.items() if v.get("event_id") in my_ids}
        self._page_header(p, "Form Builder", f"{len(my_forms)} forms",
                          "➕ Create Form", lambda: self._form_builder_popup())

        if not my_forms:
            tk.Label(p, text="No forms created yet. Create an event first, then build a form for it.",
                     font=F["body"], fg=C["muted"], bg=C["bg"]).pack(padx=32, pady=32)
            return

        for fid, frm in my_forms.items():
            evt = events.get(frm.get("event_id", ""), {})
            f = card_frame(p)
            f.pack(fill="x", padx=32, pady=8)

            # Header with form title and event name
            top = tk.Frame(f, bg=C["card"])
            top.pack(fill="x", padx=16, pady=(14, 2))
            tk.Label(top, text=f"📋 {frm['title']}", font=F["h2"],
                     fg=C["text"], bg=C["card"]).pack(side="left")
            tk.Label(top, text="", bg=C["card"]).pack(side="left", expand=True)
            tk.Label(top, text=f"📅 {evt.get('title','?')}", font=F["sm"],
                     fg=C["accent"], bg=C["card"]).pack(side="right")

            info_row = tk.Frame(f, bg=C["card"])
            info_row.pack(fill="x", padx=16, pady=(2, 8))
            tk.Label(info_row, text=f"❓ {len(frm['questions'])} questions", font=F["sm"],
                     fg=C["muted"], bg=C["card"]).pack(side="left")
            assigned = sum(1 for q in frm["questions"] if q.get("assigns_to_group"))
            if assigned:
                tk.Label(info_row, text=f"  •  🎯 {assigned} group assignments", font=F["sm"],
                         fg=C["green"], bg=C["card"]).pack(side="left")
            required = sum(1 for q in frm["questions"] if q.get("required"))
            if required:
                tk.Label(info_row, text=f"  •  ⚠️ {required} required fields", font=F["sm"],
                         fg=C["yellow"], bg=C["card"]).pack(side="left")

            # Questions preview
            for i, q in enumerate(frm["questions"], 1):
                qf = tk.Frame(f, bg=C["hover"])
                qf.pack(fill="x", padx=16, pady=2)
                tp = "🔘" if q["type"] == "choice" else "✏️"
                req = " *" if q.get("required") else ""
                grp = " [GROUP]" if q.get("assigns_to_group") else ""
                tk.Label(qf, text=f"  Q{i}: {tp} {q['text']}{req}{grp}",
                         font=F["sm"], fg=C["text"], bg=C["hover"], wraplength=600, justify="left").pack(side="left", pady=4, padx=2, anchor="w")
                if q["type"] == "choice":
                    opts = ", ".join(q.get("options", [])[:3])
                    more = f" +{len(q.get('options', []))-3} more" if len(
                        q.get('options', [])) > 3 else ""
                    tk.Label(qf, text=f"  → {opts}{more}",
                             font=F["sm"], fg=C["dim"], bg=C["hover"]).pack(side="left", padx=4)
            tk.Frame(f, bg=C["card"], height=4).pack()

    def _form_builder_popup(self):
        win = tk.Toplevel(self)
        win.title("Create Registration Form")
        win.geometry("720x640")
        win.configure(bg=C["bg"])

        events = jload(F_EVENTS)
        my_evts = {e["id"]: e["title"] for e in events.values()
                   if e["org_id"] == self.user["id"]}

        tk.Label(win, text="📋 Form Builder", font=F["h1"],
                 fg=C["text"], bg=C["bg"]).pack(pady=(20, 4), padx=24, anchor="w")
        sep(win).pack(fill="x", padx=24, pady=(0, 16))

        tk.Label(win, text="Form Title", font=F["body"],
                 fg=C["muted"], bg=C["bg"]).pack(anchor="w", padx=24, pady=(0, 2))
        title_v = tk.StringVar()
        entry(win, var=title_v, w=52).pack(ipady=8, padx=24, anchor="w")

        tk.Label(win, text="Link to Event", font=F["body"],
                 fg=C["muted"], bg=C["bg"]).pack(anchor="w", padx=24, pady=(12, 2))
        evt_v = tk.StringVar()
        evt_titles = list(my_evts.values())
        ttk.Combobox(win, textvariable=evt_v, values=evt_titles,
                     state="readonly", font=F["body"], width=50).pack(padx=24, anchor="w", ipady=6)

        tk.Label(win, text="Questions", font=F["h3"],
                 fg=C["text"], bg=C["bg"]).pack(anchor="w", padx=24, pady=(16, 4))

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
                tk.Label(qf,
                         text=f"  Q{i+1}: {tp} {q['text']}{req}{grp}",
                         font=F["sm"], fg=C["text"], bg=C["card"]).pack(
                             side="left", padx=8, pady=6)
                btn(qf, "✕", lambda idx=i: (questions.pop(idx), refresh()),
                    bg=C["red"], pady=2, padx=6, font=F["sm"]).pack(side="right", padx=8)

        def add_q_popup():
            qw = tk.Toplevel(win)
            qw.title("Add Question")
            qw.geometry("480x400")
            qw.configure(bg=C["bg"])

            tk.Label(qw, text="Question Text", font=F["body"],
                     fg=C["muted"], bg=C["bg"]).pack(anchor="w", padx=20, pady=(16, 2))
            qt_v = tk.StringVar()
            entry(qw, var=qt_v, w=48).pack(ipady=8, padx=20, anchor="w", fill="x")

            tk.Label(qw, text="Type", font=F["body"],
                     fg=C["muted"], bg=C["bg"]).pack(anchor="w", padx=20, pady=(10, 2))
            type_v = tk.StringVar(value="choice")
            ttk.Combobox(qw, textvariable=type_v,
                         values=["choice", "text"],
                         state="readonly", font=F["body"], width=16).pack(padx=20, anchor="w", ipady=6)

            tk.Label(qw,
                     text="Options (comma-separated — for 'choice' type)",
                     font=F["body"], fg=C["muted"], bg=C["bg"]).pack(
                         anchor="w", padx=20, pady=(10, 2))
            opts_v = tk.StringVar()
            entry(qw, var=opts_v, w=48).pack(ipady=8, padx=20, anchor="w", fill="x")

            grp_v = tk.BooleanVar()
            req_v = tk.BooleanVar(value=True)
            ck_row = tk.Frame(qw, bg=C["bg"])
            ck_row.pack(anchor="w", padx=20, pady=10)
            tk.Checkbutton(ck_row, text="Assigns student to a group chat",
                           variable=grp_v, bg=C["bg"], fg=C["text"],
                           activebackground=C["bg"],
                           activeforeground=C["accent"],
                           selectcolor=C["accent"],
                           highlightthickness=0,
                           font=F["body"]).pack(side="left")
            tk.Checkbutton(ck_row, text="Required",
                           variable=req_v, bg=C["bg"], fg=C["text"],
                           activebackground=C["bg"],
                           activeforeground=C["accent"],
                           selectcolor=C["accent"],
                           highlightthickness=0,
                           font=F["body"]).pack(side="left", padx=16)

            def save_q():
                text = qt_v.get().strip()
                if not text:
                    messagebox.showwarning("Missing", "Question text is required.")
                    return

                q_type = type_v.get()
                options = [o.strip() for o in opts_v.get().split(",") if o.strip()] if opts_v.get().strip() else []

                # Validate that choice type has options
                if q_type == "choice":
                    if not options:
                        messagebox.showwarning("Missing", "Choice questions must have at least one option.")
                        return

                questions.append({
                    "id": f"q{len(questions)+1}",
                    "text": text,
                    "type": q_type,
                    "options": options,
                    "assigns_to_group": grp_v.get(),
                    "required": req_v.get(),
                })
                refresh()
                qw.destroy()

            btn(qw, "✔ Add Question", save_q, bg=C["green"], pady=10).pack(padx=20, pady=16, anchor="w")

        btn(win, "➕ Add Question", add_q_popup,
            bg=C["accent"], pady=6, padx=12).pack(padx=24, anchor="w", pady=(0, 8))

        def save_form():
            sel_title = evt_v.get()
            sel_eid = next((eid for eid, et in my_evts.items() if et == sel_title), None)
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
                messagebox.showinfo("✓ Saved!", f"Form '{title_v.get().strip()}' created with {len(questions)} questions!")
                win.destroy()
                self._switch("forms")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save form: {e}")

        sep(win).pack(fill="x", padx=24, pady=10)
        btn(win, "💾  Save Form", save_form, bg=C["green"], pady=10).pack(padx=24, anchor="w")

    def page_chats(self):
        p = self._scrollable_page()
        groups = jload(F_GROUPS)
        events = jload(F_EVENTS)
        my_ids = {e["id"] for e in events.values() if e["org_id"] == self.user["id"]}
        my_grps = {k: v for k, v in groups.items() if v.get("event_id") in my_ids}
        self._page_header(p, "Group Chats", f"{len(my_grps)} active groups")

        if not my_grps:
            tk.Label(p, text="No groups yet. Create events and build forms to auto-generate groups.",
                     font=F["body"], fg=C["muted"], bg=C["bg"]).pack(padx=32, pady=16)

        msgs_all = jload(F_MESSAGES)
        for gid, grp in my_grps.items():
            evt = events.get(grp["event_id"], {})
            msgs = msgs_all.get(gid, [])
            last = (msgs[-1]["text"][:55] + "…") if msgs else "No messages yet"
            f = card_frame(p)
            f.pack(fill="x", padx=32, pady=5)
            row = tk.Frame(f, bg=C["card"])
            row.pack(fill="x", padx=16, pady=12)
            tk.Label(row, text="💬", font=("Segoe UI", 24),
                     bg=C["card"], fg=C["green"]).pack(side="left")
            c2 = tk.Frame(row, bg=C["card"])
            c2.pack(side="left", padx=10, fill="x", expand=True)
            tk.Label(c2, text=grp["name"], font=F["h3"],
                     fg=C["text"], bg=C["card"]).pack(anchor="w")
            tk.Label(c2,
                     text=f"{evt.get('title','')}  •  {len(grp['members'])} members",
                     font=F["sm"], fg=C["muted"], bg=C["card"]).pack(anchor="w")
            tk.Label(c2, text=last, font=F["sm"],
                     fg=C["dim"], bg=C["card"]).pack(anchor="w", pady=(2, 0))
            btn(row, "Open Chat →",
                lambda g=gid: ChatWindow(self, g, self.user),
                bg=C["green"], pady=6, padx=12).pack(side="right")

    def page_members(self):
        p = self._scrollable_page()
        groups = jload(F_GROUPS)
        events = jload(F_EVENTS)
        users = jload(F_USERS)
        my_evts = {e["id"]: e["title"] for e in events.values()
                   if e["org_id"] == self.user["id"]}
        self._page_header(p, "Members by Group",
                          "Students assigned to your event groups")

        for gid, grp in groups.items():
            if grp["event_id"] not in my_evts:
                continue
            tk.Label(p,
                     text=f"💬 {grp['name']}  —  {my_evts[grp['event_id']]}",
                     font=F["h3"], fg=C["text"], bg=C["bg"]).pack(
                         anchor="w", padx=32, pady=(16, 4))
            f = card_frame(p)
            f.pack(fill="x", padx=32, pady=(0, 8))
            if not grp["members"]:
                tk.Label(f, text="No members yet.",
                         font=F["sm"], fg=C["muted"], bg=C["card"]).pack(padx=16, pady=8, anchor="w")
                continue
            for uid in grp["members"]:
                u = users.get(uid, {})
                if not u:
                    continue
                row = tk.Frame(f, bg=C["card"])
                row.pack(fill="x", padx=16, pady=4)
                tk.Label(row, text=u.get("avatar", "👤"),
                         font=("Segoe UI", 18), bg=C["card"], fg=C["text"]).pack(side="left", padx=4)
                tk.Label(row, text=u.get("name", uid), font=F["bold"],
                         fg=C["text"], bg=C["card"]).pack(side="left", padx=6)
                tk.Label(row, text=f"{u.get('course','')} · {u.get('year','')}",
                         font=F["sm"], fg=C["muted"], bg=C["card"]).pack(side="left")
                role_col = C["muted"] if u["role"] == "org" else C["accent"]
                tk.Label(row, text=u["role"].upper(), font=F["sm"],
                         fg=role_col, bg=C["card"]).pack(side="right", padx=16)


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
        return [e for e in jload(F_EVENTS).values()
                if self.user["id"] in e["registered"]]

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
        return {k: v for k, v in jload(F_GROUPS).items()
                if self.user["id"] in v["members"]}

    def page_overview(self):
        p = self._scrollable_page()

        # ALWAYS refresh user data to get latest points from disk
        users = jload(F_USERS)
        self.user = users.get(self.user["id"], self.user)
        self.app.current_user = self.user

        joined = self._joined_events()
        pts = self.user.get("points", 0)
        grps = self._my_groups()

        level, lv_col = get_level(pts)
        self._page_header(p,
                          f"Welcome back, {self.user['name'].split()[0]}! 👋",
                          f"{self.user.get('course','')} · {self.user.get('year','')}")

        self._stat_row(p, [
            ("📅", len(joined), "Events Joined", C["accent"]),
            ("⭐", pts, "Total Points", C["yellow"]),
            ("💬", len(grps), "My Group Chats", C["green"]),
        ])

        # level banner
        lv_f = card_frame(p)
        lv_f.pack(fill="x", padx=32, pady=(0, 16))
        lv_r = tk.Frame(lv_f, bg=C["card"])
        lv_r.pack(fill="x", padx=16, pady=14)
        tk.Label(lv_r, text=f"🎖️  {level} Member",
                 font=F["h3"], fg=lv_col, bg=C["card"]).pack(side="left")
        next_pts = {"Bronze": 200, "Silver": 500, "Gold": 1000, "Platinum": 99999}
        rem = next_pts[level] - pts
        tk.Label(lv_r, text=f"  —  {rem} pts to next level  •  Keep participating!",
                 font=F["sm"], fg=C["muted"], bg=C["card"]).pack(side="left")

        # upcoming joined events
        tk.Label(p, text="My Upcoming Events", font=F["h2"],
                 fg=C["text"], bg=C["bg"]).pack(anchor="w", padx=32, pady=(8, 8))
        if not joined:
            tk.Label(p,
                     text="You haven't joined any events yet. Browse Discover Events →",
                     font=F["body"], fg=C["muted"], bg=C["bg"]).pack(padx=32, pady=8)
        for e in joined[:3]:
            self._event_card(p, e,
                             btn_text="💬 Open Chat",
                             btn_cmd=lambda ev=e: self._open_event_chat(ev),
                             btn_color=C["green"])

        # notifications preview
        notifs = jload(F_NOTIFS).get(self.user["id"], [])
        unread = [n for n in notifs if not n["read"]]
        if unread:
            tk.Label(p, text=f"🔔 Notifications ({len(unread)} unread)",
                     font=F["h2"], fg=C["text"], bg=C["bg"]).pack(
                         anchor="w", padx=32, pady=(16, 8))
            for n in unread[:3]:
                kind_col = {"success": C["green"], "info": C["accent"],
                            "warning": C["yellow"], "error": C["red"]}.get(n.get("kind","info"), C["muted"])
                nf = card_frame(p)
                nf.pack(fill="x", padx=32, pady=3)
                nr = tk.Frame(nf, bg=C["card"])
                nr.pack(fill="x", padx=16, pady=10)
                tk.Frame(nf, bg=kind_col, width=4).place(x=0, y=0, relheight=1)
                tk.Label(nr, text=n["text"], font=F["body"],
                         fg=C["text"], bg=C["card"],
                         wraplength=700, justify="left").pack(side="left", fill="x", expand=True)
                tk.Label(nr, text=n["time"], font=F["sm"],
                         fg=C["muted"], bg=C["card"]).pack(side="right")

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

        self._page_header(p, "Discover Events",
                          "Find and register for upcoming events")

        # filter bar
        fb = tk.Frame(p, bg=C["bg"])
        fb.pack(fill="x", padx=32, pady=(8, 4))
        tk.Label(fb, text="Category:", font=F["body"],
                 fg=C["muted"], bg=C["bg"]).pack(side="left")
        cat_v = tk.StringVar(value="All")
        cat_cb = ttk.Combobox(fb, textvariable=cat_v,
                              values=["All"] + list(CAT_COLOR.keys()),
                              state="readonly", font=F["body"], width=16)
        cat_cb.pack(side="left", padx=(6, 16), ipady=4)

        tk.Label(fb, text="Search:", font=F["body"],
                 fg=C["muted"], bg=C["bg"]).pack(side="left")
        search_v = tk.StringVar()
        entry(fb, var=search_v, w=24).pack(side="left", ipady=6, padx=(4, 0))

        list_frame = tk.Frame(p, bg=C["bg"])
        list_frame.pack(fill="x")

        def render(evts_to_show):
            for w in list_frame.winfo_children():
                w.destroy()
            if not evts_to_show:
                tk.Label(list_frame, text="No events match your filter.",
                         font=F["body"], fg=C["muted"], bg=C["bg"]).pack(padx=32, pady=16)
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
                self._event_card(list_frame, evt,
                                 btn_text=bt, btn_cmd=bc_fn, btn_color=bc)

        def render_all():
            query = search_v.get().strip().lower()
            cat = cat_v.get()
            all_evts = list(events.values())
            filtered = [e for e in all_evts
                        if (cat == "All" or e.get("category") == cat)
                        and (not query or query in e["title"].lower()
                             or query in e.get("description","").lower())]
            render(filtered)

        btn(fb, "Search", render_all, bg=C["accent"],
            pady=6, padx=12).pack(side="left", padx=8)
        render_all()

    def _register_event(self, evt, refresh_fn=None):
        forms = jload(F_FORMS)
        if evt.get("form_id") and evt["form_id"] in forms:
            FormFillWindow(self, evt, forms[evt["form_id"]], self.user,
                           on_done=lambda: (self._switch("discover") if refresh_fn is None else refresh_fn()))
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
                msgs[target_gid].append({
                    "sender_id": org_id,
                    "sender": org.get("name", "Organization"),
                    "text": f"👋 Welcome {self.user['name']}! You've joined the event. Looking forward to seeing you there!",
                    "time": now_str(),
                })

            jsave(F_EVENTS, events)
            jsave(F_GROUPS, groups)
            jsave(F_MESSAGES, msgs)

            push_notif(self.user["id"],
                       f"✅ You registered for '{evt['title']}'! 💬 Join the group chat.", "success")
            messagebox.showinfo("Registered! 🎉", f"You joined '{evt['title']}'!\n\nA group chat has been created for you.")
            self._switch("discover")

    def page_my_events(self):
        p = self._scrollable_page()
        joined = self._joined_events()
        self._page_header(p, "My Events", f"You have joined {len(joined)} event(s)")
        if not joined:
            tk.Label(p, text="No events joined yet.",
                     font=F["body"], fg=C["muted"], bg=C["bg"]).pack(padx=32, pady=16)
        for evt in joined:
            self._event_card(p, evt,
                             btn_text="💬 Open Chat",
                             btn_cmd=lambda e=evt: self._open_event_chat(e),
                             btn_color=C["green"])

    def page_chats(self):
        p = self._scrollable_page()
        grps = self._my_groups()
        events = jload(F_EVENTS)
        msgs_all = jload(F_MESSAGES)
        self._page_header(p, "My Group Chats", f"{len(grps)} group(s)")

        if not grps:
            tk.Label(p,
                     text="No group chats yet. Register for events to get assigned to groups!",
                     font=F["body"], fg=C["muted"], bg=C["bg"]).pack(padx=32, pady=16)
        for gid, g in grps.items():
            evt = events.get(g["event_id"], {})
            msgs = msgs_all.get(gid, [])
            last = (msgs[-1]["text"][:60] + "…") if msgs else "No messages yet"
            unread_cnt = 0  # could track per-user read pointer

            f = card_frame(p)
            f.pack(fill="x", padx=32, pady=5)
            row = tk.Frame(f, bg=C["card"])
            row.pack(fill="x", padx=16, pady=12)
            tk.Label(row, text="💬", font=("Segoe UI", 26),
                     bg=C["card"], fg=C["accent"]).pack(side="left")
            c2 = tk.Frame(row, bg=C["card"])
            c2.pack(side="left", padx=10, fill="x", expand=True)
            tk.Label(c2, text=g["name"], font=F["h3"],
                     fg=C["text"], bg=C["card"]).pack(anchor="w")
            tk.Label(c2,
                     text=f"📅 {evt.get('title','?')}  •  👥 {len(g['members'])} members",
                     font=F["sm"], fg=C["muted"], bg=C["card"]).pack(anchor="w")
            tk.Label(c2, text=last, font=F["sm"],
                     fg=C["dim"], bg=C["card"]).pack(anchor="w", pady=(3, 0))
            btn(row, "Open →",
                lambda g_id=gid: ChatWindow(self, g_id, self.user),
                bg=C["accent"], pady=6, padx=12).pack(side="right")

    def page_notifs(self):
        p = self._scrollable_page()
        notifs = jload(F_NOTIFS)
        my_notifs = notifs.get(self.user["id"], [])
        unread_cnt = sum(1 for n in my_notifs if not n["read"])
        self._page_header(p, "Notifications",
                          f"{unread_cnt} unread  •  {len(my_notifs)} total")

        def mark_all_read():
            for n in my_notifs:
                n["read"] = True
            notifs[self.user["id"]] = my_notifs
            jsave(F_NOTIFS, notifs)
            self._switch("notifs")

        btn(p, "✔ Mark all as read", mark_all_read,
            bg=C["dim"], pady=6, padx=12).pack(anchor="e", padx=32, pady=(8, 4))

        if not my_notifs:
            tk.Label(p, text="No notifications yet.",
                     font=F["body"], fg=C["muted"], bg=C["bg"]).pack(padx=32, pady=16)

        kind_map = {"success": C["green"], "info": C["accent"],
                    "warning": C["yellow"], "error": C["red"]}
        for n in my_notifs:
            col = kind_map.get(n.get("kind", "info"), C["muted"])
            f = card_frame(p)
            f.pack(fill="x", padx=32, pady=3)
            # color left bar
            tk.Frame(f, bg=col, width=5).pack(side="left", fill="y")
            body = tk.Frame(f, bg=C["card"] if not n["read"] else C["surface"])
            body.pack(side="left", fill="x", expand=True, padx=14, pady=10)
            tk.Label(body, text=n["text"], font=F["body"],
                     fg=C["text"] if not n["read"] else C["muted"],
                     bg=body.cget("bg"),
                     wraplength=750, justify="left").pack(anchor="w")
            tk.Label(body, text=n["time"], font=F["sm"],
                     fg=C["dim"], bg=body.cget("bg")).pack(anchor="w", pady=(4, 0))
            if not n["read"]:
                tk.Frame(f, bg=col, width=10, height=10).place(relx=1, rely=0,
                                                                 x=-16, y=8)

    def page_rewards(self):
        p = self._scrollable_page()

        # Refresh user data to get latest points
        users = jload(F_USERS)
        self.user = users.get(self.user["id"], self.user)
        self.app.current_user = self.user

        pts = self.user.get("points", 0)
        joined = self._joined_events()
        level, lv_col = get_level(pts)

        self._page_header(p, "Rewards & Points", "Your engagement journey")

        # big points display
        pf = card_frame(p)
        pf.pack(fill="x", padx=32, pady=16)
        pi = tk.Frame(pf, bg=C["card"])
        pi.pack(fill="x", padx=24, pady=20)
        tk.Label(pi, text="⭐ Total Points", font=F["h2"],
                 fg=C["yellow"], bg=C["card"]).pack(anchor="w")
        tk.Label(pi, text=str(pts), font=("Segoe UI", 52, "bold"),
                 fg=C["yellow"], bg=C["card"]).pack(anchor="w")
        tk.Label(pi, text=f"Current Level: {level}",
                 font=F["h3"], fg=lv_col, bg=C["card"]).pack(anchor="w", pady=(4, 0))

        # progress bar to next level
        thresholds = {"Bronze": 0, "Silver": 200, "Gold": 500, "Platinum": 1000}
        next_map = {"Bronze": 200, "Silver": 500, "Gold": 1000, "Platinum": 9999}
        lo = thresholds[level]
        hi = next_map[level]
        pct = min(100, int(100 * (pts - lo) / (hi - lo))) if hi > lo else 100
        pb_row = tk.Frame(pi, bg=C["card"])
        pb_row.pack(anchor="w", pady=(10, 0), fill="x")
        tk.Label(pb_row, text=f"Progress to next level: {pct}%",
                 font=F["sm"], fg=C["muted"], bg=C["card"]).pack(anchor="w", pady=(0, 4))
        pb_bg = tk.Frame(pb_row, bg=C["border"], height=12, width=500)
        pb_bg.pack(anchor="w")
        pb_bg.pack_propagate(False)
        tk.Frame(pb_bg, bg=lv_col, width=int(500 * pct / 100), height=12).place(x=0, y=0)

        # level tiers
        tk.Label(p, text="Level Tiers", font=F["h2"],
                 fg=C["text"], bg=C["bg"]).pack(anchor="w", padx=32, pady=(16, 8))
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
            tk.Label(tf, text=name, font=F["h3"],
                     fg=col, bg=C["card"]).pack(padx=14, pady=(14, 2), anchor="w")
            tk.Label(tf, text=rng, font=F["sm"],
                     fg=C["muted"], bg=C["card"]).pack(padx=14, anchor="w")
            here = lo2 <= pts < hi2 or (level == "Platinum" and name == "💎 Platinum")
            if here:
                tk.Label(tf, text="← You're here", font=("Segoe UI", 9, "bold"),
                         fg=col, bg=C["card"]).pack(padx=14, pady=(2, 14), anchor="w")
            else:
                tk.Frame(tf, bg=C["card"], height=14).pack()

        # contribution log
        tk.Label(p, text="Event Contribution Log",
                 font=F["h2"], fg=C["text"], bg=C["bg"]).pack(
                     anchor="w", padx=32, pady=(20, 8))
        if not joined:
            tk.Label(p, text="Join events to earn points!",
                     font=F["body"], fg=C["muted"], bg=C["bg"]).pack(padx=32)
        for e in joined:
            f = card_frame(p)
            f.pack(fill="x", padx=32, pady=4)
            row = tk.Frame(f, bg=C["card"])
            row.pack(fill="x", padx=16, pady=10)
            cat_col = CAT_COLOR.get(e.get("category",""), C["muted"])
            tk.Label(row, text=f"● {e.get('category','')}",
                     font=F["sm"], fg=cat_col, bg=C["card"]).pack(side="left")
            tk.Label(row, text=f"  {e['title']}", font=F["bold"],
                     fg=C["text"], bg=C["card"]).pack(side="left")
            tk.Label(row, text=f"📅 {e['date']}",
                     font=F["sm"], fg=C["muted"], bg=C["card"]).pack(side="left", padx=16)
            tk.Label(row, text=f"+{e.get('points',0)} pts",
                     font=F["h3"], fg=C["yellow"], bg=C["card"]).pack(side="right", padx=16)

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
        tk.Label(left_p, text=u.get("avatar", "👤"),
                 font=("Segoe UI", 64), bg=C["card"], fg=C["text"]).pack()
        level, lv_col = get_level(u.get("points", 0))
        tk.Label(left_p, text=f"🎖️ {level}",
                 font=F["h3"], fg=lv_col, bg=C["card"]).pack(pady=(4, 0))

        right_p = tk.Frame(pi, bg=C["card"])
        right_p.pack(side="left", padx=32, fill="x", expand=True)
        tk.Label(right_p, text=u["name"], font=("Segoe UI", 22, "bold"),
                 fg=C["text"], bg=C["card"]).pack(anchor="w")
        tk.Label(right_p, text=f"@{u['id']}  •  {u['email']}",
                 font=F["body"], fg=C["muted"], bg=C["card"]).pack(anchor="w", pady=(2, 0))
        tk.Label(right_p, text=f"{u.get('course','')} · {u.get('year','')}",
                 font=F["body"], fg=C["accent"], bg=C["card"]).pack(anchor="w", pady=(4, 0))
        tk.Label(right_p, text=u.get("bio", "No bio yet."),
                 font=F["body"], fg=C["muted"], bg=C["card"],
                 wraplength=500).pack(anchor="w", pady=(6, 0))
        tk.Label(right_p, text=f"⭐ {u.get('points',0)} pts  •  Joined: {u.get('joined','')}",
                 font=F["body"], fg=C["yellow"], bg=C["card"]).pack(anchor="w", pady=(8, 0))

        # edit form
        tk.Label(p, text="Edit Profile", font=F["h2"],
                 fg=C["text"], bg=C["bg"]).pack(anchor="w", padx=32, pady=(16, 8))
        ef = card_frame(p)
        ef.pack(fill="x", padx=32, pady=(0, 32))
        ei = tk.Frame(ef, bg=C["card"])
        ei.pack(fill="x", padx=24, pady=20)

        ev = {}
        for lbl_txt, key in [("Display Name", "name"), ("Email", "email"), ("Course", "course")]:
            tk.Label(ei, text=lbl_txt, font=F["body"],
                     fg=C["muted"], bg=C["card"]).pack(anchor="w", pady=(10, 2))
            v = tk.StringVar(value=u.get(key,""))
            ev[key] = v
            entry(ei, var=v, w=40).pack(ipady=8, anchor="w", fill="x")

        tk.Label(ei, text="Year Level", font=F["body"],
                 fg=C["muted"], bg=C["card"]).pack(anchor="w", pady=(10, 2))
        yr_v = tk.StringVar(value=u.get("year","1st Year"))
        ttk.Combobox(ei, textvariable=yr_v,
                     values=["1st Year","2nd Year","3rd Year","4th Year","5th Year"],
                     state="readonly", font=F["body"], width=20).pack(ipady=6, anchor="w")

        tk.Label(ei, text="Bio", font=F["body"],
                 fg=C["muted"], bg=C["card"]).pack(anchor="w", pady=(10, 2))
        bio_box = scrolledtext.ScrolledText(ei, height=3, width=50,
                                            font=F["body"], bg=C["surface"],
                                            fg=C["text"], insertbackground=C["text"],
                                            relief="flat", highlightthickness=1,
                                            highlightbackground=C["border"])
        bio_box.insert("1.0", u.get("bio",""))
        bio_box.pack(fill="x")

        def save_profile():
            users2 = jload(F_USERS)
            uid = self.user["id"]
            users2[uid]["name"] = ev["name"].get().strip() or users2[uid]["name"]
            users2[uid]["email"] = ev["email"].get().strip() or users2[uid]["email"]
            users2[uid]["course"] = ev["course"].get().strip()
            users2[uid]["year"] = yr_v.get()
            users2[uid]["bio"] = bio_box.get("1.0","end").strip()
            jsave(F_USERS, users2)
            self.user = users2[uid]
            self.app.current_user = users2[uid]
            messagebox.showinfo("Saved", "Profile updated!")
            self._switch("profile")

        btn(ei, "💾  Save Changes", save_profile,
            bg=C["green"], pady=12).pack(anchor="w", pady=(16, 0))
