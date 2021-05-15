from typing import List
from datetime import datetime

from urllib3.util import parse_url
from bs4 import BeautifulSoup
import requests

from .abc import AbstractScrapper
from .. import models, enums


class BandcampScrapper(AbstractScrapper):
    def scrap(self, url: str) -> models.Song:
        bs = self._get_bs(url)
        names = bs.find(id="name-section")
        title = names.find(class_="trackTitle").contents[0].strip()
        album = names.find(class_="fromAlbum").contents[0]
        author = names.find(class_="albumTitle").find_all("a")[1].contents[0]
        tags = {
            i.contents[0]
            for i in bs.find(
                    class_="tralbumData tralbum-tags tralbum-tags-nu hidden"
                ).find_all(class_="tag")
        }
        tags.update({album})

        models.Song(
            url=url,
            title=title,
            author=author,
            description="",
            provided_from=enums.Providers.BANDCAMP,
            tags=tags,
            import_date=datetime.now()
        )

    def scrap_multiple(self, url: str) -> List[models.Song]:
        bs = self._get_bs(url)
        hostname = parse_url(url).hostname
        return [
            self.scrap(f"https://{hostname}{i.div.a['href']}")
            for i in bs.find_all(class_="title-col")
        ]

    def _get_bs(self, url: str) -> BeautifulSoup:
        r = requests.get(url)
        return BeautifulSoup(r.content, "html.parser")
