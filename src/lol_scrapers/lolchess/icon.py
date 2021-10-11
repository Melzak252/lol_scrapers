from typing import Dict, Union

from requests_html import HTML

from lol_scrapers.utils import src2https


class IconScraper:
    def scrape(self, resp_icon: HTML, trait_name: str) -> Dict[str, Union[str, None]]:
        *_, table = resp_icon.find("table.guide-items-table")

        images = table.find("img")

        emblem = f"{trait_name.title()} Emblem"
        trait_icon = [img.attrs["src"] for img in images if img.attrs["alt"] == emblem]

        if not trait_icon:
            return {"src": None}

        return {"src": src2https(trait_icon[0]) if trait_icon else ""}
