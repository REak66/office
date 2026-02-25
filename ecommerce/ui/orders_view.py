"""Order history view for customers."""

import tkinter as tk
from tkinter import ttk

from . import theme as T
from .widgets import DataTable, SectionLabel


class OrdersView(tk.Frame):
    """Displays the logged-in customer's order history."""

    def __init__(self, master, db, customer, **kwargs):
        super().__init__(master, bg=T.BG_LIGHT, **kwargs)
        self.db = db
        self.customer = customer
        self._build()
        self.refresh()

    # ------------------------------------------------------------------

    def _build(self):
        top = tk.Frame(self, bg=T.BG_LIGHT, pady=T.PAD)
        top.pack(fill=tk.X, padx=T.PAD)
        SectionLabel(top, "📦  My Orders").pack(side=tk.LEFT)

        # Orders table
        cols = ["Order #", "Date", "Items", "Total", "Status", "Shipping Address"]
        self._table = DataTable(self, columns=cols)
        self._table.pack(fill=tk.BOTH, expand=True, padx=T.PAD, pady=T.PAD)
        self._table.tree.bind("<<TreeviewSelect>>", self._on_select)

        # Detail panel
        detail_lf = tk.LabelFrame(self, text="Order Details",
                                  bg=T.BG_LIGHT, font=T.FONT_BODY)
        detail_lf.pack(fill=tk.X, padx=T.PAD, pady=(0, T.PAD))

        cols2 = ["Product", "Unit Price", "Qty", "Subtotal"]
        self._detail_table = DataTable(detail_lf, columns=cols2)
        self._detail_table.pack(fill=tk.X, padx=4, pady=4)
        self._detail_table.tree.configure(height=5)

    # ------------------------------------------------------------------

    def refresh(self):
        self._table.clear()
        orders = self.db.list_orders(customer_id=self.customer.id)
        for order in orders:
            date_str = order.created_at[:10] if order.created_at else ""
            self._table.insert((
                f"#{order.id}",
                date_str,
                len(order.items),
                order.formatted_total(),
                order.status.value,
                order.shipping_address,
            ))

    def _on_select(self, _event=None):
        vals = self._table.selected_values()
        if not vals:
            return
        order_id_str = str(vals[0]).lstrip("#")
        try:
            order_id = int(order_id_str)
        except ValueError:
            return
        order = self.db.get_order_by_id(order_id)
        if not order:
            return
        self._detail_table.clear()
        for item in order.items:
            self._detail_table.insert((
                item.product_name,
                f"${item.unit_price:,.2f}",
                item.quantity,
                item.formatted_subtotal(),
            ))
