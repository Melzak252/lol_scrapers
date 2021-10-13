from typing import Union, Tuple

from requests_html import HTMLSession, AsyncHTMLSession, HTML

from lol_scrapers.utils import ITEMS_URL
from lol_scrapers.request.abc import RequestStrategy


class TftItemsStrategy(RequestStrategy):
    def request(self, session: HTMLSession) -> Tuple[bool, Union[HTML, None]]:
        """Requests for lolchess items site and returns HTML object

        Returns
        _______
        HTML
           HTML object with items data
        """
        resp = session.get(ITEMS_URL)

        if resp.status_code == 200:
            return True, resp.html

        return False, None

    async def arequest(self, session: AsyncHTMLSession) -> Tuple[bool, Union[HTML, None]]:
        """Async requests for lolchess items site and returns HTML object

        Return
        ______
        HTML
           HTML object with items data
        """
        resp = await session.get(ITEMS_URL)

        if resp.status_code == 200:
            return True, resp.html

        return False, None
