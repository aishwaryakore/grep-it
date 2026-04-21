import re

def split_by_sections(text):
    """
    Splits document into sections using markdown headings.
    """
    sections = []
    current_section = None
    buffer = []

    lines = text.split("\n")

    for line in lines:
        if re.match(r"^#{1,4}\s", line):
            if current_section:
                sections.append((current_section, "\n".join(buffer)))

            current_section = line.strip()
            buffer = []
        else:
            buffer.append(line)

    if current_section:
        sections.append((current_section, "\n".join(buffer)))

    return sections


def split_large_chunk(text, max_words=500, overlap=100):
    """
    Splits large chunks into smaller ones with overlap.
    """
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + max_words
        chunk = " ".join(words[start:end])
        chunks.append(chunk)

        start += max_words - overlap

    return chunks


def create_chunks(doc):
    """
    doc = {
        "url": "...",
        "title": "...",
        "content": "cleaned markdown"
    }
    """
    sections = split_by_sections(doc["content"])
    final_chunks = []

    for section_title, section_content in sections:
        full_text = f"{doc['title']}\n{section_title}\n{section_content}"

        sub_chunks = split_large_chunk(full_text)

        for chunk in sub_chunks:
            final_chunks.append({
                "content": chunk,
                "source": doc["url"],
                "section": section_title,
                "title": doc["title"]
            })

    return final_chunks