from requests_html import HTML

from lol_scrapers.utils.abc.scraper_strategy import ScrapeStrategy
from lol_scrapers.lolchess.trait import TraitScraper
from lol_scrapers.lolchess.icon import IconScraper
from lol_scrapers.lolchess.names import TraitNamesScraper
from lol_scrapers.lolchess.traits import TraitsScraper


class LOLChessScraper:
    @staticmethod
    def get_data(champion_html: HTML, scraper: ScrapeStrategy, *args):
        assert isinstance(champion_html, HTML)

        return scraper.scrape(champion_html, *args)
