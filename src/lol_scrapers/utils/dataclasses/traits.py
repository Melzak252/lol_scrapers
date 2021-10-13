from dataclasses import dataclass
from typing import List

from lol_scrapers.utils.dataclasses.trait import Trait


@dataclass
class Traits:
    url: str
    traits: List[Trait]
