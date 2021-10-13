from typing import List, Union

from requests_html import HTML, Element

from lol_scrapers.utils.abc.scraper_strategy import ScrapeStrategy
from lol_scrapers.utils.dataclasses.champion import TftChampion
from lol_scrapers.utils.dataclasses.trait import Trait


class TraitScraper(ScrapeStrategy):
    def scrape(self, synergy_html: HTML, *args: str) -> Union[Trait, None]:
        trait_div = synergy_html.find(
            f".guide-synergy-table__synergy.guide-synergy-table__synergy--{''.join(args).lower()}",
            first=True,
        )

        if trait_div is None:
            return None

        trait_values = self._values(
            trait_div
        )

        trait_desc = trait_div.find(
            ".guide-synergy-table__synergy__desc.mb-2", first=True
        ).text.strip()

        trait_name = trait_div.find("span.align-middle", first=True).text.strip()

        champions = self._champions(trait_div)

        return Trait(
            name=trait_name,
            no_champions=len(champions),
            description=trait_desc,
            champions=champions,
            values=trait_values,
        )

    @staticmethod
    def _values(trait_div: Element) -> List[str]:
        trait_values = trait_div.find(
            ".guide-synergy-table__synergy__stats", first=True
        ).text.split("\n")

        trait_values = [value.strip() for value in trait_values]

        return trait_values

    @staticmethod
    def _champions(trait_div: Element) -> List[TftChampion]:
        champions_div = trait_div.find(
            ".guide-synergy-table__synergy__champions.mb-1", first=True
        )

        champions = [
            TftChampion(
                name=champion.find("img", first=True).attrs["alt"],
                cost=champion.find("span.cost", first=True).text
            )
            for champion in champions_div.find("a")
        ]

        return champions
