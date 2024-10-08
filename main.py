import requests

url = 'https://darwin.md/'

response = requests.get(url)

if response.status_code == 200:
    print(response.text)
else:
    print(f"Failed. Status code: {response.status_code}")
