import requests
from bs4 import BeautifulSoup
from config.settings import BASE_URL, ALLOWED_PATHS


def get_doc_urls():

    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "xml")

    urls = []

    for loc in soup.find_all("loc"):
        url = loc.text
        if any(path in url for path in ALLOWED_PATHS):
            urls.append(url)

    print(f"Found {len(urls)} URLs")
    print(urls[:5])

    return urls
