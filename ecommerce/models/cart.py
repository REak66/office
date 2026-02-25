"""Cart and CartItem models for the E-commerce Mini-system."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .product import Product


@dataclass
class CartItem:
    """Represents a single item line in the shopping cart."""

    product: Product
    quantity: int = 1

    def __post_init__(self):
        if self.quantity < 1:
            raise ValueError("Quantity must be at least 1.")

    @property
    def subtotal(self) -> float:
        """Calculate subtotal for this cart item."""
        return self.product.price * self.quantity

    def formatted_subtotal(self) -> str:
        return f"${self.subtotal:,.2f}"

    def __str__(self) -> str:
        return (
            f"CartItem(product='{self.product.name}', qty={self.quantity}, "
            f"subtotal={self.formatted_subtotal()})"
        )


class Cart:
    """Shopping cart that holds CartItem objects keyed by product id."""

    def __init__(self, customer_id: Optional[int] = None):
        self.customer_id = customer_id
        self._items: Dict[int, CartItem] = {}

    # ------------------------------------------------------------------
    # Mutators
    # ------------------------------------------------------------------

    def add_item(self, product: Product, quantity: int = 1) -> None:
        """Add a product to the cart or increase its quantity."""
        if product.id is None:
            raise ValueError("Product must have a valid id.")
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        if quantity > product.stock:
            raise ValueError(
                f"Cannot add {quantity} items; only {product.stock} in stock."
            )

        if product.id in self._items:
            new_qty = self._items[product.id].quantity + quantity
            if new_qty > product.stock:
                raise ValueError(
                    f"Total quantity ({new_qty}) exceeds available stock ({product.stock})."
                )
            self._items[product.id].quantity = new_qty
        else:
            self._items[product.id] = CartItem(product=product, quantity=quantity)

    def remove_item(self, product_id: int) -> None:
        """Remove a product entirely from the cart."""
        if product_id not in self._items:
            raise KeyError(f"Product id {product_id} not in cart.")
        del self._items[product_id]

    def update_quantity(self, product_id: int, quantity: int) -> None:
        """Update the quantity for a cart item; removes item if quantity <= 0."""
        if product_id not in self._items:
            raise KeyError(f"Product id {product_id} not in cart.")
        if quantity <= 0:
            self.remove_item(product_id)
        else:
            product = self._items[product_id].product
            if quantity > product.stock:
                raise ValueError(
                    f"Quantity ({quantity}) exceeds available stock ({product.stock})."
                )
            self._items[product_id].quantity = quantity

    def clear(self) -> None:
        """Empty the cart."""
        self._items.clear()

    # ------------------------------------------------------------------
    # Accessors
    # ------------------------------------------------------------------

    @property
    def items(self) -> List[CartItem]:
        return list(self._items.values())

    @property
    def total(self) -> float:
        """Return the grand total of all cart items."""
        return sum(item.subtotal for item in self._items.values())

    @property
    def item_count(self) -> int:
        """Return the total number of individual units in the cart."""
        return sum(item.quantity for item in self._items.values())

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def formatted_total(self) -> str:
        return f"${self.total:,.2f}"

    def __len__(self) -> int:
        return len(self._items)

    def __str__(self) -> str:
        lines = [f"Cart (customer_id={self.customer_id}):"]
        for item in self._items.values():
            lines.append(f"  {item}")
        lines.append(f"  Total: {self.formatted_total()}")
        return "\n".join(lines)
