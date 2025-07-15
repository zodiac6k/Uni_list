import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_universities_from_wikipedia():
    sources = {
        "United Kingdom": "https://en.wikipedia.org/wiki/Russell_Group",
        "Canada": "https://en.wikipedia.org/wiki/Rankings_of_universities_in_Canada",
        "Australia": "https://en.wikipedia.org/wiki/List_of_universities_in_Australia"
    }

    universities = []

    # UK - Russell Group
    uk_resp = requests.get(sources["United Kingdom"])
    uk_soup = BeautifulSoup(uk_resp.text, "html.parser")
    table = uk_soup.find("table", {"class": "wikitable"})
    for row in table.find_all("tr")[1:]:
        cols = row.find_all("td")
        if cols:
            universities.append({
                "University": cols[0].get_text(strip=True),
                "Country": "United Kingdom",
                "Source": "Russell Group"
            })

    # Canada - QS table
    ca_resp = requests.get(sources["Canada"])
    ca_soup = BeautifulSoup(ca_resp.text, "html.parser")
    tables = ca_soup.find_all("table", {"class": "wikitable"})
    ca_table = tables[0]  # first table
    for row in ca_table.find_all("tr")[1:11]:  # top 10 only
        cols = row.find_all("td")
        if len(cols) >= 2:
            universities.append({
                "University": cols[0].get_text(strip=True),
                "Country": "Canada",
                "Source": "Wikipedia QS Canada"
            })

    # Australia - comprehensive list
    au_resp = requests.get(sources["Australia"])
    au_soup = BeautifulSoup(au_resp.text, "html.parser")
    au_table = au_soup.find("table", {"class": "wikitable"})
    for row in au_table.find_all("tr")[1:]:
        cols = row.find_all("td")
        if cols:
            universities.append({
                "University": cols[0].get_text(strip=True),
                "Country": "Australia",
                "Source": "Wikipedia Australia"
            })

    return pd.DataFrame(universities)
