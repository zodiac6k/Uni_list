import pandas as pd
import requests
from bs4 import BeautifulSoup

WIKI_URLS = {
    "Canada": "https://en.wikipedia.org/wiki/Rankings_of_universities_in_Canada",
    "Australia": "https://en.wikipedia.org/wiki/University_of_Queensland",  # replace with robust list page later
    "United Kingdom": "https://en.wikipedia.org/wiki/Russell_Group"
}

def get_rankings_from_wiki(country):
    url = WIKI_URLS[country]
    resp = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    data = []

    table = soup.find("table", {"class":"wikitable"})
    if not table: return pd.DataFrame()

    for row in table.find_all("tr")[1:11]:
        cols = [c.get_text(strip=True) for c in row.find_all(["td", "th"])]
        if country == "Canada":
            uni = cols[0]
            rank = cols[1].split(" ")[0]
        else:
            uni = cols[0]
            rank = cols[1] if len(cols) > 1 else ""
        data.append({"University": uni, "Rank": rank, "Country": country})

    return pd.DataFrame(data)

def get_all():
    dfs = [get_rankings_from_wiki(c) for c in WIKI_URLS]
    combined = pd.concat(dfs, ignore_index=True)
    return combined.dropna(subset=["University"])
