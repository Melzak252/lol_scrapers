import pytest

from lol_scrapers import LOLRequest
from lol_scrapers.opgg import OPGGScraper
from lol_scrapers.lolchess import LOLChessScraper
from lol_scrapers.utils.processor import ChampionNameProcessor


@pytest.fixture(scope="session")
def opgg_scraper():
    return OPGGScraper()


@pytest.fixture(scope="session")
def processor():
    return ChampionNameProcessor()


@pytest.fixture(scope="session")
def lolchess_scraper():
    return LOLChessScraper()


@pytest.fixture(scope="session")
def lol_request():
    return LOLRequest()
