from typing import Union, Tuple

from requests_html import HTML

from lol_scrapers.request.abc import LolReq, RequestStrategy


class LolRequest(LolReq):
    def request(self, strategy: RequestStrategy) -> Tuple[bool, Union[HTML, None]]:
        isvalid, html = strategy.request(self.session)

        return isvalid, html

    async def arequest(self, strategy: RequestStrategy) -> Tuple[bool, Union[HTML, None]]:
        isvalid, html = await strategy.arequest(self.asession)

        return isvalid, html
