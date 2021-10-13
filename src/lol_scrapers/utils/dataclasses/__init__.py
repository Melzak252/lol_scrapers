from dataclasses import dataclass


@dataclass
class Stats:
    win_rate: str
    pick_rate: str
    times_picked: str


@dataclass
class RipChamp:
    rip: bool = True
