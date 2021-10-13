from dataclasses import dataclass
from typing import List

from lol_scrapers.utils.dataclasses.champion import TftChampion


@dataclass
class Trait:
    name: str
    no_champions: int
    description: str
    champions: List[TftChampion]
    values: List[str]
    type: str = ""
