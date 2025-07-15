import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_qs_top100():
    url = "https://www.topuniversities.com/university-rankings/world-university-rankings/2025"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")

    rows = soup.select("tbody tr")  # Adjusted selector for 2025 page structure
    data = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 3:
            try:
                rank = int(cols[0].text.strip())
                uni = cols[1].text.strip()
                location = cols[2].text.strip()
                link_tag = cols[1].find("a")
                link = "https://www.topuniversities.com" + link_tag["href"] if link_tag else ""
                country = location.split(",")[-1].strip()
                if country in ["United Kingdom", "Australia", "Canada"]:
                    data.append({
                        "Rank": rank,
                        "University": uni,
                        "Country": country,
                        "Website": link
                    })
            except Exception:
                continue

    return pd.DataFrame(data)
