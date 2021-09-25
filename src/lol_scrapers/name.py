from requests_html import HTML


class NameScraper:

    def get_champion_name(self, champion_html: HTML):
        champion_name_desc = champion_html.find(
            "h1.champion-stats-header-info__name", first=True
        ).text.strip()
        champion_name, *description = champion_name_desc.split(" ")
        description = " ".join(description)

        champion_img = champion_html.find(".champion-stats-header-info__image", first=True).find(
            "img", first=True
        )

        return {
            "name": champion_name.strip(),
            "description": description.strip(),
            "icon_src": self.src2https(champion_img.attrs["src"]),
            "url": champion_html.url,
        }

    @staticmethod
    def src2https(src: str):
        return f"https:{src}"
