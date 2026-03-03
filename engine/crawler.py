import requests
from bs4 import BeautifulSoup

def crawl(url):
    urls = []
    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        for a in soup.find_all("a", href=True):
            if a["href"].startswith("http"):
                urls.append(a["href"])
    except:
        pass
    return list(set(urls))
