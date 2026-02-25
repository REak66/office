"""E-commerce Mini-System – top-level package."""

__all__ = ["EcommerceApp"]


def __getattr__(name):
    if name == "EcommerceApp":
        from .ui.app import EcommerceApp  # noqa: PLC0415
        return EcommerceApp
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
