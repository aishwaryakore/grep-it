import requests

def load_page(url):
    try:
        resonse = requests.get(url)
        return {
            "url" : url,
            "html" : resonse.text
        }
    except Exception as e:
        print(f"Error loading {url}: {e}")
        return None
    