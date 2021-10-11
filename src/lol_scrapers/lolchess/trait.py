from typing import Tuple, List, Dict

from requests_html import HTML, Element


class TraitScraper:
    def scrape(self, synergy_html: HTML, trait_name: str):
        trait_div = synergy_html.find(
            f".guide-synergy-table__synergy.guide-synergy-table__synergy--{trait_name.lower()}",
            first=True,
        )
        if trait_div is None:
            return {}

        trait_name, champions, trait_desc, trait_values = self._get_trait_data(
            trait_div
        )

        data = {
            "name": trait_name,
            "no_champions": len(champions),
            "description": trait_desc,
            "champions": champions,
            "values": trait_values,
        }
        return data

    @staticmethod
    def _get_trait_data(trait_div: Element) -> Tuple[str, List[Dict[str, str]], str, List[str]]:
        trait_name = trait_div.find("span.align-middle", first=True).text.strip()

        champions_div = trait_div.find(
            ".guide-synergy-table__synergy__champions.mb-1", first=True
        )
        champions = [
            {
                "name": champion.find("img", first=True).attrs["alt"],
                "cost": champion.find("span.cost", first=True).text,
            }
            for champion in champions_div.find("a")
        ]
        trait_desc = trait_div.find(
            ".guide-synergy-table__synergy__desc.mb-2", first=True
        ).text.strip()
        trait_values = trait_div.find(
            ".guide-synergy-table__synergy__stats", first=True
        ).text.split("\n")
        trait_values = [value.strip() for value in trait_values]

        return trait_name, champions, trait_desc, trait_values
