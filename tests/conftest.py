import pytest
from lol_scrapers.opgg import OPGGScraper
from lol_scrapers.lolchess import LOLChessScraper
from requests_html import HTMLSession


@pytest.fixture(scope="session")
def opgg_scraper():
    return OPGGScraper()


@pytest.fixture(scope="session")
def lolchess_scraper():
    return LOLChessScraper()


@pytest.fixture(scope="session")
def session():
    return HTMLSession()
