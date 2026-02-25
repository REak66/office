"""Main application window for the E-commerce Mini-system."""

import tkinter as tk
from tkinter import messagebox

from . import theme as T
from .admin_view import AdminView
from .cart_view import CartView
from .login_dialog import LoginDialog
from .orders_view import OrdersView
from .products_view import ProductsView
from .profile_view import ProfileView
from .widgets import StatusBar, StyledButton
from ..database.db_manager import DatabaseManager
from ..models.cart import Cart


class EcommerceApp(tk.Tk):
    """Root window – manages navigation, session, and view switching."""

    def __init__(self, db_path: str = "ecommerce.db"):
        super().__init__()
        self.db = DatabaseManager(db_path)
        self.current_customer = None
        self.cart = Cart()

        self.title("🛒 E-Commerce Mini-System")
        self.geometry(f"{T.WINDOW_W}x{T.WINDOW_H}")
        self.minsize(800, 550)
        self.configure(bg=T.BG_LIGHT)
        self._center()

        self._build_layout()
        self._show_login()

    # ------------------------------------------------------------------

    def _center(self):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - T.WINDOW_W) // 2
        y = (sh - T.WINDOW_H) // 2
        self.geometry(f"{T.WINDOW_W}x{T.WINDOW_H}+{x}+{y}")

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _build_layout(self):
        # Top nav bar
        self._navbar = tk.Frame(self, bg=T.PRIMARY, height=T.NAV_H)
        self._navbar.pack(fill=tk.X, side=tk.TOP)
        self._navbar.pack_propagate(False)

        tk.Label(
            self._navbar,
            text="🛒  E-Commerce Mini-System",
            font=(T.FONT_FAMILY, 14, "bold"),
            bg=T.PRIMARY,
            fg=T.TEXT_LIGHT,
        ).pack(side=tk.LEFT, padx=T.PAD)

        self._nav_buttons_frame = tk.Frame(self._navbar, bg=T.PRIMARY)
        self._nav_buttons_frame.pack(side=tk.LEFT, padx=(T.PAD, 0))

        self._right_nav = tk.Frame(self._navbar, bg=T.PRIMARY)
        self._right_nav.pack(side=tk.RIGHT, padx=T.PAD)

        # Content area
        self._content = tk.Frame(self, bg=T.BG_LIGHT)
        self._content.pack(fill=tk.BOTH, expand=True)

        # Status bar
        self._status_bar = StatusBar(self)
        self._status_bar.pack(fill=tk.X, side=tk.BOTTOM)

    # ------------------------------------------------------------------
    # Auth flow
    # ------------------------------------------------------------------

    def _show_login(self):
        dialog = LoginDialog(self, self.db)
        self.wait_window(dialog)
        if dialog.result:
            self.current_customer = dialog.result
            self.cart = Cart(customer_id=self.current_customer.id)
            self._build_nav()
            self._show_products()
            self._status_bar.set(f"Logged in as: {self.current_customer.full_name}")
        else:
            # Closed without logging in → quit
            self.destroy()

    def _logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to log out?", parent=self):
            self.current_customer = None
            self.cart = Cart()
            self._clear_nav()
            self._clear_content()
            self._show_login()

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def _clear_nav(self):
        for w in self._nav_buttons_frame.winfo_children():
            w.destroy()
        for w in self._right_nav.winfo_children():
            w.destroy()

    def _build_nav(self):
        self._clear_nav()

        nav_items = [
            ("🛍  Products", self._show_products),
            ("🛒  Cart",     self._show_cart),
            ("📦  My Orders", self._show_orders),
            ("👤  Profile",  self._show_profile),
        ]
        if self.current_customer and self.current_customer.is_admin:
            nav_items.append(("⚙️  Admin", self._show_admin))

        self._nav_btns = {}
        for label, cmd in nav_items:
            btn = tk.Button(
                self._nav_buttons_frame,
                text=label,
                command=cmd,
                bg=T.PRIMARY,
                fg=T.TEXT_LIGHT,
                font=T.FONT_BODY,
                relief=tk.FLAT,
                cursor="hand2",
                padx=10,
                activebackground=T.SECONDARY,
                activeforeground=T.TEXT_LIGHT,
            )
            btn.pack(side=tk.LEFT, ipady=8)
            self._nav_btns[label] = btn

        # Cart badge
        self._cart_badge = tk.Label(
            self._right_nav,
            text="",
            bg=T.PRIMARY,
            fg=T.WARNING,
            font=T.FONT_SMALL,
        )
        self._cart_badge.pack(side=tk.LEFT, padx=(0, T.PAD))
        self._update_cart_badge()

        # Logout button
        StyledButton(
            self._right_nav,
            "🚪 Logout",
            self._logout,
            variant="danger",
        ).pack(side=tk.LEFT)

    def _set_active_nav(self, active_label: str):
        for label, btn in self._nav_btns.items():
            btn.config(bg=T.SECONDARY if label == active_label else T.PRIMARY)

    def _update_cart_badge(self):
        count = self.cart.item_count
        self._cart_badge.config(
            text=f"({count} item{'s' if count != 1 else ''})" if count > 0 else ""
        )

    # ------------------------------------------------------------------
    # View switching
    # ------------------------------------------------------------------

    def _clear_content(self):
        for w in self._content.winfo_children():
            w.destroy()

    def _show_products(self):
        self._clear_content()
        self._set_active_nav("🛍  Products")
        ProductsView(
            self._content,
            db=self.db,
            cart=self.cart,
            on_cart_changed=self._on_cart_changed,
        ).pack(fill=tk.BOTH, expand=True)

    def _show_cart(self):
        self._clear_content()
        self._set_active_nav("🛒  Cart")
        CartView(
            self._content,
            db=self.db,
            cart=self.cart,
            customer=self.current_customer,
            on_order_placed=self._show_orders,
            on_cart_changed=self._on_cart_changed,
        ).pack(fill=tk.BOTH, expand=True)

    def _show_orders(self):
        self._clear_content()
        self._set_active_nav("📦  My Orders")
        OrdersView(
            self._content,
            db=self.db,
            customer=self.current_customer,
        ).pack(fill=tk.BOTH, expand=True)

    def _show_profile(self):
        self._clear_content()
        self._set_active_nav("👤  Profile")
        ProfileView(
            self._content,
            db=self.db,
            customer=self.current_customer,
        ).pack(fill=tk.BOTH, expand=True)

    def _show_admin(self):
        self._clear_content()
        self._set_active_nav("⚙️  Admin")
        AdminView(
            self._content,
            db=self.db,
        ).pack(fill=tk.BOTH, expand=True)

    # ------------------------------------------------------------------

    def _on_cart_changed(self):
        self._update_cart_badge()
        self._status_bar.set(
            f"Cart updated – {self.cart.item_count} item(s) | Total: {self.cart.formatted_total()}"
        )
