from typing import Tuple, Union

from unidecode import unidecode
from lol_scrapers.utils import ROLES


class ChampionNameProcessor:

    def process(self, role, champion_name):
        isvalid = self._check(role, champion_name)

        if not isvalid:
            return False, None, None

        role, champion_name = isvalid

        champion_name = self._refactor(champion_name)
        if not champion_name.isalpha():
            return False, None, None

        return True, role, champion_name

    @staticmethod
    def _refactor(champion_name: Union[Tuple[str], str]) -> str:
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
    def _check(role: str, champ: Union[str, Tuple[str]]):
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
