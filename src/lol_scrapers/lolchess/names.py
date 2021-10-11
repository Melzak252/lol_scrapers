from typing import Dict, List

from requests_html import HTML


class TraitNamesScraper:
    def scrape(self, synergies_html: HTML) -> Dict[str, List[str]]:
        """Scraps all traits name from synergies_html

        Parameter
        _________
        synergies_html: HTML
            Synergies HTML object with all traits

        Returns
        _______
        dict
            Dict containing list of all traits names
        """
        traits_div = synergies_html.find(".guide-synergy__header.clearfix")
        traits = []
        for trait in traits_div:
            champions_in_trait = trait.find("a")
            if len(champions_in_trait) > 1:
                trait_name = trait.find("span", first=True).text.strip()
                traits.append(trait_name)

        return {
            "traits": traits,
        }
