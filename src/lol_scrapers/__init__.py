from typing import Union, Tuple

from requests_html import HTMLSession, AsyncHTMLSession, HTML
from unidecode import unidecode

NOT_FOUND_URLS = [
    "https://eune.op.gg/champion/statistics",
    "https://eune.op.gg/aram/statistics",
]

CHAMPION_URL = "https://eune.op.gg/champion/{}/statistics/{}"
ARAM_URL = "https://eune.op.gg/aram/{}/statistics/{}"
SYNERGY_URL = "https://lolchess.gg/synergies"
ITEMS_URL = "https://lolchess.gg/items"

ROLES = {
    "top": "top",
    "jungle": "jungle",
    "jg": "jungle",
    "jng": "jungle",
    "mid": "mid",
    "middle": "mid",
    "adc": "adc",
    "bot": "adc",
    "support": "support",
    "supp": "support",
    "sup": "support",
}


class LOLRequest:
    """This class purpose is to request and return needed HTML objects to scrap data.

    Attributes
    ----------
    asession : AsyncHTMLSession
        Asynchronous session to request to get HTML object
    session : HTMLSession
        Session to request to get HTML object

    """

    def __init__(self):
        self.asession = AsyncHTMLSession()
        self.session = HTMLSession()

    async def async_request_champion_html(self, role: str, champion_name: Union[str, Tuple[str]]):
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

        isvalid = self._check_role_champ(role, champion_name)

        if not isvalid:
            return False, None, None

        role, champion_name = isvalid

        champion_name = self._refactor_champ_name(champion_name)
        if not champion_name.isalpha():
            return False, None, None

        if role == "aram":
            role = ""
            resp = await self.asession.get(ARAM_URL.format(champion_name, role))
        else:
            resp = await self.asession.get(CHAMPION_URL.format(champion_name, role))

        return True, resp.html, role

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

        isvalid = self._check_role_champ(role, champion_name)

        if not isvalid:
            return False, None

        role, champion_name = isvalid

        champion_name = self._refactor_champ_name(champion_name)
        if not champion_name.isalpha():
            return False, None

        if role == "aram":
            role = ""
            resp = self.session.get(ARAM_URL.format(champion_name, role))
        else:
            resp = self.session.get(CHAMPION_URL.format(champion_name, role))

        if resp.url in NOT_FOUND_URLS:
            return True, None

        return True, resp.html, role

    @staticmethod
    def _refactor_champ_name(champion_name: Union[Tuple[str], str]) -> str:
        """Refactors given champion tokens to acceptable str format

        Parameter
        _________
        champion_name: Union[Tuple[str], str]
            Its tuple of tokens of champion name or string with main token

        Returns
        _______
        str
            Refactored str acceptable by opgg
        """

        if isinstance(champion_name, tuple):
            champion_name = "".join(champion_name)

        champion_name = unidecode(champion_name)
        champion_name = champion_name.replace(" ", "").replace("'", "").replace(".", "").replace(",", "").lower()
        if champion_name.lower().startswith("nunu"):
            champion_name = "nunu"

        if champion_name == "wukong":
            champion_name = "monkeyking"

        return champion_name

    @staticmethod
    def _check_role_champ(role: str, champ: Union[str, Tuple[str]]):
        """Checks if given parameters are valid and refactors them if needed

         if role is not given or is empty string returns empty tuple as sign of invalid data
         if role is nor in ROLES or is "aram" then role is consider as first token of champion name
         else checks if there is given champion name if the champ is empty then returns empty tuple

        Parameters
        __________
        role: str
            Contains role name or champion name first token
        champ: Union[str, Tuple[str]]
            Contains tuple of champion name tokens or str with name

        Returns
        _______
        If there are incorrect data
            Tuple[()]
                Empty tuple as a sign of incorrect data
        else
            str
                Empty if there is no selected role else refactored selected role to acceptable version by opgg
            Tuple[str]
                Tokens of champion name

        """
        if not role:
            return ()

        role = role.lower()
        if role == "aram":
            if not champ:
                return ()
            return role, champ

        if role in ROLES:
            role = ROLES[role]

            if not champ:
                return ()

            return role, champ

        champion_tuple, role = (role, *champ), ""

        return role, champion_tuple

    async def async_request_tft_synergies_html(self) -> HTML:
        """Async requests for lolchess synergies site and returns HTML object

        Return
        ______
        HTML
            HTML object with all traits data
        """
        resp = await self.asession.get(SYNERGY_URL)

        return resp.html

    def request_tft_synergies_html(self) -> HTML:
        """Requests for lolchess synergies site and returns HTML object

        Return
        ______
        HTML
            HTML object with all traits data
        """
        resp = self.session.get(SYNERGY_URL)

        return resp.html

    async def async_request_tft_items_html(self) -> HTML:
        """Async requests for lolchess items site and returns HTML object

        Return
        ______
        HTML
            HTML object with items data
        """
        resp = await self.asession.get(ITEMS_URL)

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
