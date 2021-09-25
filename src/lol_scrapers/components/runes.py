from requests_html import HTML, Element


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
    def src2https(src: str):
        return f"https:{src}"
