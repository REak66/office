"""Admin panel: product management + all orders overview."""

import tkinter as tk
from tkinter import messagebox, ttk

from . import theme as T
from .widgets import Card, DataTable, SectionLabel, StyledButton
from ..models.order import OrderStatus
from ..models.product import Product


class AdminView(tk.Frame):
    """Admin panel with tabs for Products and Orders management."""

    def __init__(self, master, db, **kwargs):
        super().__init__(master, bg=T.BG_LIGHT, **kwargs)
        self.db = db
        self._build()
        self.refresh()

    # ------------------------------------------------------------------

    def _build(self):
        top = tk.Frame(self, bg=T.BG_LIGHT, pady=T.PAD)
        top.pack(fill=tk.X, padx=T.PAD)
        SectionLabel(top, "⚙️  Admin Panel").pack(side=tk.LEFT)

        # Notebook
        nb = ttk.Notebook(self)
        nb.pack(fill=tk.BOTH, expand=True, padx=T.PAD, pady=T.PAD)

        self._products_tab = tk.Frame(nb, bg=T.BG_LIGHT)
        self._orders_tab   = tk.Frame(nb, bg=T.BG_LIGHT)
        self._customers_tab = tk.Frame(nb, bg=T.BG_LIGHT)
        nb.add(self._products_tab,  text="  🏷  Products  ")
        nb.add(self._orders_tab,    text="  📦  Orders  ")
        nb.add(self._customers_tab, text="  👤  Customers  ")
        nb.bind("<<NotebookTabChanged>>", lambda _: self.refresh())

        self._build_products_tab()
        self._build_orders_tab()
        self._build_customers_tab()

    # ── Products tab ─────────────────────────────────────────────────

    def _build_products_tab(self):
        f = self._products_tab
        btn_row = tk.Frame(f, bg=T.BG_LIGHT)
        btn_row.pack(fill=tk.X, padx=4, pady=6)
        StyledButton(btn_row, "➕ Add Product",    self._add_product,    variant="success").pack(side=tk.LEFT, padx=2)
        StyledButton(btn_row, "✏️  Edit Product",  self._edit_product,   variant="primary").pack(side=tk.LEFT, padx=2)
        StyledButton(btn_row, "🗑  Delete Product", self._delete_product, variant="danger").pack(side=tk.LEFT, padx=2)

        cols = ["ID", "Name", "Category", "Price", "Stock", "Description"]
        self._prod_table = DataTable(f, columns=cols)
        self._prod_table.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

    def _refresh_products(self):
        self._prod_table.clear()
        for p in self.db.list_products():
            self._prod_table.insert((
                p.id, p.name, p.category,
                p.formatted_price(), p.stock, p.description,
            ))

    def _add_product(self):
        ProductFormDialog(self, self.db, product=None, on_save=self._refresh_products)

    def _edit_product(self):
        vals = self._prod_table.selected_values()
        if not vals:
            messagebox.showinfo("Edit", "Please select a product first.", parent=self)
            return
        product = self.db.get_product_by_id(int(vals[0]))
        if product:
            ProductFormDialog(self, self.db, product=product, on_save=self._refresh_products)

    def _delete_product(self):
        vals = self._prod_table.selected_values()
        if not vals:
            messagebox.showinfo("Delete", "Please select a product first.", parent=self)
            return
        if messagebox.askyesno("Delete", f"Delete product '{vals[1]}'?", parent=self):
            self.db.delete_product(int(vals[0]))
            self._refresh_products()

    # ── Orders tab ───────────────────────────────────────────────────

    def _build_orders_tab(self):
        f = self._orders_tab

        btn_row = tk.Frame(f, bg=T.BG_LIGHT)
        btn_row.pack(fill=tk.X, padx=4, pady=6)
        tk.Label(btn_row, text="Set Status:", bg=T.BG_LIGHT, font=T.FONT_BODY).pack(side=tk.LEFT)
        self._status_var = tk.StringVar(value=OrderStatus.CONFIRMED.value)
        status_combo = ttk.Combobox(
            btn_row,
            textvariable=self._status_var,
            values=[s.value for s in OrderStatus],
            state="readonly",
            width=14,
        )
        status_combo.pack(side=tk.LEFT, padx=4)
        StyledButton(btn_row, "✅ Update Status", self._update_order_status, variant="primary").pack(side=tk.LEFT, padx=4)

        cols = ["Order #", "Customer", "Date", "Items", "Total", "Status", "Address"]
        self._orders_table = DataTable(f, columns=cols)
        self._orders_table.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)
        self._orders_table.tree.bind("<<TreeviewSelect>>", self._on_order_select)

        # Order items detail
        detail_lf = tk.LabelFrame(f, text="Order Items", bg=T.BG_LIGHT, font=T.FONT_BODY)
        detail_lf.pack(fill=tk.X, padx=4, pady=(0, 6))
        cols2 = ["Product", "Unit Price", "Qty", "Subtotal"]
        self._order_detail_table = DataTable(detail_lf, columns=cols2)
        self._order_detail_table.pack(fill=tk.X, padx=4, pady=4)
        self._order_detail_table.tree.configure(height=4)

    def _refresh_orders(self):
        self._orders_table.clear()
        for order in self.db.list_orders():
            self._orders_table.insert((
                f"#{order.id}",
                order.customer_name,
                order.created_at[:10],
                len(order.items),
                order.formatted_total(),
                order.status.value,
                order.shipping_address,
            ))

    def _on_order_select(self, _event=None):
        vals = self._orders_table.selected_values()
        if not vals:
            return
        order_id = int(str(vals[0]).lstrip("#"))
        order = self.db.get_order_by_id(order_id)
        if not order:
            return
        self._order_detail_table.clear()
        for item in order.items:
            self._order_detail_table.insert((
                item.product_name,
                f"${item.unit_price:,.2f}",
                item.quantity,
                item.formatted_subtotal(),
            ))

    def _update_order_status(self):
        vals = self._orders_table.selected_values()
        if not vals:
            messagebox.showinfo("Update", "Please select an order first.", parent=self)
            return
        order_id = int(str(vals[0]).lstrip("#"))
        new_status = OrderStatus(self._status_var.get())
        self.db.update_order_status(order_id, new_status)
        self._refresh_orders()

    # ── Customers tab ────────────────────────────────────────────────

    def _build_customers_tab(self):
        f = self._customers_tab
        cols = ["ID", "Username", "Full Name", "Email", "Phone", "Address", "Role"]
        self._cust_table = DataTable(f, columns=cols)
        self._cust_table.pack(fill=tk.BOTH, expand=True, padx=4, pady=8)

    def _refresh_customers(self):
        self._cust_table.clear()
        for c in self.db.list_customers():
            self._cust_table.insert((
                c.id, c.username, c.full_name, c.email,
                c.phone, c.address, "Admin" if c.is_admin else "Customer",
            ))

    # ------------------------------------------------------------------

    def refresh(self):
        self._refresh_products()
        self._refresh_orders()
        self._refresh_customers()


# ── Product Form Dialog ──────────────────────────────────────────────────────

class ProductFormDialog(tk.Toplevel):
    """Dialog for adding or editing a product."""

    def __init__(self, master, db, product: Product | None, on_save):
        super().__init__(master)
        self.db = db
        self.product = product
        self.on_save = on_save
        self.title("Edit Product" if product else "Add Product")
        self.resizable(False, False)
        self.configure(bg=T.BG_LIGHT)
        self.grab_set()
        self._build()
        self._center()

    def _center(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"+{x}+{y}")

    def _build(self):
        f = tk.Frame(self, bg=T.BG_LIGHT, padx=20, pady=16)
        f.pack()

        fields_cfg = [
            ("Name *",       "_f_name",  "entry"),
            ("Category *",   "_f_cat",   "entry"),
            ("Price ($) *",  "_f_price", "entry"),
            ("Stock *",      "_f_stock", "entry"),
            ("Description",  "_f_desc",  "text"),
        ]

        for i, (label, attr, kind) in enumerate(fields_cfg):
            tk.Label(f, text=label, bg=T.BG_LIGHT, font=T.FONT_BODY).grid(
                row=i, column=0, sticky=tk.W, padx=(0, 10), pady=4)
            if kind == "text":
                widget = tk.Text(f, font=T.FONT_BODY, width=32, height=3,
                                 relief=tk.SOLID, bd=1)
            else:
                widget = tk.Entry(f, font=T.FONT_BODY, width=32, relief=tk.SOLID, bd=1)
            widget.grid(row=i, column=1, sticky=tk.EW, pady=4)
            setattr(self, attr, widget)

        # Prefill if editing
        if self.product:
            self._f_name.insert(0, self.product.name)
            self._f_cat.insert(0,  self.product.category)
            self._f_price.insert(0, str(self.product.price))
            self._f_stock.insert(0, str(self.product.stock))
            self._f_desc.insert("1.0", self.product.description)

        btn_row = tk.Frame(f, bg=T.BG_LIGHT)
        btn_row.grid(row=len(fields_cfg), column=0, columnspan=2, pady=(12, 0), sticky=tk.E)
        StyledButton(btn_row, "Save",   self._save,              variant="success").pack(side=tk.LEFT, padx=4)
        StyledButton(btn_row, "Cancel", self.destroy,            variant="secondary").pack(side=tk.LEFT)

    def _save(self):
        name     = self._f_name.get().strip()
        category = self._f_cat.get().strip()
        price_s  = self._f_price.get().strip()
        stock_s  = self._f_stock.get().strip()
        desc     = self._f_desc.get("1.0", tk.END).strip()

        if not name or not category or not price_s or not stock_s:
            messagebox.showwarning("Validation", "Please fill in all required fields.", parent=self)
            return
        try:
            price = float(price_s)
            stock = int(stock_s)
        except ValueError:
            messagebox.showerror("Validation", "Price must be a number; stock must be an integer.", parent=self)
            return

        try:
            if self.product:
                self.product.name        = name
                self.product.category    = category
                self.product.price       = price
                self.product.stock       = stock
                self.product.description = desc
                self.db.update_product(self.product)
            else:
                new_product = Product(name=name, price=price, stock=stock,
                                      category=category, description=desc)
                self.db.create_product(new_product)
        except ValueError as e:
            messagebox.showerror("Validation", str(e), parent=self)
            return

        self.on_save()
        self.destroy()
