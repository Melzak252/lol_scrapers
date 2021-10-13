from dataclasses import dataclass
from typing import List

from lol_scrapers.utils.dataclasses import Stats


@dataclass
class RuneName:
    name: str
    src: str


@dataclass
class Runes:
    main_rune: RuneName
    main_tree: List[RuneName]
    secondary_tree: List[RuneName]


@dataclass
class RuneSet:
    title: str
    stats: Stats
    runes: Runes
    rip: bool
