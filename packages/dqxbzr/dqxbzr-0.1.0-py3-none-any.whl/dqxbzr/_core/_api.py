from __future__ import annotations

from typing import TYPE_CHECKING

from ._data import Item, Listing
from ._pages import ItemDataPage, ItemSearchPage, ListingSearchPage
from ._types import Listings, PageFetcher

if TYPE_CHECKING:
    from collections.abc import AsyncIterator


class _Listings:
    def __init__(self, *, fetcher: PageFetcher, item: Item) -> None:
        self._fetcher = fetcher
        self._item = item

    @property
    def item(self) -> Item:
        return self._item

    async def count(self) -> int:
        page = await ListingSearchPage.fetch(self._fetcher, self._item.id, 0)
        return page.listing_count

    async def stream(self) -> AsyncIterator[Listing]:
        item_id = self._item.id
        page = await ListingSearchPage.fetch(self._fetcher, item_id, 0)
        for i in range(page.page_count):
            if i > 0:
                page = await ListingSearchPage.fetch(self._fetcher, item_id, i)
            for listing in page.listings:
                yield listing


async def listings(fetcher: PageFetcher, item: str) -> Listings:
    if len(item) >= 10:
        data_page = await ItemDataPage.fetch(fetcher, item)
        return _Listings(fetcher=fetcher, item=data_page.item)
    search_page = await ItemSearchPage.fetch(fetcher, item)
    first_item = search_page.first_item
    if first_item is None or first_item.name != item:
        raise RuntimeError(f"Invalid item name: '{item}'")
    return _Listings(fetcher=fetcher, item=first_item)
