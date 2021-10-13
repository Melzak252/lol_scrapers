from typing import List, Union

from requests_html import Element, HTML

from lol_scrapers.utils import src2https
from lol_scrapers.utils.dataclasses.item import Item, ItemSet, ChampionItems
from lol_scrapers.utils.abc.scraper_strategy import ScrapeStrategy
from lol_scrapers.utils.dataclasses import RipChamp


class ItemScraper(ScrapeStrategy):

    def scrape(self, champion_html: HTML, *args) -> Union[ChampionItems, RipChamp]:
        items_table = champion_html.find("table.champion-overview__table")

        if not items_table:
            return RipChamp()

        # separate table with main item sets
        items_table = items_table[1]

        # scrape all rows from table
        items_rows = items_table.find("tr")

        item_sets: List[ItemSet] = []
        for items in items_rows:

            # scrapes win rate for current item set
            pick_rate = items.find(
                "td.champion-overview__stats.champion-overview__stats--pick.champion-overview__border",
                first=True
            )

            # scrapes win rate for current item set
            win_rate = items.find(
                "td.champion-overview__stats.champion-overview__stats--win.champion-overview__border",
                first=True
            )

            # scrapes all items Elements
            items = items.find("li.champion-stats__list__item.tip")

            # scrapes all img src
            imgs_src = [item.find("img", first=True).attrs["src"] for item in items]

            # saves only items names
            items = [
                HTML(html=item.attrs["title"]).find("b", first=True).text
                for item in items
            ]

            # checks if there are saved items
            if items:
                item_set = self._item_set(items, win_rate, pick_rate, imgs_src)
                item_sets.append(item_set)

        return ChampionItems(
            item_sets[:2],
            item_sets[2:-3],
            item_sets[-3:],
            False
        )

    @staticmethod
    def _item_set(items_names: List[str], win_rate: Element, pick_rate: Element, imgs_src: List[str]):
        # prepares statistics
        win_rate = win_rate.text.strip()
        pick_rate, times_picked = pick_rate.text.strip().split(" ")

        # creates list of item objects
        items = [
            Item(name, src2https(src))
            for name, src in zip(items_names, imgs_src)
        ]

        item_set = ItemSet(
            items=items,
            win_rate=win_rate,
            pick_rate=pick_rate,
            times_picked=times_picked
        )

        return item_set
