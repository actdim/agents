"""API package exports."""

try:
    from .router import api_router
    __all__ = ["api_router"]
except ImportError:
    __all__ = []

