"""
UI Widgets module - reusable Tkinter widget components.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from core.theme import COLORS as C, FONTS as F
from core.utils import get_bg


def lbl(parent, text, font=None, fg=None, **kw):
    """Create a label with theme styling."""
    return tk.Label(
        parent,
        text=text,
        font=font or F["body"],
        fg=fg or C["text"],
        bg=get_bg(parent),
        **kw
    )


def sep(parent, color=None, h=1):
    """Create a separator line."""
    return tk.Frame(parent, bg=color or C["border"], height=h)


def card_frame(parent, **kw):
    """Create a card frame with theme styling."""
    return tk.Frame(parent, bg=C["card"], **kw)


def surface_frame(parent, **kw):
    """Create a surface frame with theme styling."""
    return tk.Frame(parent, bg=C["surface"], **kw)


def btn(parent, text, cmd=None, bg=None, fg=None, padx=20, pady=8, font=None, **kw):
    """Create a button with theme styling."""
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
        **kw
    )
    if not cmd:
        b.config(cursor="default")
    return b


def entry(parent, var=None, w=30, show="", **kw):
    """Create an entry field with theme styling."""
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
        **kw
    )
    return e


def badge(parent, text, color):
    """Create a badge label."""
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
    """Create a scrollable frame. Returns (outer_frame, inner_frame)."""
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
