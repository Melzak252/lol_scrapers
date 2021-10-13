from dataclasses import dataclass


@dataclass
class Champion:
    name: str
    description: str
    icon_src: str
    url: str
    tier: str


@dataclass
class TftChampion:
    name: str
    cost: str
