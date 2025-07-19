import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def scrape_shiksha_bba_canada():
    url = "https://studyabroad.shiksha.com/canada/bba-colleges-dc"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    base_url = "https://studyabroad.shiksha.com"

    universities = []
    for card in soup.find_all("div", class_="tuple-content"):
        name_tag = card.find("a", class_="uni-link")
        name = name_tag.text.strip() if name_tag else ""
        website = base_url + name_tag["href"] if name_tag and name_tag["href"].startswith("/") else (name_tag["href"] if name_tag else "")
        city = card.find("span", class_="location-span")
        city = city.text.strip() if city else ""
        fees = card.find("div", class_="fees-col")
        fees = re.sub(r"\s+", " ", fees.text.strip()) if fees else ""

        universities.append({
            "University": name,
            "Country": "Canada",
            "City": city,
            "Course": "BBA",
            "Fees (INR)": fees,
            "Co-op": "Unknown",
            "Indian/Vegetarian Friendly": "Unknown",
            "Website": website
        })

    df = pd.DataFrame(universities)
    df.to_csv("universities_detailed.csv", index=False)
    print("Saved to universities_detailed.csv")

if __name__ == "__main__":
    scrape_shiksha_bba_canada()
