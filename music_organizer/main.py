import requests
from bs4 import BeautifulSoup

URL = "https://pilotredsun.bandcamp.com/album/achievement"
r = requests.get(URL)
bs = BeautifulSoup(r.content, "html.parser")
for i in bs.find_all(class_="title-col"):
    print(i.div.a["href"])
