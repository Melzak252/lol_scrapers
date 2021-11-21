from lol_scrapers.utils import ITEMS_URL
from lol_scrapers.request.abc import TftRequestStrategy


class TftItemsStrategy(TftRequestStrategy):
    url = ITEMS_URL
