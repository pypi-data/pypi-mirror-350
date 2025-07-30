from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, kw_only=True, slots=True)
class Item:
    id: str
    name: str


@dataclass(frozen=True, kw_only=True, slots=True)
class Listing:
    item_id: str
    item_name: str
    item_quality: int
    item_enhancement: int
    quantity: int
    price: int
    seller_id: str
    seller_name: str
    period_start: date
    period_end: date
