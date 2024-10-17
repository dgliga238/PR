import requests
from bs4 import BeautifulSoup
import re
import json
import functools
from datetime import datetime

url = "https://darwin.md/telefoane/smartphone"

response = requests.get(url)

products = []


def convert(price):
    return int(price / 20)


def price_range(price):
    return 1000 < price


if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    raw_prices = []

    for product in soup.find_all("figure", class_="card card-product border-0"):
        names = product.find("figcaption").find("div", class_="title").a.get_text(strip=True)
        prices_text = product.find("div", class_="price-wrap h5 d-flex flex-column m-0").span.get_text(strip=True)

        # Validate price (if it is an integer)
        price_int = re.sub(r"[^\d]", "", prices_text)
        if price_int.isdigit():
            raw_prices.append(price_int)  # Store the raw price string

            link = product.find("figcaption").find("div", class_="title").a.get("href")
            response2 = requests.get(link)
            if response2.status_code == 200:
                soup2 = BeautifulSoup(response2.text, "html.parser")
                prod_elements = soup2.find_all("td", class_="p-8 p-xxl-16")

                if len(prod_elements) >= 2:
                    producator = prod_elements[1].get_text(strip=True)
                    converted_price = convert(int(price_int))
                    product_info = {
                        "name": names,
                        "price": f"{converted_price} EUR",
                        "product": producator,
                        "link": link,
                        "timestamp": datetime.utcnow().isoformat()
                    }

                    if price_range(converted_price):
                        products.append(product_info)
                        print(f"Filtered Product: {product_info}")


    with open("products.json", "w") as files:
        json.dump(products, files, indent=2)

    prices = list(map(int, raw_prices))
    price_eur = list(map(convert, prices))

    # Filter valid prices
    valid_prices = list(filter(price_range, price_eur))


    if valid_prices:
        total_sum = functools.reduce(lambda x, y: x + y, valid_prices)
        print(f"Total sum of filtered products: {total_sum} EUR")
    else:
        print("No valid prices found.")

else:
    print(f"Request failed with status code: {response.status_code}")
