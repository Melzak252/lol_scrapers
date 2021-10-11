from requests_html import HTML, Element


class TraitsScraper:
    def scrape(self, synergies_html: HTML):
        """Scraps all traits data lolchess html page abot given champion.

        We re looking for two divs fitst about origins, second about classes.
        Then we re extracting all trats data from div.

        Parameters
        __________
        synergies_html: HTML
            The synergies HTML object with all traits

        Returns
        _______
        dict
            Dict with all collected data about traits

            {
                'url': 'https://synergies_url',
                "traits": [
                    {
                        "type": "class",
                        "name": "Legionare,
                        "no_champions": 4,
                        "description": "Champions got buffed...",
                        "champions": [
                            {"name": "Kalista", "cost": "$1"},
                            ...
                        ],
                        "values": ["(3) Buff", ...],
                    },
                    ...
                ]
            }
        """
        origin_divs, class_divs = synergies_html.find(".row.row-normal")
        traits = []
        origins = self._get_traits_from_div(origin_divs, "origin")
        classes = self._get_traits_from_div(class_divs, "class")
        traits.extend(origins)
        traits.extend(classes)

        return {"traits": traits, "url": synergies_html.url}

    @staticmethod
    def _get_traits_from_div(traits_div: Element, trait_type: str):
        traits = []
        traits_div = traits_div.find(".guide-synergy")
        for trait in traits_div:
            champions_in_trait = trait.find("a.d-inline-block")
            no_champions = len(champions_in_trait) // 2
            if no_champions > 1:
                trait_name = trait.find("span", first=True).text.strip()

                champions = [
                    {
                        "name": champion_a_tag.find(
                            "span.name", first=True
                        ).text.strip(),
                        "cost": champion_a_tag.find(
                            "span.cost", first=True
                        ).text.strip(),
                    }
                    for champion_a_tag in champions_in_trait[:no_champions]
                ]

                trait_desc = trait.find(
                    ".guide-synergy__description", first=True
                ).text.strip()
                trait_values = trait.find(
                    ".guide-synergy__stats", first=True
                ).text.split("/")
                trait_values = [value.strip() for value in trait_values]

                data = {
                    "type": trait_type,
                    "name": trait_name,
                    "no_champions": no_champions,
                    "description": trait_desc,
                    "champions": champions,
                    "values": trait_values,
                }
                traits.append(data)
        return traits
