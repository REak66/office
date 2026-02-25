"""Entry point for the E-commerce Mini-System."""

import sys
import os

# Ensure the project root is on the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ecommerce.ui.app import EcommerceApp


def main():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ecommerce.db")
    app = EcommerceApp(db_path=db_path)
    app.mainloop()


if __name__ == "__main__":
    main()
