"""Customer profile view."""

import tkinter as tk
from tkinter import messagebox

from . import theme as T
from .widgets import Card, SectionLabel, StyledButton


class ProfileView(tk.Frame):
    """Allows the logged-in customer to view and edit their profile."""

    def __init__(self, master, db, customer, **kwargs):
        super().__init__(master, bg=T.BG_LIGHT, **kwargs)
        self.db = db
        self.customer = customer
        self._build()

    def _build(self):
        top = tk.Frame(self, bg=T.BG_LIGHT, pady=T.PAD)
        top.pack(fill=tk.X, padx=T.PAD)
        SectionLabel(top, "👤  My Profile").pack(side=tk.LEFT)

        card = Card(self, padx=20, pady=20)
        card.pack(padx=T.PAD, pady=T.PAD, anchor=tk.NW)

        fields = [
            ("Username",  self.customer.username, False),
            ("Full Name", self.customer.full_name, True),
            ("Email",     self.customer.email,     True),
            ("Phone",     self.customer.phone,     True),
            ("Address",   self.customer.address,   True),
        ]

        self._entries = {}
        for i, (label, value, editable) in enumerate(fields):
            tk.Label(card, text=label + ":", bg=T.BG_CARD, font=T.FONT_BODY,
                     width=12, anchor=tk.W).grid(row=i, column=0, pady=5, sticky=tk.W)
            var = tk.StringVar(value=value or "")
            entry = tk.Entry(card, textvariable=var, font=T.FONT_BODY,
                             width=32, relief=tk.SOLID, bd=1,
                             state=tk.NORMAL if editable else "disabled")
            entry.grid(row=i, column=1, pady=5, sticky=tk.EW)
            if editable:
                self._entries[label] = var

        btn_row = tk.Frame(card, bg=T.BG_CARD)
        btn_row.grid(row=len(fields), column=0, columnspan=2, pady=(14, 0), sticky=tk.W)
        StyledButton(btn_row, "💾 Save Changes", self._save, variant="success").pack(side=tk.LEFT)

    def _save(self):
        self.customer.full_name = self._entries["Full Name"].get().strip()
        self.customer.email     = self._entries["Email"].get().strip()
        self.customer.phone     = self._entries["Phone"].get().strip()
        self.customer.address   = self._entries["Address"].get().strip()

        if not self.customer.full_name or not self.customer.email:
            messagebox.showwarning("Profile", "Full name and email are required.", parent=self)
            return
        self.db.update_customer(self.customer)
        messagebox.showinfo("Profile", "Profile updated successfully.", parent=self)
