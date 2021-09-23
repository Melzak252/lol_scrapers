from abc import abstractmethod
from typing import List, Any

from requests_html import HTML, Element


class StatsScraper:
    @staticmethod
    def get_stats(champion_html: HTML):
        champion_stats_div = champion_html.find(".champion-stats-header")

        roles = champion_stats_div.find(
            "span.champion-stats-header__position__role"
        )

        pick_rates = champion_stats_div.find(
            "span.champion-stats-header__position__rate"
        )

        role_rates = {
            role.text.strip(): pick_rate.text.strip() for role, pick_rate in zip(roles, pick_rates)
        }

        champion_tier = (
            champion_stats_div.find(".champion-stats-header-info__tier", first=True)
            .find("b", first=True)
            .text.strip()
        )

        win_rate = champion_html.find(".champion-stats-trend-rate", first=True).text.strip()
        win_rate_title = champion_html.find(
            ".champion-stats-trend-average", first=True
        ).text.strip()

        return {
            "title": win_rate_title,
            "win_rate": win_rate if win_rate != "%" else None,
            "role_pick_rates": role_rates,
            "champion_tier": champion_tier,
        }

    def get_champion_name(self, champion_html: HTML):

        champion_name_desc = champion_html.find(
            "h1.champion-stats-header-info__name", first=True
        ).text.strip()
        champion_name, *description = champion_name_desc.split(" ")
        description = " ".join(description)

        champion_img = champion_html.find(".champion-stats-header-info__image", first=True).find(
            "img", first=True
        )

        return {
            "name": champion_name.strip(),
            "description": description.strip(),
            "icon_src": self.src2https(champion_img.attrs["src"]),
            "url": champion_html.url,
        }

    @staticmethod
    @abstractmethod
    def src2https(src: str):
        pass


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
    @abstractmethod
    def src2https(src: str):
        pass


class RuneScraper:
    def get_runes(self, champion_html: HTML):
        runes_tables = champion_html.find("table.champion-overview__table--rune", first=True)
        rip = False
        if runes_tables is None:
            rip = True
            return {
                "rip": rip
            }

        runes_title = runes_tables.find(
            ".champion-stats-summary-rune__name", first=True
        )
        runes_stats = runes_tables.find(
            "td.champion-overview__stats.champion-overview__stats--pick", first=True
        )
        runes_table = runes_tables.find("td.champion-overview__data", first=True)

        title = runes_title.text.strip()
        stats = self._format_runes_stats(runes_stats.text)
        active_runes = self._extract_runes_from_table(runes_table)

        return {"title": title, "stats": stats, "runes": active_runes, "rip": rip}

    @staticmethod
    def _format_runes_stats(runes_stats: str):
        _, _, pick_rate, times_picked, _, _, win_rate = runes_stats.strip().split(" ")
        return {
            "pick_rate": pick_rate,
            "times_picked": times_picked,
            "win_rate": win_rate,
        }

    def _get_runes_from_tree_div(self, tree_div: Element):
        runes = tree_div.find(
            ".perk-page__item.perk-page__item--active"
        )
        runes = [
            {"name": img.attrs["alt"], "src": self.src2https(img.attrs["src"])}
            for rune in runes
            for img in rune.find("img")
        ]
        return runes

    def _extract_runes_from_table(self, table: Element):
        main_tree_div, secondary_tree_div = table.find(".perk-page")
        main_rune_div = table.find(
            ".perk-page__item.perk-page__item--keystone.perk-page__item--active", first=True
        )

        main_rune_img = main_rune_div.find("img", first=True)
        main_rune = main_rune_img.attrs["alt"]
        main_rune_src = main_rune_img.attrs["src"]

        main_tree = self._get_runes_from_tree_div(main_tree_div)
        secondary_tree = self._get_runes_from_tree_div(secondary_tree_div)

        return {
            "main_rune": {
                "name": main_rune,
                "src": self.src2https(main_rune_src),
            },
            "main_tree": main_tree,
            "secondary_tree": secondary_tree,
        }

    @staticmethod
    @abstractmethod
    def src2https(src: str):
        pass
