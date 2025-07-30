from __future__ import annotations

import re
from functools import cached_property
from typing import TYPE_CHECKING, cast

from lxml import html

from .._data import Item
from ._utils import fetch_with_retry

if TYPE_CHECKING:
    from lxml.html import HtmlElement

    from .._types import PageFetcher


def _extract_id(cell: HtmlElement) -> str:
    urls = cast("list[str]", cell.xpath(".//a/@href"))
    assert len(urls) == 1
    match = re.search(r"/([0-9A-Fa-f]+)/*\s*$", urls[0])
    assert match is not None
    return match[1]


def _extract_name(cell: HtmlElement) -> str:
    texts = cast("list[str]", cell.xpath(".//a/text()"))
    assert len(texts) == 1
    return texts[0].strip()


def _extract_item(row: HtmlElement) -> Item:
    cells = cast("list[HtmlElement]", row.xpath("./td"))
    assert len(cells) == 5
    return Item(
        id=_extract_id(cells[0]),
        name=_extract_name(cells[0]),
    )


def _extract_first_item(content: str) -> Item | None:
    root = html.fromstring(content)
    tables = cast(
        "list[HtmlElement]",
        root.xpath("//table[@class='searchItemTable']"),
    )
    if len(tables) == 0:
        return None
    rows = cast("list[HtmlElement]", tables[0].xpath("./tbody/tr"))
    assert len(rows) > 0
    return _extract_item(rows[0])


class ItemSearchPage:
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
    def first_item(self) -> Item | None:
        return _extract_first_item(self._content)

    @staticmethod
    async def fetch(fetcher: PageFetcher, keyword: str) -> ItemSearchPage:
        url = f"https://hiroba.dqx.jp/sc/search/{keyword}/item/"
        return ItemSearchPage(
            url=url, content=await fetch_with_retry(fetcher, url)
        )
