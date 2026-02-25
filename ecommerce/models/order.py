"""Order and OrderItem models for the E-commerce Mini-system."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional


class OrderStatus(Enum):
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


@dataclass
class OrderItem:
    """Represents a snapshot of one product line in a placed order."""

    product_id: int
    product_name: str
    unit_price: float
    quantity: int
    id: Optional[int] = None
    order_id: Optional[int] = None

    @property
    def subtotal(self) -> float:
        return self.unit_price * self.quantity

    def formatted_subtotal(self) -> str:
        return f"${self.subtotal:,.2f}"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "unit_price": self.unit_price,
            "quantity": self.quantity,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "OrderItem":
        return cls(
            id=data.get("id"),
            order_id=data.get("order_id"),
            product_id=data["product_id"],
            product_name=data["product_name"],
            unit_price=data["unit_price"],
            quantity=data["quantity"],
        )


@dataclass
class Order:
    """Represents a customer order with a list of OrderItems."""

    customer_id: int
    customer_name: str
    shipping_address: str
    items: List[OrderItem] = field(default_factory=list)
    id: Optional[int] = None
    status: OrderStatus = OrderStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    notes: str = ""

    @property
    def total(self) -> float:
        return sum(item.subtotal for item in self.items)

    def formatted_total(self) -> str:
        return f"${self.total:,.2f}"

    def update_status(self, new_status: OrderStatus) -> None:
        self.status = new_status
        self.updated_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "shipping_address": self.shipping_address,
            "status": self.status.value,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "items": [item.to_dict() for item in self.items],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Order":
        items = [OrderItem.from_dict(i) for i in data.get("items", [])]
        return cls(
            id=data.get("id"),
            customer_id=data["customer_id"],
            customer_name=data["customer_name"],
            shipping_address=data["shipping_address"],
            status=OrderStatus(data.get("status", OrderStatus.PENDING.value)),
            notes=data.get("notes", ""),
            created_at=data.get("created_at", datetime.now().isoformat()),
            updated_at=data.get("updated_at", datetime.now().isoformat()),
            items=items,
        )

    def __str__(self) -> str:
        return (
            f"Order(id={self.id}, customer='{self.customer_name}', "
            f"status={self.status.value}, total={self.formatted_total()})"
        )
