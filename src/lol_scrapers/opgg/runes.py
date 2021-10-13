from requests_html import HTML, Element

from lol_scrapers.utils import src2https
from lol_scrapers.utils.dataclasses import RipChamp, Stats
from lol_scrapers.utils.dataclasses.runes import RuneSet, Runes, RuneName
from lol_scrapers.utils.abc.scraper_strategy import ScrapeStrategy


class RuneScraper(ScrapeStrategy):
    def scrape(self, champion_html: HTML, *args):
        runes_tables = champion_html.find("table.champion-overview__table--rune", first=True)
        if runes_tables is None:
            return RipChamp()

        # scrapes runes title
        runes_title = runes_tables.find(
            ".champion-stats-summary-rune__name", first=True
        )

        # scrapes Element with statistics
        runes_stats = runes_tables.find(
            "td.champion-overview__stats.champion-overview__stats--pick", first=True
        )

        # scrapes table with runes
        runes_table = runes_tables.find("td.champion-overview__data", first=True)

        title = runes_title.text.strip()
        stats = self._extract_stats(runes_stats.text)
        active_runes = self._scrape_table(runes_table)

        return RuneSet(
            title=title,
            stats=stats,
            runes=active_runes,
            rip=False
        )

    @staticmethod
    def _extract_stats(runes_stats: str):
        _, _, pick_rate, times_picked, _, _, win_rate = runes_stats.strip().split(" ")
        return Stats(win_rate, pick_rate, times_picked)

    @staticmethod
    def _scrape_tree(tree_div: Element):
        runes = tree_div.find(
            ".perk-page__item.perk-page__item--active"
        )
        runes = [
            RuneName(img.attrs["alt"], src2https(img.attrs["src"]))
            for rune in runes
            for img in rune.find("img")
        ]
        return runes

    def _scrape_table(self, table: Element):
        main_tree_div, secondary_tree_div = table.find(".perk-page")
        main_rune_div = table.find(
            ".perk-page__item.perk-page__item--keystone.perk-page__item--active", first=True
        )

        main_rune_img = main_rune_div.find("img", first=True)

        main_rune = main_rune_img.attrs["alt"]
        main_rune_src = main_rune_img.attrs["src"]
        rune_name = RuneName(main_rune, src2https(main_rune_src))

        main_tree = self._scrape_tree(main_tree_div)
        secondary_tree = self._scrape_tree(secondary_tree_div)

        return  Runes(rune_name, main_tree, secondary_tree)
