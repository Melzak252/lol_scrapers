from requests_html import HTML

from lol_scrapers.opgg.items import ItemScraper
from lol_scrapers.opgg.runes import RuneScraper
from lol_scrapers.opgg.stats import StatsScraper
from lol_scrapers.opgg.name import ChampionScraper
from lol_scrapers.utils.abc.scraper_strategy import ScrapeStrategy


class OPGGScraper:
    """Unites all subscrapers from champion opgg HTML object"""

    def get_data(self, champion_html: HTML, scraper: ScrapeStrategy, *args):
        assert isinstance(champion_html, HTML)

        return scraper.scrape(champion_html, *args)
