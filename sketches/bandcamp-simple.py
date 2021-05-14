import requests
from urllib3.util import parse_url
from bs4 import BeautifulSoup
import youtube_dl


URL = "https://pilotredsun.bandcamp.com/album/achievement"
YDL_PARAMS = {
    "format": "bestaudio/best"
}

url = parse_url(URL)

r = requests.get(URL)
bs = BeautifulSoup(r.content, "html.parser")

with youtube_dl.YoutubeDL(YDL_PARAMS) as ydl:
    for i in bs.find_all(class_="title-col"):
        route = i.div.a["href"]
        audio_url = f"https://{url.hostname}{route}"
        info = ydl.extract_info(audio_url, download=False)
        print(info["url"])
