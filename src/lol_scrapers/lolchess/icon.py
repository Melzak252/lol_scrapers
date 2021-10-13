from requests_html import HTML

from lol_scrapers.utils import src2https
from lol_scrapers.utils.abc.scraper_strategy import ScrapeStrategy
from lol_scrapers.utils.dataclasses.icon import Icon


class IconScraper(ScrapeStrategy):
    def scrape(self, html: HTML, *args: str) -> Icon:
        *_, table = html.find("table.guide-items-table")

        images = table.find("img")

        emblem = f"{''.join(args).title()} Emblem"
        trait_icon = [img.attrs["src"] for img in images if img.attrs["alt"] == emblem]

        if not trait_icon:
            return Icon()

        icon_src = src2https(trait_icon[0]) if trait_icon else ""
        return Icon(
            name=emblem,
            src=icon_src
        )
