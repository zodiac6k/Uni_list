import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_qs_top100():
    url = "https://www.topuniversities.com/student-info/choosing-university/worlds-top-100-universities"
    resp = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    rows = soup.select("tr")  # adjust selector to match table rows
    data = []
    for r in rows:
        cols = [c.get_text(strip=True) for c in r.find_all("td")]
        if len(cols) >= 3:
            rank, uni, location = cols[:3]
            country = location.split(",")[-1].strip()
            if country in ["United Kingdom","Australia","Canada"]:
                link = r.find("a", href=True)["href"]
                data.append({"Rank": int(rank), "University": uni, "Country": country, "Link": link})
    return pd.DataFrame(data)
