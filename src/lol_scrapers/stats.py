from requests_html import HTML


class StatsScraper:
    @staticmethod
    def get_stats(champion_html: HTML):
        """Scraps general statistics data from opgg html page abot given champion.

        We re looking for roles played on this champion in header of champion page and
        table with general win rate and if there is no table
        that means champion is rip. If we can find table
        we extract win rate and win rate title

        Parameters
        __________
        champion_html: HTML
            The champion html file with champion statistics

        Returns
        _______
        dict
            If champion is not rip(There is not enough
            data available to display statistics) returns
            The dictionary with all collected data about most
            played roles, general win rate, champion tier.

        Example
        _______
        >>> session = HTMLSession()
        >>> resp = session.get("https://champion_url")
        >>> StatsScraper().get_stats(resp.html)
        {
            "title": "Support Rakan Win Rate",
            "win_rate": "50,75%" if win_rate != "%" else None,
            "role_pick_rates": {
                'Support': '100%'
                },
            "champion_tier": "Tier 3",
        }
        """

        champion_stats_div = champion_html.find(".champion-stats-header", first=True)
        rip = False
        if champion_stats_div is None:
            rip = True
            return {
                "rip": rip
            }
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
            "rip": rip
        }

    @staticmethod
    def src2https(src: str):
        """Formats src urls to https type
        """
        return f"https:{src}"
