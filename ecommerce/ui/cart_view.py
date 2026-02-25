"""Shopping cart view for the E-commerce Mini-system."""

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from . import theme as T
from .widgets import Card, SectionLabel, StyledButton
from ..models.order import Order, OrderItem


class CartView(tk.Frame):
    """Displays cart items, allows removal/quantity changes, and checkout."""

    def __init__(self, master, db, cart, customer, on_order_placed, on_cart_changed, **kwargs):
        super().__init__(master, bg=T.BG_LIGHT, **kwargs)
        self.db = db
        self.cart = cart
        self.customer = customer
        self.on_order_placed = on_order_placed
        self.on_cart_changed = on_cart_changed
        self._build()
        self.refresh()

    # ------------------------------------------------------------------

    def _build(self):
        top = tk.Frame(self, bg=T.BG_LIGHT, pady=T.PAD)
        top.pack(fill=tk.X, padx=T.PAD)
        SectionLabel(top, "🛒  Shopping Cart").pack(side=tk.LEFT)
        StyledButton(top, "🗑  Clear Cart", self._clear_cart, variant="danger").pack(side=tk.RIGHT)

        # ── Items list ──
        list_frame = tk.Frame(self, bg=T.BG_LIGHT)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=T.PAD)

        headers = tk.Frame(list_frame, bg=T.PRIMARY)
        headers.pack(fill=tk.X)
        for text, width in [("Product", 30), ("Unit Price", 12), ("Qty", 8), ("Subtotal", 12), ("", 8)]:
            tk.Label(headers, text=text, font=T.FONT_SUBHEAD,
                     bg=T.PRIMARY, fg=T.TEXT_LIGHT,
                     width=width, anchor=tk.CENTER).pack(side=tk.LEFT, pady=4)

        self._items_canvas = tk.Canvas(list_frame, bg=T.BG_LIGHT, highlightthickness=0)
        vsb = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self._items_canvas.yview)
        self._items_canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self._items_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._items_frame = tk.Frame(self._items_canvas, bg=T.BG_LIGHT)
        self._items_canvas.create_window((0, 0), window=self._items_frame, anchor=tk.NW)
        self._items_frame.bind("<Configure>",
                               lambda _: self._items_canvas.configure(
                                   scrollregion=self._items_canvas.bbox("all")))

        # ── Summary card ──
        summary = Card(self, padx=16, pady=12)
        summary.pack(fill=tk.X, padx=T.PAD, pady=T.PAD)

        tk.Label(summary, text="Order Summary", font=T.FONT_SUBHEAD,
                 bg=T.BG_CARD, fg=T.TEXT_DARK).grid(row=0, column=0, columnspan=2, sticky=tk.W)

        tk.Label(summary, text="Items:", bg=T.BG_CARD, font=T.FONT_BODY).grid(
            row=1, column=0, sticky=tk.W, pady=2)
        self._items_count_lbl = tk.Label(summary, text="0", bg=T.BG_CARD, font=T.FONT_BODY)
        self._items_count_lbl.grid(row=1, column=1, sticky=tk.E)

        ttk.Separator(summary, orient=tk.HORIZONTAL).grid(row=2, column=0, columnspan=2, sticky=tk.EW, pady=6)

        tk.Label(summary, text="Total:", bg=T.BG_CARD,
                 font=(T.FONT_FAMILY, 13, "bold")).grid(row=3, column=0, sticky=tk.W)
        self._total_lbl = tk.Label(summary, text="$0.00", bg=T.BG_CARD,
                                   font=(T.FONT_FAMILY, 15, "bold"), fg=T.SUCCESS)
        self._total_lbl.grid(row=3, column=1, sticky=tk.E)

        summary.columnconfigure(1, weight=1)

        StyledButton(summary, "✅  Proceed to Checkout",
                     self._checkout, variant="success").grid(
            row=4, column=0, columnspan=2, sticky=tk.EW, pady=(12, 0), ipady=4)

    # ------------------------------------------------------------------

    def refresh(self):
        for widget in self._items_frame.winfo_children():
            widget.destroy()

        if self.cart.is_empty():
            tk.Label(self._items_frame, text="Your cart is empty.",
                     font=T.FONT_SUBHEAD, fg=T.TEXT_MUTED,
                     bg=T.BG_LIGHT).pack(pady=30)
        else:
            for item in self.cart.items:
                self._build_item_row(item)

        self._items_count_lbl.config(text=str(self.cart.item_count))
        self._total_lbl.config(text=self.cart.formatted_total())

    def _build_item_row(self, cart_item):
        row = tk.Frame(self._items_frame, bg=T.BG_CARD,
                       highlightthickness=1, highlightbackground=T.BORDER)
        row.pack(fill=tk.X, pady=2)

        tk.Label(row, text=cart_item.product.name, font=T.FONT_BODY,
                 bg=T.BG_CARD, fg=T.TEXT_DARK, width=30, anchor=tk.W).pack(side=tk.LEFT, padx=6)
        tk.Label(row, text=cart_item.product.formatted_price(), font=T.FONT_BODY,
                 bg=T.BG_CARD, width=12, anchor=tk.CENTER).pack(side=tk.LEFT)

        qty_var = tk.IntVar(value=cart_item.quantity)
        spin = tk.Spinbox(row, from_=1, to=cart_item.product.stock,
                          textvariable=qty_var, width=5, font=T.FONT_BODY,
                          command=lambda p=cart_item.product, q=qty_var: self._update_qty(p.id, q.get()))
        spin.pack(side=tk.LEFT, padx=4)
        spin.bind("<FocusOut>", lambda _, p=cart_item.product, q=qty_var: self._update_qty(p.id, q.get()))

        tk.Label(row, text=cart_item.formatted_subtotal(), font=T.FONT_BODY,
                 bg=T.BG_CARD, fg=T.SUCCESS, width=12, anchor=tk.CENTER).pack(side=tk.LEFT)

        StyledButton(row, "✕", lambda p=cart_item.product.id: self._remove_item(p),
                     variant="danger").pack(side=tk.LEFT, padx=4)

    def _update_qty(self, product_id: int, qty: int):
        try:
            self.cart.update_quantity(product_id, qty)
            self.on_cart_changed()
            self.refresh()
        except ValueError as e:
            messagebox.showwarning("Cart", str(e), parent=self)

    def _remove_item(self, product_id: int):
        self.cart.remove_item(product_id)
        self.on_cart_changed()
        self.refresh()

    def _clear_cart(self):
        if messagebox.askyesno("Clear Cart", "Remove all items from cart?", parent=self):
            self.cart.clear()
            self.on_cart_changed()
            self.refresh()

    # ------------------------------------------------------------------
    # Checkout
    # ------------------------------------------------------------------

    def _checkout(self):
        if self.cart.is_empty():
            messagebox.showinfo("Checkout", "Your cart is empty.", parent=self)
            return

        address = self.customer.address or ""
        address = simpledialog.askstring(
            "Shipping Address",
            "Enter your shipping address:",
            initialvalue=address,
            parent=self,
        )
        if address is None:
            return  # user cancelled
        if not address.strip():
            messagebox.showwarning("Checkout", "Shipping address cannot be empty.", parent=self)
            return

        items = [
            OrderItem(
                product_id=ci.product.id,
                product_name=ci.product.name,
                unit_price=ci.product.price,
                quantity=ci.quantity,
            )
            for ci in self.cart.items
        ]
        order = Order(
            customer_id=self.customer.id,
            customer_name=self.customer.full_name,
            shipping_address=address,
            items=items,
        )
        try:
            order = self.db.create_order(order)
        except Exception as e:
            messagebox.showerror("Order Error", str(e), parent=self)
            return

        self.cart.clear()
        self.on_cart_changed()
        self.refresh()
        messagebox.showinfo(
            "Order Placed! 🎉",
            f"Order #{order.id} placed successfully!\nTotal: {order.formatted_total()}\n"
            f"Status: {order.status.value}",
            parent=self,
        )
        self.on_order_placed()
