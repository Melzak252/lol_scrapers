from abc import ABC, abstractmethod
from typing import Union, Tuple

from requests_html import HTML

from lol_scrapers.utils.processor import ChampionNameProcessor


class LolReq(ABC):
    def __init__(self):
        self.processor = ChampionNameProcessor()

    @abstractmethod
    def request_champion_html(self, role: str, champion_name: Union[str, Tuple[str]]):
        pass

    @abstractmethod
    def request_tft_items_html(self) -> HTML:
        pass
