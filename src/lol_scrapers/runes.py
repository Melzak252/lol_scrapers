from requests_html import HTML, Element


class RuneScraper:
    def get_runes(self, champion_html: HTML):
        """Scraps runes data from opgg html page abot given champion.

        We re looking for rune table in html and if there is no tables
        that means champion is rip. If we can find tables we divide table
        for main table, title, statistics like pick rate and win rate.
        From main table we extract active runes

        Parameters
        __________
        champion_html: HTML
            The champion html file with rune data

        Returns
        _______
        dict
            If champion is not rip(There is not enough
            data available to display statistics) returns
            The dictionary with all collected data about most
            played runes on given champion. Like statistics, runes and title.

        Example
        _______
        >>> session = HTMLSession()
        >>> resp = session.get("https://champion_url")
        >>> RuneScraper().get_runes(resp.html)
        {
            "title": "Resolve + Domination,
            "stats": {
                "pick_rate": "20,78%",
                "times_picked": "1353",
                "win_rate": "50,43%",
                },
            "runes": {
               "main_rune": {
                    "name": "Guardian",
                    "src": "https://url_for_main_rune_icon",
                },
                "main_tree": [{
                    "name": "Font of life"
                    "src": "https://url_for_rune_icon"
                    }, {...}, ...],
                "secondary_tree": [{...}, ...]
            },
            "rip": True if champion is rip else False
        }
        """
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
        stats = self._extract_runes_statistics(runes_stats.text)
        active_runes = self._extract_runes_from_table(runes_table)

        return {"title": title, "stats": stats, "runes": active_runes, "rip": rip}

    @staticmethod
    def _extract_runes_statistics(runes_stats: str):
        """Extracts statistics from given runes_statistic merged string

        Parameters
        __________
        runes_stats: str
            Merged string from statistics and unneeded words

        Returns
        _______
        dict
            Dict containing extracted data from string
        """
        _, _, pick_rate, times_picked, _, _, win_rate = runes_stats.strip().split(" ")
        return {
            "pick_rate": pick_rate,
            "times_picked": times_picked,
            "win_rate": win_rate,
        }

    def _get_runes_from_tree_div(self, tree_div: Element):
        """Extracts active runes from div

        Parameters
        __________
        tree_div: Element
            Div containing all active runes from selected tree

        Returns
        _______
        List[dict]
            List of all active runes names and their icon urls
        """
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
        """Extracts all runes from main rune table

        Divides table for two trees and main rune div. For each element we extract
        needed data like names and icons src

        Parameters
        __________
        table: Element
            HTML table containing all active runes

        Returns
        _______
        dict
            Dict with all extracted data like main rune, icons and
            all active runes from first and second tree.
        """
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
    def src2https(src: str):
        """Formats src urls to https type
        """
        return f"https:{src}"
