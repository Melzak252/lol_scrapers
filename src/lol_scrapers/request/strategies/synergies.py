from typing import Union, Tuple

from requests_html import HTMLSession, AsyncHTMLSession, HTML

from lol_scrapers.utils import SYNERGY_URL
from lol_scrapers.request.abc import RequestStrategy


class SynergyStrategy(RequestStrategy):
    def request(self, session: HTMLSession) -> Tuple[bool, Union[HTML, None]]:
        resp = session.get(SYNERGY_URL)

        if resp.status_code == 200:
            return True, resp.html

        return False, None

    async def arequest(self, session: AsyncHTMLSession) -> Tuple[bool, Union[HTML, None]]:
        resp = await session.get(SYNERGY_URL)

        if resp.status_code == 200:
            return True, resp.html

        return False, None
