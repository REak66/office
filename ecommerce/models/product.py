"""Product model for the E-commerce Mini-system."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Product:
    """Represents a product in the e-commerce system."""

    name: str
    price: float
    stock: int
    category: str
    description: str = ""
    id: Optional[int] = None
    image_path: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def __post_init__(self):
        if self.price < 0:
            raise ValueError("Price cannot be negative.")
        if self.stock < 0:
            raise ValueError("Stock cannot be negative.")

    def is_available(self) -> bool:
        """Return True if the product is in stock."""
        return self.stock > 0

    def reduce_stock(self, quantity: int) -> None:
        """Reduce stock by the given quantity."""
        if quantity > self.stock:
            raise ValueError(
                f"Insufficient stock. Available: {self.stock}, Requested: {quantity}"
            )
        self.stock -= quantity

    def restore_stock(self, quantity: int) -> None:
        """Restore stock by the given quantity (e.g., when order is cancelled)."""
        self.stock += quantity

    def formatted_price(self) -> str:
        """Return price formatted as currency string."""
        return f"${self.price:,.2f}"

    def to_dict(self) -> dict:
        """Serialize product to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "category": self.category,
            "description": self.description,
            "image_path": self.image_path,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        """Deserialize product from dictionary."""
        return cls(
            id=data.get("id"),
            name=data["name"],
            price=data["price"],
            stock=data["stock"],
            category=data["category"],
            description=data.get("description", ""),
            image_path=data.get("image_path", ""),
            created_at=data.get("created_at", datetime.now().isoformat()),
        )

    def __str__(self) -> str:
        return f"Product(id={self.id}, name='{self.name}', price={self.formatted_price()}, stock={self.stock})"
