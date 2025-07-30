from __future__ import annotations

from typing import TYPE_CHECKING, cast

from lxml import html

if TYPE_CHECKING:
    from lxml.html import HtmlElement

    from .._types import PageFetcher


def _extract_error(content: str) -> str | None:
    root = html.fromstring(content)
    tables = cast(
        "list[HtmlElement]",
        root.xpath("//div[@class='errorBox']//table"),
    )
    if len(tables) == 0:
        return None
    rows = cast("list[HtmlElement]", tables[0].xpath("./tbody/tr"))
    assert len(rows) == 1
    return rows[0].text_content().strip()


async def fetch_with_retry(fetcher: PageFetcher, url: str) -> str:
    content = await fetcher.fetch(url)
    while True:
        reason = _extract_error(content)
        if reason is None:
            return content
        content = await fetcher.refetch(reason)
