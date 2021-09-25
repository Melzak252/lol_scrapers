from typing import Union, Tuple

from unidecode import unidecode

from lol_scrapers.items import ItemScraper
from lol_scrapers.runes import RuneScraper
from lol_scrapers.stats import StatsScraper
from lol_scrapers.name import NameScraper


class OPGGScraper:
    not_found_urls = [
        "https://eune.op.gg/champion/statistics",
        "https://eune.op.gg/aram/statistics",
    ]

    champion_url = "https://eune.op.gg/champion/{}/statistics/{}"
    aram_url = "https://eune.op.gg/aram/{}/statistics/{}"

    def __init__(self):
        self.items = ItemScraper()
        self.runes = RuneScraper()
        self.stats = StatsScraper()
        self.name = NameScraper()

    @staticmethod
    def refactor_champ_name(champ_name: Union[Tuple[str], str]) -> str:
        if isinstance(champ_name, tuple):
            champ_name = "".join(champ_name)

        champ_name = unidecode(champ_name)
        champ_name = champ_name.replace(" ", "").replace("'", "").replace(".", "").replace(",", "").lower()
        if champ_name.lower().startswith("nunu"):
            champ_name = "nunu"

        if champ_name == "wukong":
            champ_name = "monkeyking"

        return champ_name
