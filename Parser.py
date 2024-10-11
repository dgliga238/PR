import requests
from bs4 import BeautifulSoup
import re
import json

url = "https://darwin.md/telefoane/smartphone"

response = requests.get(url)

products = []

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    for product in soup.find_all("figure", class_="card card-product border-0"):

        names = product.find("figcaption").find("div", class_="title").a.get_text(strip=True)
        prices = product.find("div", class_="price-wrap h5 d-flex flex-column m-0").span.get_text(strip=True)

        #validate price (if it is integer)
        price_int = re.sub(r"[^\d]", "", prices)
        if price_int.isdigit():
            price_int = int(price_int)
            price_final = (f"{price_int} lei")
        else:
            print("Invalid price ")

        link = product.find("figcaption").find("div", class_="title").a.get("href")

        response2 = requests.get(link)
        if response2.status_code == 200:
            soup2 = BeautifulSoup(response2.text, "html.parser")

            prod_elements = soup2.find_all("td", class_="p-8 p-xxl-16")

            if len(prod_elements) >= 2:
                producator = prod_elements[1].get_text(strip=True)

                product_info ={
                    "name": names,
                    "price": price_final,
                    "product": producator,
                    "link": link
                }

                products.append(product_info)

        else:
            print("error")

        with open("products.json", "w") as files:
            json.dump(products, files, indent=4)

else:
    print(f"Request failed with status code: {response.status_code}")
