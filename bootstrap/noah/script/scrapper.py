from urllib.request import urlopen
from bs4 import BeautifulSoup


def scrapper ():
    print("Scrapping data...")
    for i in range(1, 11):
        url = construct_url('charenton-le-pont_94018', i)
        print("Scrapping page {}: {}".format(i, url))
        try:
            response = urlopen(url)
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            # commentaires = soup.find_all('div', attrs={'class': 'commentaires'})
            print(soup.prettify())
            print("Page {} scrapped successfully.".format(i))
        except Exception as e:
            print("Error scrapping page {}: {}".format(i, e))


def construct_url(city, page):
    url = 'https://ville-ideale.fr/'
    if page > 1:
        url += '{}?page={}#commentaires'.format(city, page)
    return url

if __name__ == "__main__":
    scrapper()