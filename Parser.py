import socket
import ssl
import re
import functools
from datetime import datetime
from bs4 import BeautifulSoup
import json


def create_ssl_socket(hostname, port=443):
    # Create a socket and wrap it with SSL
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context = ssl.create_default_context()
    ssl_sock = context.wrap_socket(sock, server_hostname=hostname)
    return ssl_sock


def send_http_request(sock, request):
    sock.send(request.encode())
    response = b""
    while True:
        data = sock.recv(4096)  # Receiving data in chunks
        if not data:
            break
        response += data
    return response


def parse_product_info(product):
    names = product.find("figcaption").find("div", class_="title").a.get_text(strip=True)
    prices_text = product.find("div", class_="price-wrap h5 d-flex flex-column m-0").span.get_text(strip=True)

    # Validate price (if it is an integer)
    price_int = re.sub(r"[^\d]", "", prices_text)
    if price_int.isdigit():
        return names, int(price_int)
    return None, None


def convert(price):
    return int(price / 20)


def price_range(price):
    return 1000 < price


def main():
    hostname = 'darwin.md'
    port = 443

    try:
        # Create the initial socket connection to get the product list
        sock = create_ssl_socket(hostname, port)
        sock.connect((socket.gethostbyname(hostname), port))
        print(f"The socket has successfully connected to {hostname}")

        # Sending an HTTP GET request (over HTTPS)
        http_request = "GET /telefoane/smartphone HTTP/1.1\r\nHost: darwin.md\r\nConnection: close\r\n\r\n"
        response = send_http_request(sock, http_request)
        sock.close()  # Close the socket after receiving the initial response

        # Decoding the response
        response_str = response.decode()

        # Splitting the response into headers and body
        headers, response_body = response_str.split("\r\n\r\n", 1)

        # Parsing the HTML response
        soup = BeautifulSoup(response_body, "html.parser")
        products = []
        raw_prices = []
        xml_products = []

        for product in soup.find_all("figure", class_="card card-product border-0"):
            names, price_int = parse_product_info(product)
            if price_int:
                raw_prices.append(price_int)  # Store the raw price string
                link = product.find("figcaption").find("div", class_="title").a.get("href")

                # Create a new socket connection for the product detail request
                detail_sock = create_ssl_socket(hostname, port)
                detail_sock.connect((socket.gethostbyname(hostname), port))

                # Send a request for the product details
                detail_request = f"GET {link} HTTP/1.1\r\nHost: darwin.md\r\nConnection: close\r\n\r\n"
                detail_response = send_http_request(detail_sock, detail_request)
                detail_sock.close()  # Close the socket after receiving the detail response

                detail_response_str = detail_response.decode()
                detail_headers, detail_response_body = detail_response_str.split("\r\n\r\n", 1)
                soup_detail = BeautifulSoup(detail_response_body, "html.parser")

                prod_elements = soup_detail.find_all("td", class_="p-8 p-xxl-16")
                if len(prod_elements) >= 2:
                    producator = prod_elements[1].get_text(strip=True)
                    converted_price = convert(price_int)

                    product_info = {
                        "name": names,
                        "price": f"{converted_price} EUR",
                        "producator": producator,
                        "link": link,
                        "timestamp": datetime.utcnow().isoformat()
                    }

                    if price_range(converted_price):
                        products.append(product_info)
                        xml_product = f"""
                        <product>
                            <name>{names}</name>
                            <price>{converted_price} EUR</price>
                            <producator>{producator}</producator>
                            <link>{link}</link>
                        </product>
                        """
                        xml_products.append(xml_product)


        # Display the XML output after all products have been processed
        xml_output = "<products>\n" + "\n".join(xml_products) + "\n</products>"
        print("\nFiltered products in XML format:")
        print(xml_output)

        # Print products in JSON format
        json_output = json.dumps(products, indent=4)  # Convert products list to JSON format
        print("\nFiltered products in JSON format:")
        print(json_output)

        # Filter valid prices
        prices = list(map(int, raw_prices))
        price_eur = list(map(convert, prices))
        valid_prices = list(filter(price_range, price_eur))

        if valid_prices:
            total_sum = functools.reduce(lambda x, y: x + y, valid_prices)
            print(f"\nTotal sum of filtered products: {total_sum} EUR")
        else:
            print("No valid prices found.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

