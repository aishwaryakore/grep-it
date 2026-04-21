from bs4 import BeautifulSoup

def clean_html(html):
    soup = BeautifulSoup(html, "html.parser")

    main = soup.find(id="body-content")
    if main:
        soup = main

    sidebar = soup.find(id="sidebar-content")
    if sidebar:
        sidebar.decompose()

    banner = soup.find(id="banner")
    if banner:
        banner.decompose()

    for tag in soup(["nav", "footer", "aside", "script", "style", "button", "svg", "img"]):
        tag.decompose()

    content = []
    seen = set()

    for element in soup.find_all(["h1", "h2", "h3", "h4", "p", "pre", "span"]):

        if element.find_parent(["p", "pre"]) and element.name != "span":
            continue

        if element.name == "span":
            if element.get("data-as") == "p":
                text = element.get_text(" ", strip=True)
            else:
                continue
        elif element.name == "pre":
            code = element.get_text()
            content.append(f"\n```python\n{code}\n```\n")
            continue
        else:
            text = element.get_text(" ", strip=True)

        text = text.replace("\u200b", "").strip()

        if not text:
            continue

        if any(x in text for x in ["Join us", "Was this page helpful", "Edit this page"]):
            continue

        if text in seen:
            continue
        seen.add(text)

        if element.name == "h1":
            content.append(f"\n# {text}\n")
        elif element.name == "h2":
            content.append(f"\n## {text}\n")
        elif element.name == "h3":
            content.append(f"\n### {text}\n")
        elif element.name == "h4":
            content.append(f"\n#### {text}\n")
        else:
            content.append(text)

    return "\n\n".join(content)

