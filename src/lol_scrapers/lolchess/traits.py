from typing import List, Union

from requests_html import HTML, Element

from lol_scrapers.utils.abc.scraper_strategy import ScrapeStrategy
from lol_scrapers.utils.dataclasses.champion import TftChampion
from lol_scrapers.utils.dataclasses.trait import Trait
from lol_scrapers.utils.dataclasses.traits import Traits


class TraitsScraper(ScrapeStrategy):
    def scrape(self, synergies_html: HTML, *args) -> Traits:
        origin_divs, class_divs = synergies_html.find(".row.row-normal")
        traits = []

        origins = self._synergies(origin_divs, "origin")
        classes = self._synergies(class_divs, "class")

        traits.extend(origins)
        traits.extend(classes)

        return Traits(
            traits=traits,
            url=synergies_html.url
        )

    def _synergies(self, traits_div: Element, trait_type: str) -> List[Trait]:
        traits = []

        traits_div = traits_div.find(".guide-synergy")
        for trait in traits_div:
            trait = self._trait(trait, trait_type)
            if trait is not None:
                traits.append(trait)

        return traits

    def _trait(self, trait: Element, trait_type: str) -> Union[Trait, None]:
        champions = self._champions(trait)

        if len(champions) < 2:
            return None

        trait_name = trait.find("span", first=True).text.strip()

        trait_desc = trait.find(
            ".guide-synergy__description", first=True
        ).text.strip()

        trait_values = trait.find(
            ".guide-synergy__stats", first=True
        ).text.split("/")

        trait_values = [value.strip() for value in trait_values]

        return Trait(
            name=trait_name,
            no_champions=len(champions),
            description=trait_desc,
            champions=champions,
            values=trait_values,
            type=trait_type,
        )

    @staticmethod
    def _champions(trait: Element) -> List[TftChampion]:
        champions_in_trait = trait.find("a.d-inline-block")

        champions = [
            TftChampion(
                name=champion_a_tag.find("span.name", first=True).text.strip(),
                cost=champion_a_tag.find("span.cost", first=True).text.strip(),
            )
            for champion_a_tag in champions_in_trait[:len(champions_in_trait)//2]
        ]
        return champions
