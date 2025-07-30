from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.async_api import Page

    from .._core._types import PageFetcher


class _PageFetcher:
    def __init__(self, *, page: Page) -> None:
        self._page = page
        self._url: str | None = None
        self._refetch_count = 0
        self._refetch_limit = 3

    async def fetch(self, url: str) -> str:
        await self._page.goto(url, wait_until="domcontentloaded")
        content = await self._page.content()
        self._url = url
        self._refetch_count = 0
        return content

    async def refetch(self, reason: str) -> str:
        if self._url is None:
            raise RuntimeError("Page not yet fetched")
        if self._refetch_count > self._refetch_limit:
            raise RuntimeError("Too many refetch attempts")
        await asyncio.sleep(2 ** (self._refetch_count - 1))
        await self._page.reload(wait_until="domcontentloaded")
        content = await self._page.content()
        self._refetch_count += 1
        return content


def page_fetcher(page: Page) -> PageFetcher:
    return _PageFetcher(page=page)
