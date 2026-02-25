"""Miscellaneous helper utilities for the E-commerce Mini-system."""


def format_currency(amount: float, symbol: str = "$") -> str:
    """Format a float as a currency string."""
    return f"{symbol}{amount:,.2f}"


def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text to max_length characters, appending '…' if needed."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 1] + "…"
