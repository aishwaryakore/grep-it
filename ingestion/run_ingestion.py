import os
from ingestion.utils.url_collector import get_doc_urls
from ingestion.loaders.web_loader import load_page
from ingestion.cleaners.html_cleaner import clean_html
from ingestion.utils.parser import extract_title
from ingestion.utils.saver import save_json
from config.settings import OUTPUT_RAW_DIR, OUTPUT_CLEAN_DIR

def run_ingestion():
    urls = get_doc_urls()
    print(f"Found {len(urls)} URLs")

    for i, url in enumerate(urls):
        print(f"[{i+1}/{len(urls)}] Processing {url}")

        page = load_page(url)
        if not page:
            continue

        title = extract_title(page["html"])
        cleaned_text = clean_html(page["html"])

        raw_data = {
            "url": url,
            "html": page["html"]
        }

        clean_data = {
            "url": url,
            "title": title,
            "content": cleaned_text
        }

        filename = f"doc_{i}.json"

        save_json(raw_data, os.path.join(OUTPUT_RAW_DIR, filename))
        save_json(clean_data, os.path.join(OUTPUT_CLEAN_DIR, filename))

if __name__ == "__main__":
    run_ingestion()