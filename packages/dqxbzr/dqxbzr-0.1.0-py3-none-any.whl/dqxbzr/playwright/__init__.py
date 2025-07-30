try:
    import playwright as _playwright  # noqa: F401
except ImportError as err:
    raise ImportError("Missing optional dependency 'playwright'") from err

from ._page_fetcher import page_fetcher

__all__ = ("page_fetcher",)
