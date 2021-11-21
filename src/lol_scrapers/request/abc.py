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


class TftRequestStrategy(RequestStrategy):
    @property
    @abstractmethod
    def url(self) -> str:
        pass

    def request(self, session: HTMLSession) -> Tuple[bool, Union[HTML, None]]:
        resp = session.get(self.url)

        if resp.status_code == 200:
            return True, resp.html

        return False, None

    async def arequest(self, session: AsyncHTMLSession) -> Tuple[bool, Union[HTML, None]]:
        resp = await session.get(self.url)

        if resp.status_code == 200:
            return True, resp.html

        return False, None
