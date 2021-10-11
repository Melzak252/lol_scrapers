__all__ = ["icon", "names", "trait", "traits"]

from requests_html import HTML

from lol_scrapers.lolchess.icon import IconScraper
from lol_scrapers.lolchess.names import TraitNamesScraper
from lol_scrapers.lolchess.trait import TraitScraper
from lol_scrapers.lolchess.traits import TraitsScraper


class LOLChessScraper:

    def __init__(self):
        self._scrapers = {
            "trait": TraitScraper(),
            "traits": TraitsScraper(),
            "icon": IconScraper(),
            "names": TraitNamesScraper(),
        }

    def get_data(self, champion_html: HTML, *args, data_type: str):
        data_type = data_type.lower()

        assert data_type in self._scrapers
        assert isinstance(champion_html, HTML)

        return self._scrapers[data_type].scrape(champion_html, *args)
