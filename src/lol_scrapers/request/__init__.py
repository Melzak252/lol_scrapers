from typing import Union, Tuple

from requests_html import HTML

from lol_scrapers.request.abc import LolReq, RequestStrategy


class LolRequest(LolReq):
    def request(self, strategy: RequestStrategy, **kwargs) -> Tuple[bool, Union[HTML, None]]:
        isvalid, html = strategy.request(self.session, **kwargs)

        return isvalid, html

    async def arequest(self, strategy: RequestStrategy, **kwargs) -> Tuple[bool, Union[HTML, None]]:
        isvalid, html = await strategy.arequest(self.asession, **kwargs)

        return isvalid, html
