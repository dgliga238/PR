import requests
from bs4 import BeautifulSoup

url = "https://darwin.md/telefoane/smartphone"

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    for product in soup.find_all("figure", class_="card card-product border-0"):

        names = product.find("figcaption").find("div", class_="title").a.text
        prices = product.find("div", class_="price-wrap h5 d-flex flex-column m-0").span.text
        link = product.find("figcaption").find("div", class_="title").a.get("href")

        response2 = requests.get(link)
        if response2.status_code == 200:
            soup2 = BeautifulSoup(response2.text, "html.parser")

            prod_elements = soup2.find_all("td", class_="p-8 p-xxl-16")

            if len(prod_elements) >= 2:
                producator = prod_elements[1].text
                print(f"{names} Price: {prices}\n Producator: {producator} ")

        else:
            print("error")

else:
    print(f"Request failed with status code: {response.status_code}")
