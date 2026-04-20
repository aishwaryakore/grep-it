from bs4 import BeautifulSoup

def clean_html(html):
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup(["nav", "footer", "aside", "script", "style", "button", "svg", "img"]):
        tag.decompose()

    content = []

    for element in soup.find_all(["h1", "h2", "h3", "h4", "p", "pre", "code", "li", "div", "span"]):

        if element.find_parent(["p", "pre", "li"]):
            continue

        text = element.get_text(separator=" ", strip=True)

        if not text or len(text) < 20:
            continue

        if element.name in ["h1", "h2", "h3", "h4"]:
            content.append(f"\n## {text}\n")
        elif element.name == "pre":
            content.append(f"\n```\n{text}\n```\n")
        elif element.name == "li":
            content.append(f"- {text}")
        else:
            content.append(text)

    seen = []
    for line in content:
        if not seen or line != seen[-1]:
            seen.append(line)

    return "\n".join(seen)

