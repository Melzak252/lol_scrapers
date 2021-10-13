from dataclasses import dataclass, field
from typing import List


@dataclass
class Item:
    name: str
    src: str


@dataclass
class ItemSet:
    items: List[Item]
    win_rate: str
    pick_rate: str
    times_picked: str = field(default="NaN")


@dataclass
class ChampionItems:
    starter: List[ItemSet]
    recommended: List[ItemSet]
    boots: List[ItemSet]
    rip: bool
