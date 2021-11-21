from dataclasses import dataclass
from typing import List


@dataclass
class Champion:
    name: str
    description: str
    icon_src: str
    url: str
    tier: str
    role: str


@dataclass
class TftChampion:
    name: str
    cost: str
    items: List[str] = None
