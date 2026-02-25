"""Customer model for the E-commerce Mini-system."""

import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Customer:
    """Represents a customer in the e-commerce system."""

    username: str
    email: str
    full_name: str
    address: str = ""
    phone: str = ""
    id: Optional[int] = None
    is_admin: bool = False
    _password_hash: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def set_password(self, password: str) -> None:
        """Hash and store the customer password."""
        if len(password) < 4:
            raise ValueError("Password must be at least 4 characters.")
        self._password_hash = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password: str) -> bool:
        """Verify if the provided password matches the stored hash."""
        return self._password_hash == hashlib.sha256(password.encode()).hexdigest()

    def to_dict(self) -> dict:
        """Serialize customer to dictionary."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "address": self.address,
            "phone": self.phone,
            "is_admin": self.is_admin,
            "password_hash": self._password_hash,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Customer":
        """Deserialize customer from dictionary."""
        customer = cls(
            id=data.get("id"),
            username=data["username"],
            email=data["email"],
            full_name=data["full_name"],
            address=data.get("address", ""),
            phone=data.get("phone", ""),
            is_admin=data.get("is_admin", False),
            created_at=data.get("created_at", datetime.now().isoformat()),
        )
        customer._password_hash = data.get("password_hash", "")
        return customer

    def __str__(self) -> str:
        return f"Customer(id={self.id}, username='{self.username}', email='{self.email}')"
