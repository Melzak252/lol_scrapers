
from lol_scrapers.items import ItemScraper
from lol_scrapers.runes import RuneScraper
from lol_scrapers.stats import StatsScraper
from lol_scrapers.name import NameScraper


class OPGGScraper:
    """This unites all subscrapers from champion opgg HTML object

    Attributes
    ----------
    items : ItemScraper
        Scraper to extracting all item data from HTML object
    runes : RuneScraper
        Scraper to extracting all runes data from HTML object
    stats : StatsScraper
        Scraper to extracting statistics about champion from HTML object
    name : NameScraper
        Scraper to extracting champion name and basic statistics from HTML object
    """

    def __init__(self):
        self.items = ItemScraper()
        self.runes = RuneScraper()
        self.stats = StatsScraper()
        self.name = NameScraper()
