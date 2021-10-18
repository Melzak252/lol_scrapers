from typing import Tuple

from unidecode import unidecode
from lol_scrapers.utils import ROLES


class ChampionNameProcessor:
    def __init__(self, champion_tokens: Tuple[str]):
        self.champion_tokens = champion_tokens
        self.role = ""

    def process(self):
        isvalid = self._check()

        if not isvalid:
            return False, None, None

        return True, self.role, self.name

    @property
    def name(self) -> str:
        champion_name = "".join(self.champion_tokens)
        champion_name = unidecode(champion_name)

        if champion_name.lower().startswith("nunu"):
            champion_name = "nunu"

        if champion_name == "wukong":
            champion_name = "monkeyking"

        return champion_name

    def _check(self):

        if not self.champion_tokens or not self.champion_tokens[0]:
            return False
        self.champion_tokens = [
            (token.replace(" ", "").replace("'", "").replace(".", "").replace(",", "").replace("&", "").lower())
            for token in self.champion_tokens
        ]

        self.champion_tokens = [token for token in self.champion_tokens if token]

        if not all(token.isalpha() for token in self.champion_tokens if token):
            return False

        if self.is_role(self.champion_tokens[0]):
            if len(self.champion_tokens) == 1:
                return False

            self.role, *self.champion_tokens = self.champion_tokens
            self.role = ROLES[self.role]

        return True

    @staticmethod
    def is_role(token) -> bool:
        return token.lower() in ROLES
