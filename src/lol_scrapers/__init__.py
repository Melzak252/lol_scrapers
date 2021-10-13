from requests_html import HTML

from lol_scrapers.utils.abc.scraper_strategy import ScrapeStrategy


class LOLScraper:
    """This class spouse to unite the scrape strategies"""

    @staticmethod
    def get_data(champion_html: HTML, scraper: ScrapeStrategy, *args):
        assert isinstance(champion_html, HTML)

        return scraper.scrape(champion_html, *args)
