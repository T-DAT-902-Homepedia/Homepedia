import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

url = "https://www.ville-ideale.fr/amberieu-en-bugey_1004"
response = requests.get(url, headers=headers)

print("Status code:", response.status_code)
print("Taille:", len(response.text))
print("Contenu:", response.text[:500])