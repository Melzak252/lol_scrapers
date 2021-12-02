import asyncio

from requests_html import HTML

from lol_scrapers import ScrapeStrategy
from lol_scrapers.utils import src2https
from lol_scrapers.utils.dataclasses import TftStats
from lol_scrapers.utils.dataclasses.champion import TftChampion
from lol_scrapers.utils.dataclasses.item import PriorityItem

from lol_scrapers.utils.dataclasses.meta_comp import MetaComp
from lol_scrapers.utils.dataclasses.trait_names import TraitNames


class TftMetaScraper(ScrapeStrategy):
    def scrape(self, meta_html: HTML):
        asyncio.run(meta_html.arender())

        meta_comps = meta_html.find(".deck")

        meta = []
        for comp in meta_comps:
            traits_name = comp.find(".deck__traits__name", first=True)

            main, secondary = self.refactor_traits_name(traits_name)

            champions, important_unit = self.extract_champions(comp)
            components = self.get_components(comp)

            stats = self.get_stats(comp)
            comp = MetaComp(
                main=main,
                secondary=secondary,
                champions=champions,
                important_unit=important_unit,
                components=components,
                stats=stats
            )
            meta.append(
                comp
            )

        return meta

    @staticmethod
    def extract_champions(comp):
        units = comp.find(".unit")
        units_name = [name.text for name in comp.find(".unit__name")]

        champions = []
        important_unit = {
            "name": None,
            "src": None,
        }
        for unit, name in zip(units, units_name):
            unit_cost = unit.attrs["class"][-1][-1]
            unit_items = [item_img.attrs["alt"] for item_img in unit.find(".unit__item__image")]
            unit_stars = True if len(unit.find(".unit__stars", first=True).attrs["class"]) == 1 else False

            if unit_stars:
                important_unit["name"] = name
                unit_img = unit.find(".unit__image>img", first=True).attrs["src"]
                important_unit["src"] = src2https(unit_img)

            champions.append(
                TftChampion(
                    name=name,
                    cost=unit_cost,
                    items=unit_items,
                    stars=unit_stars
                )
            )
        return champions, important_unit

    @staticmethod
    def refactor_traits_name(traits_name):
        main_traits = [name.text for name in traits_name.find("b")]
        secondary = [name.text for name in traits_name.find("span")]

        main = TraitNames(names=main_traits)
        secondary = TraitNames(names=secondary)

        return main, secondary

    @staticmethod
    def get_stats(comp):
        stats = comp.find(".deck__stats", first=True)
        win_rate, top4, avg_placement = [dd.text for dd in stats.find("dd")]
        return TftStats(
            win_rate=win_rate,
            top4=top4,
            avg_placement=avg_placement
        )

    @staticmethod
    def get_components(comp):
        components = []
        for item_element in comp.find(".item-priority__item"):
            print("Here1")
            item_img = item_element.find("img", first=True)
            name = item_img.attrs["alt"]
            src = item_img.attrs["src"]
            count = item_element.text
            components.append(PriorityItem(
                name=name,
                number=count,
                src=src
            ))
        return components
