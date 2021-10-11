from requests_html import HTML

from lol_scrapers.opgg.items import ItemScraper
from lol_scrapers.opgg.runes import RuneScraper
from lol_scrapers.opgg.stats import StatsScraper
from lol_scrapers.opgg.name import NameScraper


class OPGGScraper:
    """This unites all subscrapers from champion opgg HTML object

    Attributes
    ----------
    _scrapers: dict
        Dict of all data types and Scrapers to get
    """

    def __init__(self):
        self._scrapers = {
            "items": ItemScraper(),
            "runes": RuneScraper(),
            "stats": StatsScraper(),
            "name": NameScraper(),
        }

    def get_data(self, champion_html: HTML, *args, data_type: str):
        data_type = data_type.lower()

        assert data_type in self._scrapers
        assert isinstance(champion_html, HTML)

        return self._scrapers[data_type].scrape(champion_html, *args)
