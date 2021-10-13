from abc import ABC, abstractmethod
from typing import Union, Tuple

from requests_html import HTML, AsyncHTMLSession, HTMLSession


class RequestStrategy(ABC):
    @abstractmethod
    def request(self, session: HTMLSession) -> Tuple[bool, Union[HTML, None]]:
        pass

    @abstractmethod
    async def arequest(self, session: AsyncHTMLSession) -> Tuple[bool, Union[HTML, None]]:
        pass


class LolReq(ABC):
    def __init__(self):
        self.session = HTMLSession()
        self.asession = AsyncHTMLSession()

    @abstractmethod
    async def arequest(self, strategy: RequestStrategy) -> Tuple[bool, Union[HTML, None]]:
        pass

    @abstractmethod
    def request(self, strategy: RequestStrategy) -> Tuple[bool, Union[HTML, None]]:
        pass
