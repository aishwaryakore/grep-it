from bs4 import BeautifulSoup

def extract_title(html):
    soup = BeautifulSoup(html, "html.parser")

    h1 = soup.find("h1")

    if h1:
        return h1.get_text(strip=True)
    return "Untitled"