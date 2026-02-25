"""Login and Registration dialog for the E-commerce Mini-system."""

import tkinter as tk
from tkinter import messagebox

from . import theme as T
from .widgets import StyledButton
from ..models.customer import Customer


class LoginDialog(tk.Toplevel):
    """Modal login / register dialog."""

    def __init__(self, master, db):
        super().__init__(master)
        self.db = db
        self.result: tk.Optional[Customer] = None

        self.title("E-Commerce – Sign In")
        self.resizable(False, False)
        self.configure(bg=T.BG_LIGHT)
        self.grab_set()

        self._build()
        self._center()

    # ------------------------------------------------------------------

    def _center(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f"+{x}+{y}")

    def _build(self):
        # ── Header ──
        header = tk.Frame(self, bg=T.PRIMARY, pady=18)
        header.pack(fill=tk.X)
        tk.Label(header, text="🛒  E-Commerce Shop",
                 font=(T.FONT_FAMILY, 20, "bold"),
                 fg=T.TEXT_LIGHT, bg=T.PRIMARY).pack()
        tk.Label(header, text="Sign in to continue",
                 font=T.FONT_SMALL,
                 fg=T.TEXT_MUTED, bg=T.PRIMARY).pack(pady=(2, 0))

        # ── Notebook for Login / Register ──
        self._nb = tk.Frame(self, bg=T.BG_LIGHT)
        self._nb.pack(fill=tk.BOTH, padx=30, pady=20)

        # Tab buttons
        tab_row = tk.Frame(self._nb, bg=T.BG_LIGHT)
        tab_row.pack(fill=tk.X)

        self._login_frame    = tk.Frame(self._nb, bg=T.BG_LIGHT)
        self._register_frame = tk.Frame(self._nb, bg=T.BG_LIGHT)

        self._btn_login = StyledButton(tab_row, "Login",    lambda: self._show("login"),    variant="dark")
        self._btn_reg   = StyledButton(tab_row, "Register", lambda: self._show("register"), variant="secondary")
        self._btn_login.pack(side=tk.LEFT, ipady=4, ipadx=8)
        self._btn_reg.pack(  side=tk.LEFT, ipady=4, ipadx=8, padx=(4, 0))

        self._build_login()
        self._build_register()
        self._show("login")

    # ------------------------------------------------------------------
    # Login panel
    # ------------------------------------------------------------------

    def _build_login(self):
        f = self._login_frame
        tk.Label(f, text="Username", bg=T.BG_LIGHT, font=T.FONT_BODY).grid(
            row=0, column=0, sticky=tk.W, pady=(12, 2))
        self._login_user = tk.Entry(f, font=T.FONT_BODY, relief=tk.SOLID, bd=1, width=28)
        self._login_user.grid(row=1, column=0, sticky=tk.EW)

        tk.Label(f, text="Password", bg=T.BG_LIGHT, font=T.FONT_BODY).grid(
            row=2, column=0, sticky=tk.W, pady=(10, 2))
        self._login_pass = tk.Entry(f, show="•", font=T.FONT_BODY, relief=tk.SOLID, bd=1, width=28)
        self._login_pass.grid(row=3, column=0, sticky=tk.EW)
        self._login_pass.bind("<Return>", lambda _: self._do_login())

        StyledButton(f, "Sign In", self._do_login, variant="primary").grid(
            row=4, column=0, sticky=tk.EW, pady=(16, 4), ipady=4)

    # ------------------------------------------------------------------
    # Register panel
    # ------------------------------------------------------------------

    def _build_register(self):
        f = self._register_frame
        fields = [
            ("Username *",  "_reg_user"),
            ("Full Name *",  "_reg_name"),
            ("Email *",      "_reg_email"),
            ("Phone",        "_reg_phone"),
            ("Address",      "_reg_addr"),
            ("Password *",   "_reg_pass"),
            ("Confirm Pwd *","_reg_pass2"),
        ]
        for i, (label, attr) in enumerate(fields):
            tk.Label(f, text=label, bg=T.BG_LIGHT, font=T.FONT_BODY).grid(
                row=i * 2, column=0, sticky=tk.W, pady=(8, 2))
            entry = tk.Entry(f, font=T.FONT_BODY, relief=tk.SOLID, bd=1, width=28,
                             show="•" if "pass" in attr.lower() else "")
            entry.grid(row=i * 2 + 1, column=0, sticky=tk.EW)
            setattr(self, attr, entry)

        StyledButton(f, "Create Account", self._do_register, variant="success").grid(
            row=len(fields) * 2, column=0, sticky=tk.EW, pady=(14, 4), ipady=4)

    # ------------------------------------------------------------------
    # Tab switching
    # ------------------------------------------------------------------

    def _show(self, tab: str):
        self._login_frame.pack_forget()
        self._register_frame.pack_forget()
        if tab == "login":
            self._login_frame.pack(fill=tk.BOTH, expand=True)
            self._btn_login.config(bg=T.PRIMARY)
            self._btn_reg.config(bg=T.BG_LIGHT, fg=T.TEXT_DARK)
        else:
            self._register_frame.pack(fill=tk.BOTH, expand=True)
            self._btn_reg.config(bg=T.PRIMARY, fg=T.TEXT_LIGHT)
            self._btn_login.config(bg=T.BG_LIGHT, fg=T.TEXT_DARK)

    # ------------------------------------------------------------------
    # Actions
    # ------------------------------------------------------------------

    def _do_login(self):
        username = self._login_user.get().strip()
        password = self._login_pass.get()
        if not username or not password:
            messagebox.showwarning("Login", "Please enter username and password.", parent=self)
            return
        customer = self.db.get_customer_by_username(username)
        if customer and customer.check_password(password):
            self.result = customer
            self.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.", parent=self)

    def _do_register(self):
        username = self._reg_user.get().strip()
        full_name = self._reg_name.get().strip()
        email = self._reg_email.get().strip()
        phone = self._reg_phone.get().strip()
        address = self._reg_addr.get().strip()
        password = self._reg_pass.get()
        confirm = self._reg_pass2.get()

        if not username or not full_name or not email or not password:
            messagebox.showwarning("Register", "Please fill in all required fields (*)", parent=self)
            return
        if password != confirm:
            messagebox.showerror("Register", "Passwords do not match.", parent=self)
            return
        if self.db.get_customer_by_username(username):
            messagebox.showerror("Register", f"Username '{username}' already taken.", parent=self)
            return

        customer = Customer(username=username, email=email, full_name=full_name,
                            phone=phone, address=address)
        try:
            customer.set_password(password)
        except ValueError as e:
            messagebox.showerror("Register", str(e), parent=self)
            return

        customer = self.db.create_customer(customer)
        messagebox.showinfo("Success", "Account created! You can now sign in.", parent=self)
        self._show("login")
        self._login_user.delete(0, tk.END)
        self._login_user.insert(0, username)
