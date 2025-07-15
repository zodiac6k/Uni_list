import requests
import pandas as pd

def get_qs_top100():
    url = "https://www.topuniversities.com/sites/default/files/qs-rankings-data/en/3740566.txt"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json_data = response.json()
        records = json_data["data"]

        data = []
        for rec in records:
            rank = rec.get("rank_display", "")
            name = rec.get("title", "")
            location = rec.get("location", {}).get("name", "")
            url_path = rec.get("url", "")
            full_url = "https://www.topuniversities.com" + url_path

            if location in ["United Kingdom", "Australia", "Canada"]:
                data.append({
                    "Rank": rank,
                    "University": name,
                    "Country": location,
                    "Website": full_url
                })

        return pd.DataFrame(data)

    except Exception as e:
        print("Scraper error:",
