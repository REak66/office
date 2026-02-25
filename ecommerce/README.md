# E-Commerce Mini-System

A fully OOP **Python + tkinter** desktop e-commerce application.

## Features

| Module | Highlights |
|---|---|
| **Products** | Scrollable card grid, category filter, live search, stock badges |
| **Cart** | Add/remove items, quantity spinner, real-time total, checkout flow |
| **Orders** | Order history with item detail drilldown |
| **Profile** | View and edit account details |
| **Admin Panel** | Full product CRUD, order status management, customer list |
| **Auth** | Login + Register dialog with SHA-256 password hashing |
| **Persistence** | SQLite database auto-created on first run with demo data |

## OOP Architecture

```
ecommerce/
├── main.py                  # Entry point
├── models/
│   ├── product.py           # Product dataclass
│   ├── customer.py          # Customer dataclass (hashed passwords)
│   ├── cart.py              # Cart + CartItem classes
│   └── order.py             # Order + OrderItem + OrderStatus enum
├── database/
│   └── db_manager.py        # SQLite persistence layer
├── ui/
│   ├── app.py               # EcommerceApp (root Tk window, navigation)
│   ├── theme.py             # Colour palette, fonts, dimensions
│   ├── widgets.py           # Reusable widgets (StyledButton, Card, DataTable, …)
│   ├── login_dialog.py      # Login / Register modal
│   ├── products_view.py     # Products browsing view
│   ├── cart_view.py         # Shopping cart & checkout
│   ├── orders_view.py       # Order history
│   ├── admin_view.py        # Admin panel (products, orders, customers)
│   └── profile_view.py      # User profile editor
├── utils/
│   └── helpers.py           # format_currency, truncate_text
└── tests/
    └── test_ecommerce.py    # 33 unit tests (models + database layer)
```

## Running

```bash
cd ecommerce
python main.py
```

**Default accounts** (auto-created on first run):

| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `admin123` |
| Customer | `customer1` | `pass1234` |

## Running Tests

```bash
cd /path/to/office
python -m unittest discover -s ecommerce/tests -p "test_*.py" -v
```

All **33 tests** cover:
- `Product` – validation, stock management, serialisation
- `Customer` – password hashing, serialisation
- `Cart` – add/remove/update, totals, stock enforcement
- `Order` – total calculation, status transitions, serialisation
- `DatabaseManager` – CRUD, foreign keys, stock reduction on order
