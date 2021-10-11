from typing import List, Any

from requests_html import Element, HTML

from lol_scrapers.utils import src2https


class ItemScraper:

    def scrape(self, champion_html: HTML):
        """Scraps item data from opgg html page abot given champion.

        We re looking for item table in html and if there is no tables
        that means champion is rip. If we can find tables we divide table
        for rows with items. Each row we separate for win rate, pick rate
        and items in row. After get all data we separate them on 3 categories
        starter items, recommended builds and boots.

        Parameters
        __________
        champion_html: HTML
            The champion html file with items data

        Returns
        _______
        dict
            If champion is not rip(There is not enough
            data available to display statistics) returns
            The dictionary with all collected data about most
            played items on given champion. Like boots, starter items
            and recommended build.
            {
                "starter_items": [{
                    "win_rate": "50.74%",
                    "pick_rate": "24.56%",
                    "times_picked": "1765",
                    "items": [{
                        "name": "Shurelia's Battlesong"
                        "src": "https://url_to_item_icon"
                        }, {...}, ...],
                    }, {...}, {...}],
                "recommended_builds": [{...}, ...],
                "boots": [{...}, ...],
                "rip": True if champion is rip else False
            }
        """

        items_table = champion_html.find("table.champion-overview__table")

        rip = False

        if not items_table:
            rip = True
            return {
                "rip": rip
            }

        items_table = items_table[1]
        items_rows = items_table.find("tr")

        all_items = []
        for items in items_rows:
            pick_rate = items.find(
                "td.champion-overview__stats.champion-overview__stats--pick.champion-overview__border",
                first=True
            )

            win_rate = items.find(
                "td.champion-overview__stats.champion-overview__stats--win.champion-overview__border",
                first=True
            )

            items = items.find("li.champion-stats__list__item.tip")

            imgs_src = [item.find("img", first=True).attrs["src"] for item in items]

            items = [
                HTML(html=item.attrs["title"]).find("b", first=True).text
                for item in items
            ]

            if items:
                data = self._prepare_items_set(items, win_rate, pick_rate, imgs_src)
                all_items.append(data)

        starter_items, recommended_builds, boots = self._group_items_to_categories(
            all_items
        )

        return {
            "starter_items": starter_items,
            "recommended_builds": recommended_builds,
            "boots": boots,
            "rip": rip,
        }

    @staticmethod
    def _group_items_to_categories(all_items: List[Any]):
        """Groups all items rows to 3 tuples representing 3 categories.

        Parameters
        __________

        all_items: List[List[Dict[str, str]]]
            List of items for each row.

        Returns
        _______

        Tuple[Tuple[Dict[str, str]]
            Tuple containing tuple for each 3 categories(starter items, recommended builds, boots)
        """

        starter1, starter2, *recommended, boots1, boots2, boots3 = all_items
        return (starter1, starter2), tuple(recommended), (boots1, boots2, boots3)

    def _prepare_items_set(
            self, items: List[str], win_rate: Element, pick_rate: Element, imgs_src: List[str]):
        """Prepares dict with information about item set from collected data

        Parameters
        __________
        items: List[str]
            List of items names in table row
        win_rate: Element
            HTML fragment containing item set win rate
        pick_rate: Element
            HTML fragment containing item set pick rate
        img_src: List[str]
            List of src for each item in item list

        Returns
        _______
        dict
            Dict of extracted data from parameters and restructured to
            well arranged dictionary
        """

        win_rate = win_rate.text.strip()
        pick_rate, times_picked = pick_rate.text.strip().split(" ")

        formated_items = [
            {"name": item, "src": src2https(src)}
            for item, src in zip(items, imgs_src)
        ]

        data = {
            "win_rate": win_rate,
            "pick_rate": pick_rate,
            "times_picked": times_picked,
            "items": formated_items,
        }

        return data
