from abc import ABC, abstractmethod

from requests_html import HTML


class ScrapeStrategy(ABC):

    @abstractmethod
    def scrape(self, html: HTML, *args):
        pass
