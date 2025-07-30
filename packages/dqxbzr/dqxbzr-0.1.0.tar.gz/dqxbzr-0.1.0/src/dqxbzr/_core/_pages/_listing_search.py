from __future__ import annotations

import re
from datetime import date
from functools import cached_property
from typing import TYPE_CHECKING, cast

from lxml import html

from .._data import Listing
from ._utils import fetch_with_retry

if TYPE_CHECKING:
    from collections.abc import Iterator, Sequence

    from lxml.html import HtmlElement

    from .._types import PageFetcher


def _extract_item_id(cell: HtmlElement) -> str:
    urls = cast("list[str]", cell.xpath("(./div/p)[1]/a/@href"))
    assert len(urls) == 1
    match = re.search(r"/([0-9A-Fa-f]+)/*\s*$", urls[0])
    assert match is not None
    return match[1]


def _extract_item_name(cell: HtmlElement) -> str:
    texts = cast("list[str]", cell.xpath("(./div/p)[1]/a/text()"))
    assert len(texts) == 1
    return texts[0].strip()


def _extract_item_quality(cell: HtmlElement) -> int:
    texts = cast(
        "list[str]",
        cell.xpath("(./div/p)[2]//span[@class='star']/text()"),
    )
    if len(texts) == 0:
        return 0
    return texts[0].count("★")


def _extract_item_enhancement(cell: HtmlElement) -> int:
    texts = cast("list[str]", cell.xpath("(./div/p)[1]/text()"))
    if len(texts) == 0:
        return 0
    match = re.search(r"\+\s*(\d+)", texts[0])
    assert match is not None
    return int(match[1])


def _extract_quantity(cell: HtmlElement) -> int:
    texts = cast("list[str]", cell.xpath("(./p)[1]/text()"))
    assert len(texts) == 1
    match = re.search(r"(\d+)\s*こ", texts[0])
    assert match is not None
    return int(match[1])


def _extract_price(cell: HtmlElement) -> int:
    texts = cast("list[str]", cell.xpath("(./p)[2]/text()"))
    assert len(texts) == 1
    match = re.search(r"([,0-9]+)\s*G", texts[0])
    assert match is not None
    return int(match[1].replace(",", ""))


def _extract_seller_id(cell: HtmlElement) -> str:
    urls = cast("list[str]", cell.xpath("(./p)[3]/a/@href"))
    assert len(urls) == 1
    match = re.search(r"/(\d+)/*\s*$", urls[0])
    assert match is not None
    return match[1]


def _extract_seller_name(cell: HtmlElement) -> str:
    texts = cast("list[str]", cell.xpath("(./p)[3]/a/text()"))
    assert len(texts) == 1
    return texts[0].strip()


def _extract_period_start(cell: HtmlElement) -> date:
    texts = cast("list[str]", cell.xpath("./text()"))
    assert len(texts) == 1
    match = re.search(r"^\s*(\d{4})/(\d{2})/(\d{2})", texts[0])
    assert match is not None
    return date(int(match[1]), int(match[2]), int(match[3]))


def _extract_period_end(cell: HtmlElement) -> date:
    texts = cast("list[str]", cell.xpath("./text()"))
    assert len(texts) == 1
    match = re.search(r"(\d{4})/(\d{2})/(\d{2})\s*$", texts[0])
    assert match is not None
    return date(int(match[1]), int(match[2]), int(match[3]))


def _extract_listing(row: HtmlElement) -> Listing:
    cells = cast("list[HtmlElement]", row.xpath("./td"))
    assert len(cells) == 3
    return Listing(
        item_id=_extract_item_id(cells[0]),
        item_name=_extract_item_name(cells[0]),
        item_quality=_extract_item_quality(cells[0]),
        item_enhancement=_extract_item_enhancement(cells[0]),
        quantity=_extract_quantity(cells[1]),
        price=_extract_price(cells[1]),
        seller_id=_extract_seller_id(cells[1]),
        seller_name=_extract_seller_name(cells[1]),
        period_start=_extract_period_start(cells[2]),
        period_end=_extract_period_end(cells[2]),
    )


def _extract_listing_count(content: str) -> int:
    root = html.fromstring(content)
    texts = cast(
        "list[str]",
        root.xpath("(//div[@class='searchResult'])[1]/text()"),
    )
    if len(texts) == 0:
        return 0
    match = re.match(r"全\s*(\d+)", texts[0])
    assert match is not None
    return int(match[1])


def _extract_listing_page_count(content: str) -> int:
    root = html.fromstring(content)
    tables = cast(
        "list[HtmlElement]",
        root.xpath("//table[contains(@class,'bazaarTable')]"),
    )
    if len(tables) == 0:
        return 0
    navigators = cast(
        "list[HtmlElement]", root.xpath("//div[@class='pageNavi']")
    )
    if len(navigators) == 0:
        return 1
    numbers = cast(
        "list[str]",
        navigators[0].xpath(".//li[@class='last']/a/@data-pageno"),
    )
    assert len(numbers) == 1
    return 1 + int(numbers[0])


def _extract_listings(content: str) -> Iterator[Listing]:
    root = html.fromstring(content)
    tables = cast(
        "list[HtmlElement]",
        root.xpath("//table[contains(@class,'bazaarTable')]"),
    )
    if len(tables) == 0:
        return
    for row in cast("list[HtmlElement]", tables[0].xpath("./tbody/tr[td]")):
        yield _extract_listing(row)


class ListingSearchPage:
    def __init__(self, *, url: str, content: str) -> None:
        self._url = url
        self._content = content

    @property
    def url(self) -> str:
        return self._url

    @property
    def content(self) -> str:
        return self._content

    @cached_property
    def listing_count(self) -> int:
        return _extract_listing_count(self._content)

    @cached_property
    def page_count(self) -> int:
        return _extract_listing_page_count(self._content)

    @cached_property
    def listings(self) -> Sequence[Listing]:
        return tuple(_extract_listings(self._content))

    @staticmethod
    async def fetch(
        fetcher: PageFetcher, id: str, page: int
    ) -> ListingSearchPage:
        url = f"https://hiroba.dqx.jp/sc/search/bazaar/{id}/0/page/{page}"
        return ListingSearchPage(
            url=url,
            content=await fetch_with_retry(fetcher, url),
        )
