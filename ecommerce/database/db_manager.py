"""SQLite-backed persistence layer for the E-commerce Mini-system."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import List, Optional

from ..models.customer import Customer
from ..models.order import Order, OrderItem, OrderStatus
from ..models.product import Product


class DatabaseManager:
    """Manages all SQLite interactions for the e-commerce system."""

    def __init__(self, db_path: str = "ecommerce.db"):
        self.db_path = str(Path(db_path).resolve())
        self._init_db()
        self._seed_default_data()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @contextmanager
    def _connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_db(self) -> None:
        """Create tables if they do not exist."""
        with self._connection() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS customers (
                    id            INTEGER PRIMARY KEY AUTOINCREMENT,
                    username      TEXT    NOT NULL UNIQUE,
                    email         TEXT    NOT NULL UNIQUE,
                    full_name     TEXT    NOT NULL,
                    address       TEXT    DEFAULT '',
                    phone         TEXT    DEFAULT '',
                    is_admin      INTEGER DEFAULT 0,
                    password_hash TEXT    NOT NULL,
                    created_at    TEXT    NOT NULL
                );

                CREATE TABLE IF NOT EXISTS products (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    name        TEXT    NOT NULL,
                    price       REAL    NOT NULL,
                    stock       INTEGER NOT NULL DEFAULT 0,
                    category    TEXT    NOT NULL,
                    description TEXT    DEFAULT '',
                    image_path  TEXT    DEFAULT '',
                    created_at  TEXT    NOT NULL
                );

                CREATE TABLE IF NOT EXISTS orders (
                    id               INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id      INTEGER NOT NULL,
                    customer_name    TEXT    NOT NULL,
                    shipping_address TEXT    NOT NULL,
                    status           TEXT    NOT NULL DEFAULT 'Pending',
                    notes            TEXT    DEFAULT '',
                    created_at       TEXT    NOT NULL,
                    updated_at       TEXT    NOT NULL,
                    FOREIGN KEY (customer_id) REFERENCES customers(id)
                );

                CREATE TABLE IF NOT EXISTS order_items (
                    id           INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id     INTEGER NOT NULL,
                    product_id   INTEGER NOT NULL,
                    product_name TEXT    NOT NULL,
                    unit_price   REAL    NOT NULL,
                    quantity     INTEGER NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
                );
                """
            )

    def _seed_default_data(self) -> None:
        """Insert demo data if the database is empty."""
        with self._connection() as conn:
            if conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0] == 0:
                # Default admin
                admin = Customer(
                    username="admin",
                    email="admin@shop.com",
                    full_name="Shop Administrator",
                    is_admin=True,
                )
                admin.set_password("admin123")
                conn.execute(
                    "INSERT INTO customers (username,email,full_name,address,phone,"
                    "is_admin,password_hash,created_at) VALUES (?,?,?,?,?,?,?,?)",
                    (
                        admin.username,
                        admin.email,
                        admin.full_name,
                        admin.address,
                        admin.phone,
                        int(admin.is_admin),
                        admin._password_hash,
                        admin.created_at,
                    ),
                )
                # Demo customer
                demo = Customer(
                    username="customer1",
                    email="customer1@example.com",
                    full_name="Alice Smith",
                    address="123 Main St, Springfield",
                    phone="555-1234",
                )
                demo.set_password("pass1234")
                conn.execute(
                    "INSERT INTO customers (username,email,full_name,address,phone,"
                    "is_admin,password_hash,created_at) VALUES (?,?,?,?,?,?,?,?)",
                    (
                        demo.username,
                        demo.email,
                        demo.full_name,
                        demo.address,
                        demo.phone,
                        int(demo.is_admin),
                        demo._password_hash,
                        demo.created_at,
                    ),
                )

            if conn.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
                sample_products = [
                    ("Laptop Pro 15", 1299.99, 10, "Electronics",
                     "High-performance 15-inch laptop with Intel i7 processor."),
                    ("Wireless Headphones", 89.99, 25, "Electronics",
                     "Noise-cancelling over-ear headphones with 30hr battery."),
                    ("Running Shoes", 59.99, 50, "Footwear",
                     "Lightweight breathable running shoes, sizes 6-13."),
                    ("Coffee Maker Deluxe", 49.99, 15, "Home & Kitchen",
                     "12-cup programmable coffee maker with thermal carafe."),
                    ("Python Programming Book", 39.99, 30, "Books",
                     "Comprehensive guide to Python 3 programming."),
                    ("Yoga Mat", 24.99, 40, "Sports",
                     "Non-slip eco-friendly yoga mat, 6mm thick."),
                    ("Desk Lamp LED", 34.99, 20, "Home & Office",
                     "Adjustable LED desk lamp with USB charging port."),
                    ("Backpack Urban", 44.99, 18, "Accessories",
                     "Durable 30L backpack with laptop compartment."),
                ]
                from datetime import datetime
                now = datetime.now().isoformat()
                for name, price, stock, category, desc in sample_products:
                    conn.execute(
                        "INSERT INTO products (name,price,stock,category,description,image_path,created_at)"
                        " VALUES (?,?,?,?,?,?,?)",
                        (name, price, stock, category, desc, "", now),
                    )

    # ------------------------------------------------------------------
    # Customer CRUD
    # ------------------------------------------------------------------

    def get_customer_by_username(self, username: str) -> Optional[Customer]:
        with self._connection() as conn:
            row = conn.execute(
                "SELECT * FROM customers WHERE username=?", (username,)
            ).fetchone()
            return Customer.from_dict(dict(row)) if row else None

    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        with self._connection() as conn:
            row = conn.execute(
                "SELECT * FROM customers WHERE id=?", (customer_id,)
            ).fetchone()
            return Customer.from_dict(dict(row)) if row else None

    def create_customer(self, customer: Customer) -> Customer:
        with self._connection() as conn:
            cursor = conn.execute(
                "INSERT INTO customers (username,email,full_name,address,phone,"
                "is_admin,password_hash,created_at) VALUES (?,?,?,?,?,?,?,?)",
                (
                    customer.username,
                    customer.email,
                    customer.full_name,
                    customer.address,
                    customer.phone,
                    int(customer.is_admin),
                    customer._password_hash,
                    customer.created_at,
                ),
            )
            customer.id = cursor.lastrowid
        return customer

    def update_customer(self, customer: Customer) -> None:
        with self._connection() as conn:
            conn.execute(
                "UPDATE customers SET email=?,full_name=?,address=?,phone=? WHERE id=?",
                (customer.email, customer.full_name, customer.address, customer.phone, customer.id),
            )

    def list_customers(self) -> List[Customer]:
        with self._connection() as conn:
            rows = conn.execute("SELECT * FROM customers ORDER BY id").fetchall()
            return [Customer.from_dict(dict(r)) for r in rows]

    # ------------------------------------------------------------------
    # Product CRUD
    # ------------------------------------------------------------------

    def list_products(self, category: Optional[str] = None) -> List[Product]:
        with self._connection() as conn:
            if category:
                rows = conn.execute(
                    "SELECT * FROM products WHERE category=? ORDER BY name", (category,)
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM products ORDER BY name"
                ).fetchall()
            return [Product.from_dict(dict(r)) for r in rows]

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        with self._connection() as conn:
            row = conn.execute(
                "SELECT * FROM products WHERE id=?", (product_id,)
            ).fetchone()
            return Product.from_dict(dict(row)) if row else None

    def create_product(self, product: Product) -> Product:
        with self._connection() as conn:
            cursor = conn.execute(
                "INSERT INTO products (name,price,stock,category,description,image_path,created_at)"
                " VALUES (?,?,?,?,?,?,?)",
                (
                    product.name,
                    product.price,
                    product.stock,
                    product.category,
                    product.description,
                    product.image_path,
                    product.created_at,
                ),
            )
            product.id = cursor.lastrowid
        return product

    def update_product(self, product: Product) -> None:
        with self._connection() as conn:
            conn.execute(
                "UPDATE products SET name=?,price=?,stock=?,category=?,description=?,"
                "image_path=? WHERE id=?",
                (
                    product.name,
                    product.price,
                    product.stock,
                    product.category,
                    product.description,
                    product.image_path,
                    product.id,
                ),
            )

    def delete_product(self, product_id: int) -> None:
        with self._connection() as conn:
            conn.execute("DELETE FROM products WHERE id=?", (product_id,))

    def list_categories(self) -> List[str]:
        with self._connection() as conn:
            rows = conn.execute(
                "SELECT DISTINCT category FROM products ORDER BY category"
            ).fetchall()
            return [r[0] for r in rows]

    # ------------------------------------------------------------------
    # Order CRUD
    # ------------------------------------------------------------------

    def create_order(self, order: Order) -> Order:
        with self._connection() as conn:
            cursor = conn.execute(
                "INSERT INTO orders (customer_id,customer_name,shipping_address,"
                "status,notes,created_at,updated_at) VALUES (?,?,?,?,?,?,?)",
                (
                    order.customer_id,
                    order.customer_name,
                    order.shipping_address,
                    order.status.value,
                    order.notes,
                    order.created_at,
                    order.updated_at,
                ),
            )
            order.id = cursor.lastrowid
            for item in order.items:
                item.order_id = order.id
                item_cursor = conn.execute(
                    "INSERT INTO order_items (order_id,product_id,product_name,"
                    "unit_price,quantity) VALUES (?,?,?,?,?)",
                    (
                        item.order_id,
                        item.product_id,
                        item.product_name,
                        item.unit_price,
                        item.quantity,
                    ),
                )
                item.id = item_cursor.lastrowid
                # Reduce stock in DB
                conn.execute(
                    "UPDATE products SET stock = stock - ? WHERE id=?",
                    (item.quantity, item.product_id),
                )
        return order

    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        with self._connection() as conn:
            row = conn.execute("SELECT * FROM orders WHERE id=?", (order_id,)).fetchone()
            if not row:
                return None
            order_data = dict(row)
            items_rows = conn.execute(
                "SELECT * FROM order_items WHERE order_id=?", (order_id,)
            ).fetchall()
            order_data["items"] = [dict(r) for r in items_rows]
            return Order.from_dict(order_data)

    def list_orders(self, customer_id: Optional[int] = None) -> List[Order]:
        with self._connection() as conn:
            if customer_id:
                rows = conn.execute(
                    "SELECT * FROM orders WHERE customer_id=? ORDER BY created_at DESC",
                    (customer_id,),
                ).fetchall()
            else:
                rows = conn.execute(
                    "SELECT * FROM orders ORDER BY created_at DESC"
                ).fetchall()
            orders = []
            for row in rows:
                order_data = dict(row)
                items_rows = conn.execute(
                    "SELECT * FROM order_items WHERE order_id=?", (order_data["id"],)
                ).fetchall()
                order_data["items"] = [dict(r) for r in items_rows]
                orders.append(Order.from_dict(order_data))
            return orders

    def update_order_status(self, order_id: int, status: OrderStatus) -> None:
        from datetime import datetime
        with self._connection() as conn:
            conn.execute(
                "UPDATE orders SET status=?, updated_at=? WHERE id=?",
                (status.value, datetime.now().isoformat(), order_id),
            )
