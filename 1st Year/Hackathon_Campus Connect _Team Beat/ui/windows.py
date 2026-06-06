"""
UI Windows module - popup windows for forms and chats.
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox
import uuid
from core.database import (
    jload,
    jsave,
    F_FORMS,
    F_EVENTS,
    F_GROUPS,
    F_MESSAGES,
    F_RESPONSES,
    F_USERS,
    now_str,
    today,
    push_notif,
)
from core.theme import COLORS as C, FONTS as F
from ui.widgets import btn, entry, sep, card_frame, scrollable_frame


class FormFillWindow(tk.Toplevel):
    """Popup window for students to fill event registration forms."""

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


class ChatWindow(tk.Toplevel):
    """Popup window for group chat messaging."""

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
