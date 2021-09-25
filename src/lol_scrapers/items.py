from typing import List, Any

from requests_html import Element, HTML


class ItemScraper:

    def get_items(self, champion_html: HTML):

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
                data = self._prepare_data(items, win_rate, pick_rate, imgs_src)
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
        starter1, starter2, *recommended, boots1, boots2, boots3 = all_items
        return (starter1, starter2), tuple(recommended), (boots1, boots2, boots3)

    def _prepare_data(
            self, items: List[str], win_rate: Element, pick_rate: Element, imgs_src: List[str]):
        win_rate = win_rate.text.strip()
        pick_rate, times_picked = pick_rate.text.strip().split(" ")

        formated_items = [
            {"name": item, "src": self.src2https(src)}
            for item, src in zip(items, imgs_src)
        ]

        data = {
            "win_rate": win_rate,
            "pick_rate": pick_rate,
            "times_picked": times_picked,
            "items": formated_items,
        }

        return data

    @staticmethod
    def src2https(src: str):
        return f"https:{src}"
