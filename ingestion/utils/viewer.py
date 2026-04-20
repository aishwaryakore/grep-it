import json
import os

INPUT_FILE = "data/cleaned/doc_0.json"   # change file as needed
OUTPUT_FILE = "data/cleaned/doc_0.md"


def convert_to_markdown():
    with open(INPUT_FILE, "r") as f:
        data = json.load(f)

    content = data["content"]

    # Basic cleanup for readability
    content = content.replace("```python", "\n```python\n")
    content = content.replace("```", "\n```\n")

    md = f"# {data['title']}\n\n"
    md += f"**Source:** {data['url']}\n\n"
    md += "---\n\n"
    md += content

    with open(OUTPUT_FILE, "w") as f:
        f.write(md)

    print(f"Markdown file created: {OUTPUT_FILE}")


if __name__ == "__main__":
    convert_to_markdown()