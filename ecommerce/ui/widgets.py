"""Reusable custom tkinter widgets for the E-commerce Mini-system."""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from . import theme as T


class StyledButton(tk.Button):
    """A button that follows the app colour theme."""

    def __init__(
        self,
        master,
        text: str,
        command: Optional[Callable] = None,
        variant: str = "primary",  # primary | success | danger | secondary
        **kwargs,
    ):
        colour_map = {
            "primary":   (T.SECONDARY,  T.TEXT_LIGHT),
            "success":   (T.SUCCESS,    T.TEXT_LIGHT),
            "danger":    (T.DANGER,     T.TEXT_LIGHT),
            "secondary": (T.BG_LIGHT,   T.TEXT_DARK),
            "dark":      (T.PRIMARY,    T.TEXT_LIGHT),
        }
        bg, fg = colour_map.get(variant, colour_map["primary"])
        super().__init__(
            master,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            font=T.FONT_BODY,
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            pady=4,
            activebackground=bg,
            activeforeground=fg,
            **kwargs,
        )


class Card(tk.Frame):
    """A white rounded-border card frame."""

    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            bg=T.BG_CARD,
            relief=tk.FLAT,
            bd=1,
            highlightthickness=1,
            highlightbackground=T.BORDER,
            **kwargs,
        )


class SectionLabel(tk.Label):
    """A section heading label."""

    def __init__(self, master, text: str, **kwargs):
        super().__init__(
            master,
            text=text,
            font=T.FONT_HEADING,
            fg=T.TEXT_DARK,
            bg=T.BG_LIGHT,
            **kwargs,
        )


class StatusBar(tk.Frame):
    """A bottom status bar that shows a simple message."""

    def __init__(self, master, **kwargs):
        super().__init__(master, bg=T.PRIMARY, height=T.STATUS_H, **kwargs)
        self._var = tk.StringVar(value="Ready")
        self._label = tk.Label(
            self,
            textvariable=self._var,
            bg=T.PRIMARY,
            fg=T.TEXT_LIGHT,
            font=T.FONT_CAPTION,
            anchor=tk.W,
        )
        self._label.pack(side=tk.LEFT, padx=T.PAD)

    def set(self, message: str) -> None:
        self._var.set(message)


class SearchBar(tk.Frame):
    """An inline search entry + button."""

    def __init__(self, master, placeholder: str, on_search: Callable, **kwargs):
        super().__init__(master, bg=T.BG_LIGHT, **kwargs)
        self._var = tk.StringVar()
        entry = tk.Entry(
            self,
            textvariable=self._var,
            font=T.FONT_BODY,
            relief=tk.SOLID,
            bd=1,
            width=30,
        )
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>",  lambda _: entry.delete(0, tk.END) if entry.get() == placeholder else None)
        entry.bind("<FocusOut>", lambda _: entry.insert(0, placeholder) if not entry.get() else None)
        entry.bind("<Return>", lambda _: on_search(self._var.get()))
        entry.pack(side=tk.LEFT, padx=(0, T.PAD_SM))
        StyledButton(self, "🔍 Search", lambda: on_search(self._var.get())).pack(side=tk.LEFT)
        StyledButton(self, "✕ Clear", lambda: (self._var.set(""), on_search("")), variant="secondary").pack(side=tk.LEFT, padx=(T.PAD_SM, 0))


class DataTable(tk.Frame):
    """A scrollable Treeview-based data table."""

    def __init__(self, master, columns: list, **kwargs):
        super().__init__(master, bg=T.BG_LIGHT, **kwargs)
        style = ttk.Style()
        style.configure("Custom.Treeview",
                         rowheight=28,
                         font=T.FONT_BODY,
                         background=T.BG_CARD,
                         fieldbackground=T.BG_CARD,
                         foreground=T.TEXT_DARK)
        style.configure("Custom.Treeview.Heading",
                         font=T.FONT_SUBHEAD,
                         background=T.PRIMARY,
                         foreground=T.TEXT_LIGHT)
        style.map("Custom.Treeview", background=[("selected", T.SECONDARY)])

        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            style="Custom.Treeview",
            selectmode="browse",
        )
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, minwidth=80)

        vsb = ttk.Scrollbar(self, orient=tk.VERTICAL,   command=self.tree.yview)
        hsb = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0,  column=1, sticky="ns")
        hsb.grid(row=1,  column=0, sticky="ew")
        self.rowconfigure(0,    weight=1)
        self.columnconfigure(0, weight=1)

    def clear(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    def insert(self, values: tuple):
        self.tree.insert("", tk.END, values=values)

    def selected_values(self) -> Optional[tuple]:
        sel = self.tree.selection()
        if sel:
            return self.tree.item(sel[0])["values"]
        return None
