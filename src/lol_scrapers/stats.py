from requests_html import HTML


class StatsScraper:
    @staticmethod
    def get_stats(champion_html: HTML):
        champion_stats_div = champion_html.find(".champion-stats-header", first=True)

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

    @staticmethod
    def src2https(src: str):
        return f"https:{src}"
