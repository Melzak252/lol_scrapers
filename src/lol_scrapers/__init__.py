from typing import Union, Tuple

from requests_html import HTMLSession, AsyncHTMLSession, HTML

from lol_scrapers.utils import ITEMS_URL, SYNERGY_URL, ARAM_URL, CHAMPION_URL, NOT_FOUND_URLS
from lol_scrapers.utils.abc import lol_req


class AsyncLOLRequest(lol_req.LolReq):
    def __init__(self):
        super().__init__()
        self.session = AsyncHTMLSession()

    async def request_champion_html(self, role: str, champion_name: Union[str, Tuple[str]]):
        """Refactors given role and champion_name to send async request for champion HTML object

        Method checks first that role and champion_name are correctly typed.
        If role and champion_name are not valid method will return False and None.
        Then refactors champion name to acceptable for opgg site. Then sends
        request to site if request was not redirected to NOT_FOUND_URLS then
        It will return None instead HTML object.

        Parameters
        __________
        role: str
            Contains role name or champion name first token
        champion_name: Union[str, tuple[str]]
            Contains tuple of champion name tokens or str with name

        Returns
        _______
        bool
            If given data are correct returns True else False
        Union[HTML, None]
            If cannot get HTML object returns None else HTML object
        Union[HTML, None]
            If data is correct then return role else None
        """

        isvalid, role, champion_name = self.processor.process(role, champion_name)
        if not isvalid:
            return False, None, role

        if role == "aram":
            role = ""
            resp = await self.session.get(ARAM_URL.format(champion_name, role))
        else:
            resp = await self.session.get(CHAMPION_URL.format(champion_name, role))

        if resp.url in NOT_FOUND_URLS:
            return True, None, role

        return isvalid, resp.html, role

    async def request_tft_synergies_html(self) -> HTML:
        """Async requests for lolchess synergies site and returns HTML object

        Return
        ______
        HTML
            HTML object with all traits data
        """
        resp = await self.session.get(SYNERGY_URL)

        return resp.html

    async def request_tft_items_html(self) -> HTML:
        """Async requests for lolchess items site and returns HTML object

        Return
        ______
        HTML
            HTML object with items data
        """
        resp = await self.session.get(ITEMS_URL)

        return resp.html


class LOLRequest(lol_req.LolReq):
    """This class purpose is to request and return needed HTML objects to scrap data.

    Attributes
    ----------
    session : HTMLSession
        Session to request to get HTML object

    """

    def __init__(self):
        super().__init__()
        self.session = HTMLSession()

    def request_champion_html(self, role: str, champion_name: Union[str, Tuple[str]]):
        """Refactors given role and champion_name to send async request for champion HTML object

        Method checks first that role and champion_name are correctly typed.
        If role and champion_name are not valid method will return False and None.
        Then refactors champion name to acceptable for opgg site. Then sends
        request to site if request was not redirected to NOT_FOUND_URLS then
        It will return None instead HTML object.

        Parameters
        __________
        role: str
            Contains role name or champion name first token
        champion_name: Union[str, tuple[str]]
            Contains tuple of champion name tokens or str with name

        Returns
        _______
        bool
            If given data are correct returns True else False
        Union[HTML, None]
            If cannot get HTML object returns None else HTML object
        """

        isvalid, role, champion_name = self.processor.process(role, champion_name)
        if not isvalid:
            return isvalid, role, champion_name

        if role == "aram":
            role = ""
            resp = self.session.get(ARAM_URL.format(champion_name, role))
        else:
            resp = self.session.get(CHAMPION_URL.format(champion_name, role))

        if resp.url in NOT_FOUND_URLS:
            return True, None

        return True, resp.html, role

    def request_tft_synergies_html(self) -> HTML:
        """Requests for lolchess synergies site and returns HTML object

        Return
        ______
        HTML
            HTML object with all traits data
        """
        resp = self.session.get(SYNERGY_URL)

        return resp.html

    def request_tft_items_html(self) -> HTML:
        """Requests for lolchess items site and returns HTML object

        Return
        ______
        HTML
            HTML object with items data
        """
        resp = self.session.get(ITEMS_URL)

        return resp.html
