from lol_scrapers.utils import META_URL
from lol_scrapers.request.abc import TftRequestStrategy


class TftMetaStrategy(TftRequestStrategy):
    url = META_URL
