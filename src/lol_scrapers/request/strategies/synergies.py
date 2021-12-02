from lol_scrapers.utils import SYNERGY_URL
from lol_scrapers.request.abc import TftRequestStrategy


class SynergyStrategy(TftRequestStrategy):
    url = SYNERGY_URL
