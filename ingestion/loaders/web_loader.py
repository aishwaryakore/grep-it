import requests

def load_page(url):
    try:
        resonse = requests.get(url)
        return {
            "url" : url,
            "html" : resonse.text
        }
    except:
        print(f"Error loading {url}: {e}")
        return None
    