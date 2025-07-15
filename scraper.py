import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_qs_top100():
    url = "https://www.topuniversities.com/university-rankings/world-university-rankings/2025"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    data = []
    table = soup.find("table")
    if not table:
        return pd.DataFrame()

    rows = table.find("tbody").find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 3:
            continue
        try:
            rank = int(cols[0].get_text(strip=True))
            uni = cols[1].get_text(strip=True)
            country = cols[2].get_text(strip=True)
            if country in ["United Kingdom", "Canada", "Australia"]:
                link_tag = cols[1].find("a", href=True)
                link = "https://www.topuniversities.com" + link_tag["href"] if link_tag else ""
                data.append({
                    "Rank": rank,
                    "University": uni,
                    "Country": country,
                    "Website": link
                })
        except:
            continue

    return pd.DataFrame(data)
