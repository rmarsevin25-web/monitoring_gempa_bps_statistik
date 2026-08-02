import requests
from bs4 import BeautifulSoup

URL = "https://www.bps.go.id/en/statistics-table/3/V1ZSbFRUY3lTbFpEYTNsVWNGcDZjek53YkhsNFFUMDkjMyMwMDAw/population--population-growth-rate--percentage-distribution-of-population--population-density--and-population-sex-ratio-by-province.html?year=2025"


def get_html():

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(URL, headers=headers)

    print("Status :", response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")

    return soup