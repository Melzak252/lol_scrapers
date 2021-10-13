from requests_html import HTML

from lol_scrapers.utils.abc.scraper_strategy import ScrapeStrategy


class LOLChessScraper:
    @staticmethod
    def get_data(champion_html: HTML, scraper: ScrapeStrategy, *args):
        assert isinstance(champion_html, HTML)

        return scraper.scrape(champion_html, *args)
