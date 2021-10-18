from typing import Union, Tuple

from requests_html import HTMLSession, AsyncHTMLSession, HTML

from lol_scrapers.utils import ARAM_URL, CHAMPION_URL, NOT_FOUND_URLS
from lol_scrapers.request.abc import RequestStrategy
from lol_scrapers.utils.processor import ChampionNameProcessor


class ChampionStrategy(RequestStrategy):
    def __init__(self, champion: Tuple[str]):
        self.processor = ChampionNameProcessor(champion)

    def request(self, session: HTMLSession) -> Tuple[bool, Union[HTML, None]]:

        isvalid, role, champion_name = self.processor.process()

        if not isvalid:
            return False, None
        if role == "aram":
            role = ""
            resp = session.get(ARAM_URL.format(champion_name, role))
        else:
            resp = session.get(CHAMPION_URL.format(champion_name, role))

        if resp.url in NOT_FOUND_URLS:
            return True, None

        return isvalid, resp.html

    async def arequest(self, session: AsyncHTMLSession) -> Tuple[bool, Union[HTML, None]]:

        isvalid, role, champion_name = self.processor.process()
        if not isvalid:
            return False, None

        if role == "aram":
            role = ""
            resp = await session.get(ARAM_URL.format(champion_name, role))
        else:
            resp = await session.get(CHAMPION_URL.format(champion_name, role))

        if resp.url in NOT_FOUND_URLS:
            return True, None

        return isvalid, resp.html
