from dataclasses import dataclass
from typing import List, Dict

from lol_scrapers.utils.dataclasses import TftStats
from lol_scrapers.utils.dataclasses.champion import TftChampion
from lol_scrapers.utils.dataclasses.item import PriorityItem
from lol_scrapers.utils.dataclasses.trait_names import TraitNames


@dataclass
class MetaComp:
    main: TraitNames
    secondary: TraitNames
    champions: List[TftChampion]
    important_unit: Dict[str, str]
    components: List[PriorityItem]
    stats: TftStats
