"""Unit tests for the E-commerce Mini-System models and database layer."""

import os
import sys
import tempfile
import unittest

# Make sure the ecommerce package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from ecommerce.database.db_manager import DatabaseManager
from ecommerce.models.cart import Cart, CartItem
from ecommerce.models.customer import Customer
from ecommerce.models.order import Order, OrderItem, OrderStatus
from ecommerce.models.product import Product


class TestProduct(unittest.TestCase):
    def _make(self, **kw):
        defaults = dict(name="Widget", price=9.99, stock=10, category="Test")
        defaults.update(kw)
        return Product(**defaults)

    def test_creation(self):
        p = self._make()
        self.assertEqual(p.name, "Widget")
        self.assertEqual(p.price, 9.99)

    def test_negative_price_raises(self):
        with self.assertRaises(ValueError):
            self._make(price=-1)

    def test_negative_stock_raises(self):
        with self.assertRaises(ValueError):
            self._make(stock=-1)

    def test_is_available(self):
        self.assertTrue(self._make(stock=1).is_available())
        self.assertFalse(self._make(stock=0).is_available())

    def test_reduce_stock(self):
        p = self._make(stock=5)
        p.reduce_stock(3)
        self.assertEqual(p.stock, 2)

    def test_reduce_stock_insufficient(self):
        p = self._make(stock=2)
        with self.assertRaises(ValueError):
            p.reduce_stock(5)

    def test_restore_stock(self):
        p = self._make(stock=0)
        p.restore_stock(3)
        self.assertEqual(p.stock, 3)

    def test_formatted_price(self):
        self.assertEqual(self._make(price=1234.5).formatted_price(), "$1,234.50")

    def test_to_dict_round_trip(self):
        p = self._make(id=7)
        p2 = Product.from_dict(p.to_dict())
        self.assertEqual(p.name, p2.name)
        self.assertEqual(p.price, p2.price)
        self.assertEqual(p.id, p2.id)


class TestCustomer(unittest.TestCase):
    def _make(self, **kw):
        defaults = dict(username="alice", email="alice@x.com", full_name="Alice Smith")
        defaults.update(kw)
        return Customer(**defaults)

    def test_password_hash_and_check(self):
        c = self._make()
        c.set_password("secret")
        self.assertTrue(c.check_password("secret"))
        self.assertFalse(c.check_password("wrong"))

    def test_short_password_raises(self):
        c = self._make()
        with self.assertRaises(ValueError):
            c.set_password("ab")

    def test_to_dict_round_trip(self):
        c = self._make(id=3)
        c.set_password("pass1234")
        c2 = Customer.from_dict(c.to_dict())
        self.assertEqual(c.username, c2.username)
        self.assertTrue(c2.check_password("pass1234"))


class TestCart(unittest.TestCase):
    def _product(self, pid=1, stock=10):
        return Product(id=pid, name=f"P{pid}", price=5.0, stock=stock, category="C")

    def test_add_item(self):
        cart = Cart()
        p = self._product()
        cart.add_item(p, 2)
        self.assertEqual(cart.item_count, 2)

    def test_add_item_increments(self):
        cart = Cart()
        p = self._product()
        cart.add_item(p, 2)
        cart.add_item(p, 3)
        self.assertEqual(cart.items[0].quantity, 5)

    def test_add_item_exceeds_stock(self):
        cart = Cart()
        p = self._product(stock=3)
        with self.assertRaises(ValueError):
            cart.add_item(p, 5)

    def test_remove_item(self):
        cart = Cart()
        p = self._product()
        cart.add_item(p)
        cart.remove_item(p.id)
        self.assertTrue(cart.is_empty())

    def test_update_quantity(self):
        cart = Cart()
        p = self._product()
        cart.add_item(p, 3)
        cart.update_quantity(p.id, 7)
        self.assertEqual(cart.items[0].quantity, 7)

    def test_update_quantity_to_zero_removes(self):
        cart = Cart()
        p = self._product()
        cart.add_item(p)
        cart.update_quantity(p.id, 0)
        self.assertTrue(cart.is_empty())

    def test_total(self):
        cart = Cart()
        cart.add_item(self._product(pid=1), 2)
        cart.add_item(self._product(pid=2), 1)
        self.assertAlmostEqual(cart.total, 15.0)

    def test_clear(self):
        cart = Cart()
        cart.add_item(self._product(), 2)
        cart.clear()
        self.assertTrue(cart.is_empty())


class TestOrder(unittest.TestCase):
    def _order(self):
        items = [
            OrderItem(product_id=1, product_name="A", unit_price=10.0, quantity=2),
            OrderItem(product_id=2, product_name="B", unit_price=5.0,  quantity=1),
        ]
        return Order(customer_id=1, customer_name="Bob", shipping_address="123 St", items=items)

    def test_total(self):
        self.assertAlmostEqual(self._order().total, 25.0)

    def test_update_status(self):
        order = self._order()
        order.update_status(OrderStatus.SHIPPED)
        self.assertEqual(order.status, OrderStatus.SHIPPED)

    def test_to_dict_round_trip(self):
        order = self._order()
        order.id = 42
        order2 = Order.from_dict(order.to_dict())
        self.assertEqual(order.id, order2.id)
        self.assertEqual(len(order.items), len(order2.items))


class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self._tmp.close()
        self.db = DatabaseManager(self._tmp.name)

    def tearDown(self):
        os.unlink(self._tmp.name)

    def test_seed_creates_admin(self):
        admin = self.db.get_customer_by_username("admin")
        self.assertIsNotNone(admin)
        self.assertTrue(admin.is_admin)

    def test_seed_creates_products(self):
        products = self.db.list_products()
        self.assertGreater(len(products), 0)

    def test_create_and_get_customer(self):
        c = Customer(username="bob", email="bob@x.com", full_name="Bob Jones")
        c.set_password("pass1234")
        c = self.db.create_customer(c)
        self.assertIsNotNone(c.id)
        fetched = self.db.get_customer_by_id(c.id)
        self.assertEqual(fetched.username, "bob")

    def test_create_and_get_product(self):
        p = Product(name="Test Widget", price=19.99, stock=5, category="Test")
        p = self.db.create_product(p)
        self.assertIsNotNone(p.id)
        fetched = self.db.get_product_by_id(p.id)
        self.assertEqual(fetched.name, "Test Widget")

    def test_update_product(self):
        p = Product(name="Old Name", price=9.99, stock=3, category="Test")
        p = self.db.create_product(p)
        p.name = "New Name"
        p.price = 14.99
        self.db.update_product(p)
        fetched = self.db.get_product_by_id(p.id)
        self.assertEqual(fetched.name, "New Name")
        self.assertAlmostEqual(fetched.price, 14.99)

    def test_delete_product(self):
        p = Product(name="DeleteMe", price=1.0, stock=1, category="Test")
        p = self.db.create_product(p)
        self.db.delete_product(p.id)
        self.assertIsNone(self.db.get_product_by_id(p.id))

    def test_list_categories(self):
        cats = self.db.list_categories()
        self.assertIsInstance(cats, list)
        self.assertGreater(len(cats), 0)

    def test_create_order_reduces_stock(self):
        products = self.db.list_products()
        product = products[0]
        original_stock = product.stock

        customer = self.db.get_customer_by_username("customer1")
        order = Order(
            customer_id=customer.id,
            customer_name=customer.full_name,
            shipping_address="456 Elm St",
            items=[
                OrderItem(
                    product_id=product.id,
                    product_name=product.name,
                    unit_price=product.price,
                    quantity=1,
                )
            ],
        )
        order = self.db.create_order(order)
        self.assertIsNotNone(order.id)

        updated = self.db.get_product_by_id(product.id)
        self.assertEqual(updated.stock, original_stock - 1)

    def test_list_orders_by_customer(self):
        customer = self.db.get_customer_by_username("customer1")
        products = self.db.list_products()
        p = products[0]
        for _ in range(2):
            self.db.create_order(
                Order(
                    customer_id=customer.id,
                    customer_name=customer.full_name,
                    shipping_address="789 Oak Ave",
                    items=[OrderItem(product_id=p.id, product_name=p.name,
                                     unit_price=p.price, quantity=1)],
                )
            )
        orders = self.db.list_orders(customer_id=customer.id)
        self.assertGreaterEqual(len(orders), 2)

    def test_update_order_status(self):
        customer = self.db.get_customer_by_username("customer1")
        products = self.db.list_products()
        p = products[0]
        order = self.db.create_order(
            Order(
                customer_id=customer.id,
                customer_name=customer.full_name,
                shipping_address="1 Main St",
                items=[OrderItem(product_id=p.id, product_name=p.name,
                                 unit_price=p.price, quantity=1)],
            )
        )
        self.db.update_order_status(order.id, OrderStatus.DELIVERED)
        fetched = self.db.get_order_by_id(order.id)
        self.assertEqual(fetched.status, OrderStatus.DELIVERED)


if __name__ == "__main__":
    unittest.main()
