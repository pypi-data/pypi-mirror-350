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
    styles = cast("list[str]", cell.xpath("(.//td)[1]/div/@style"))
    assert len(styles) == 1
    match = re.search(r"/([0-9A-Fa-f]+)\.", styles[0])
    assert match is not None
    return match[1]


def _extract_name(cell: HtmlElement) -> str:
    texts = cast("list[str]", cell.xpath("(.//td)[3]/text()"))
    assert len(texts) == 1
    return texts[0].strip()


def _extract_item(content: str) -> Item:
    root = html.fromstring(content)
    tables = cast(
        "list[HtmlElement]",
        root.xpath("//table[contains(@class,'dataTable')]"),
    )
    if len(tables) == 0:
        raise RuntimeError("Invalid content")
    rows = cast("list[HtmlElement]", tables[0].xpath("./tbody/tr[td]"))
    assert len(rows) == 1
    cells = cast("list[HtmlElement]", rows[0].xpath("./td"))
    assert len(cells) == 4
    return Item(
        id=_extract_id(cells[0]),
        name=_extract_name(cells[0]),
    )


class ItemDataPage:
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
    def item(self) -> Item:
        return _extract_item(self._content)

    @staticmethod
    async def fetch(fetcher: PageFetcher, id: str) -> ItemDataPage:
        url = f"https://hiroba.dqx.jp/sc/game/item/{id}/"
        return ItemDataPage(
            url=url, content=await fetch_with_retry(fetcher, url)
        )
