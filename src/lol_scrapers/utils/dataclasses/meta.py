from dataclasses import dataclass
from typing import List

from lol_scrapers.utils.dataclasses.champion import TftChampion
from lol_scrapers.utils.dataclasses.item import PriorityItem


@dataclass
class Deck:
    champions: List[TftChampion]
    items_priority: List[PriorityItem]


@dataclass
class MetaList:
    decks: List[Deck]
    win_rate: str
    top4: str
    average_place: str
    item_priority: List[PriorityItem]

