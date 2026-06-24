import requests

def load_page(url):
    try:
        response = requests.get(url)
        return {
            "url" : url,
            "html" : response.text
        }
    except Exception as e:
        print(f"Error loading {url}: {e}")
        return None
    