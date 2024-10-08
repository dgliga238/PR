import requests
from bs4 import BeautifulSoup

url = "https://darwin.md/telefoane/smartphone"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    for product in soup.find_all("figure", class_="card card-product border-0"):

        names = product.find("figcaption").find("div", class_="title").a.get_text(strip=True)
        prices = product.find("div", class_="price-wrap h5 d-flex flex-column m-0").span.get_text(strip=True)
        print(f"{names}: {prices}")

else:
    print(f"Request failed with status code: {response.status_code}")
