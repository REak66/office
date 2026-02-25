"""Products browsing view for customers."""

import tkinter as tk
from tkinter import messagebox, ttk

from . import theme as T
from .widgets import Card, DataTable, SearchBar, SectionLabel, StyledButton


class ProductsView(tk.Frame):
    """Browse products, filter by category, and add them to the cart."""

    def __init__(self, master, db, cart, on_cart_changed, **kwargs):
        super().__init__(master, bg=T.BG_LIGHT, **kwargs)
        self.db = db
        self.cart = cart
        self.on_cart_changed = on_cart_changed
        self._selected_category = tk.StringVar(value="All")
        self._build()
        self.refresh()

    # ------------------------------------------------------------------

    def _build(self):
        # ── Top bar ──
        top = tk.Frame(self, bg=T.BG_LIGHT, pady=T.PAD)
        top.pack(fill=tk.X, padx=T.PAD)

        SectionLabel(top, "🛍  Products").pack(side=tk.LEFT)

        # Category filter
        filter_frame = tk.Frame(top, bg=T.BG_LIGHT)
        filter_frame.pack(side=tk.RIGHT)
        tk.Label(filter_frame, text="Category:", bg=T.BG_LIGHT, font=T.FONT_BODY).pack(side=tk.LEFT)
        self._cat_combo = ttk.Combobox(
            filter_frame,
            textvariable=self._selected_category,
            state="readonly",
            width=16,
            font=T.FONT_BODY,
        )
        self._cat_combo.pack(side=tk.LEFT, padx=(4, 0))
        self._cat_combo.bind("<<ComboboxSelected>>", lambda _: self.refresh())

        # ── Search ──
        search_row = tk.Frame(self, bg=T.BG_LIGHT, pady=4)
        search_row.pack(fill=tk.X, padx=T.PAD)
        SearchBar(search_row, "Search products…", self._do_search).pack(side=tk.LEFT)

        # ── Products grid (scrollable canvas) ──
        self._canvas_frame = tk.Frame(self, bg=T.BG_LIGHT)
        self._canvas_frame.pack(fill=tk.BOTH, expand=True, padx=T.PAD, pady=T.PAD)

        self._canvas = tk.Canvas(self._canvas_frame, bg=T.BG_LIGHT, highlightthickness=0)
        vsb = ttk.Scrollbar(self._canvas_frame, orient=tk.VERTICAL, command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self._canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._grid_frame = tk.Frame(self._canvas, bg=T.BG_LIGHT)
        self._canvas_window = self._canvas.create_window((0, 0), window=self._grid_frame, anchor=tk.NW)

        self._grid_frame.bind("<Configure>", self._on_frame_configure)
        self._canvas.bind("<Configure>",     self._on_canvas_configure)
        self._canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_frame_configure(self, _event=None):
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self._canvas.itemconfig(self._canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # ------------------------------------------------------------------

    def refresh(self):
        cat = self._selected_category.get()
        products = self.db.list_products(category=None if cat == "All" else cat)
        self._render_products(products)
        # Update category combo
        cats = ["All"] + self.db.list_categories()
        self._cat_combo["values"] = cats

    def _do_search(self, query: str):
        query = query.strip().lower()
        cat = self._selected_category.get()
        all_products = self.db.list_products(category=None if cat == "All" else cat)
        if query and query not in ("search products…", ""):
            all_products = [
                p for p in all_products
                if query in p.name.lower() or query in p.category.lower() or query in p.description.lower()
            ]
        self._render_products(all_products)

    def _render_products(self, products):
        # Clear grid
        for widget in self._grid_frame.winfo_children():
            widget.destroy()

        COLS = 3
        for idx, product in enumerate(products):
            row, col = divmod(idx, COLS)
            self._build_product_card(self._grid_frame, product).grid(
                row=row, column=col, padx=8, pady=8, sticky="nsew"
            )
        for c in range(COLS):
            self._grid_frame.columnconfigure(c, weight=1)

        if not products:
            tk.Label(
                self._grid_frame,
                text="No products found.",
                font=T.FONT_SUBHEAD,
                fg=T.TEXT_MUTED,
                bg=T.BG_LIGHT,
            ).grid(row=0, column=0, columnspan=COLS, pady=40)

    def _build_product_card(self, parent, product) -> Card:
        card = Card(parent, padx=12, pady=12)

        # Category badge
        tk.Label(card, text=product.category, font=T.FONT_CAPTION,
                 bg=T.SECONDARY, fg=T.TEXT_LIGHT, padx=6, pady=2).pack(anchor=tk.W)

        # Product name
        tk.Label(card, text=product.name, font=T.FONT_SUBHEAD,
                 bg=T.BG_CARD, fg=T.TEXT_DARK, wraplength=220).pack(anchor=tk.W, pady=(6, 2))

        # Description
        tk.Label(card, text=product.description or "No description.",
                 font=T.FONT_CAPTION, fg=T.TEXT_MUTED, bg=T.BG_CARD,
                 wraplength=220, justify=tk.LEFT).pack(anchor=tk.W)

        # Separator
        ttk.Separator(card, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=8)

        # Price & Stock row
        bottom = tk.Frame(card, bg=T.BG_CARD)
        bottom.pack(fill=tk.X)

        tk.Label(bottom, text=product.formatted_price(),
                 font=(T.FONT_FAMILY, 14, "bold"),
                 fg=T.SUCCESS, bg=T.BG_CARD).pack(side=tk.LEFT)

        stock_colour = T.SUCCESS if product.stock > 5 else (T.WARNING if product.stock > 0 else T.DANGER)
        tk.Label(bottom, text=f"Stock: {product.stock}",
                 font=T.FONT_SMALL, fg=stock_colour, bg=T.BG_CARD).pack(side=tk.RIGHT)

        # Quantity + Add to Cart
        ctrl = tk.Frame(card, bg=T.BG_CARD)
        ctrl.pack(fill=tk.X, pady=(8, 0))

        qty_var = tk.IntVar(value=1)
        tk.Label(ctrl, text="Qty:", bg=T.BG_CARD, font=T.FONT_BODY).pack(side=tk.LEFT)
        qty_spin = tk.Spinbox(ctrl, from_=1, to=max(1, product.stock),
                              textvariable=qty_var, width=4, font=T.FONT_BODY)
        qty_spin.pack(side=tk.LEFT, padx=(4, 8))

        if product.is_available():
            StyledButton(card, "🛒  Add to Cart",
                         lambda p=product, q=qty_var: self._add_to_cart(p, q.get()),
                         variant="primary").pack(fill=tk.X, pady=(4, 0))
        else:
            tk.Label(card, text="Out of Stock", font=T.FONT_BODY,
                     fg=T.TEXT_LIGHT, bg=T.DANGER).pack(fill=tk.X, pady=(4, 0))
        return card

    def _add_to_cart(self, product, quantity: int):
        # Refresh product from DB to get latest stock
        fresh = self.db.get_product_by_id(product.id)
        if not fresh:
            messagebox.showerror("Error", "Product not found.")
            return
        try:
            self.cart.add_item(fresh, quantity)
            self.on_cart_changed()
            messagebox.showinfo("Cart", f"Added {quantity}× '{fresh.name}' to cart.", parent=self)
        except ValueError as e:
            messagebox.showwarning("Cart", str(e), parent=self)
