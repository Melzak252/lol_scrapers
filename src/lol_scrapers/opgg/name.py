from requests_html import HTML

from lol_scrapers.utils import src2https
from lol_scrapers.utils.dataclasses.champion import Champion
from lol_scrapers.utils.abc.scraper_strategy import ScrapeStrategy


class ChampionScraper(ScrapeStrategy):

    def scrape(self, champion_html: HTML):
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

           {
                'name': 'Rakan',
                'description': 'Build for Support',
                'icon_src': 'https://opgg-static.akamaized.net/images/lol/champion/Rakan.png?image=c_scale,q_auto,w_140&v=1632277051',
                'url': 'https://url_to_champion_opgg_site'
            }
        """
        champion_html = champion_html.find(".l-champion-statistics-header", first=True)
        champion_name_desc = champion_html.find(
            "h1.champion-stats-header-info__name", first=True
        ).text.strip()
        champion_name, *description = champion_name_desc.split(" ")
        description = " ".join(description)

        champion_tier = champion_html.find(".champion-stats-header-info__tier", first=True).find(
            "b",
            first=True
        )

        if champion_tier is not None:
            champion_tier = champion_tier.text.strip()

        champion_img = champion_html.find(".champion-stats-header-info__image", first=True).find(
            "img", first=True
        )

        champion = Champion(
            champion_name.strip(),
            description.strip(),
            src2https(champion_img.attrs["src"]),
            champion_html.url,
            champion_tier
        )
        return champion
