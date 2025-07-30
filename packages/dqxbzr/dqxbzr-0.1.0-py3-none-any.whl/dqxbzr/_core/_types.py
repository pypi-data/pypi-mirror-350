from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from ._data import Item, Listing


class PageFetcher(Protocol):
    async def fetch(self, url: str) -> str: ...

    async def refetch(self, reason: str) -> str: ...


class Listings(Protocol):
    @property
    def item(self) -> Item: ...

    async def count(self) -> int: ...

    async def stream(self) -> AsyncIterator[Listing]:
        if False:
            yield
