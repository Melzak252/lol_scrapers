import pytest

from lol_scrapers import LOLScraper
from lol_scrapers.request import LolRequest
from lol_scrapers.utils.processor import ChampionNameProcessor


@pytest.fixture(scope="session")
def processor():
    return ChampionNameProcessor()


@pytest.fixture(scope="session")
def scraper():
    return LOLScraper()


@pytest.fixture(scope="session")
def lol_request():
    return LolRequest()
