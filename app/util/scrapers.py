import bs4, urllib.request


def get_soup(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"
    }
    req = urllib.request.Request(url, headers=headers)
    raw = urllib.request.urlopen(req).read()
    return bs4.BeautifulSoup(raw, "html.parser")


def smh():
    soup = get_soup("http://weather.smh.com.au/local-forecast/nsw/sydney")
    return float(soup("div", "ff_current_temp")[0].text.strip()[:-2])


def bom():
    soup = get_soup("http://www.bom.gov.au")
    caps = soup("div", "capital")
    syd = [x for x in caps if x("h3")[0].text == "Sydney"][0]
    return float(syd("p", "now")[0]("span", "val")[0].text[:-1])


def wzn():
    soup = get_soup("https://m.weatherzone.com.au/nsw/sydney/sydney")
    return float(soup("div", id="today_now")[0].text[3:-2])
