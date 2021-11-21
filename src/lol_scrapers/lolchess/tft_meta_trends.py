from typing import Union

from requests_html import HTML

from lol_scrapers import ScrapeStrategy
from lol_scrapers.utils.dataclasses.meta import MetaList, Deck


class TftMetaScraper(ScrapeStrategy):
    def __init__(self, sortby: str = None):
        self.sortby = sortby

    def scrape(self, synergy_html: HTML) -> Union[MetaList, None]:
        win_rate = ""
        top4 = ""
        average_place = ""

        return MetaList(
            decks=[],
            win_rate=win_rate,
            top4=top4,
            average_place=average_place,
            item_priority=[]
        )
