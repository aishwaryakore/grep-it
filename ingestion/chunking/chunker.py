import re

def split_by_sections(text):
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
    parts = re.split(r'(```[\s\S]*?```)', text)

    chunks = []
    current_words = []
    current_word_count = 0

    for part in parts:
        part_words = part.split()
        part_word_count = len(part_words)

        if current_word_count + part_word_count > max_words and not part.startswith("```"):
            if current_words:
                chunks.append(" ".join(current_words))
                # Keep overlap from end of previous chunk
                current_words = current_words[-overlap:]
                current_word_count = len(current_words)

        current_words.extend(part_words)
        current_word_count += part_word_count

    if current_words:
        chunks.append(" ".join(current_words))

    return chunks if chunks else [text]


def create_chunks(doc):
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