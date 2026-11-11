import configparser
import re
import sys
from pathlib import Path

BASE_DIR = Path(sys.executable).resolve().parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent
SOURCE_FILE = BASE_DIR / "All.txt"
OUTPUT_DIR = BASE_DIR / "Result"

CONFIG_FILE = BASE_DIR / "config.ini"

config = configparser.ConfigParser()
config.read(CONFIG_FILE, encoding="utf-8")

MAX_WORDS = config.getint("Settings", "max_words", fallback=130)
ENCODING = "cp1251"


def count_words(text):
    return len(text.split())


def split_long_text(text, max_words=MAX_WORDS):
    words = text.split()
    if len(words) <= max_words:
        return [text]

    return [
        " ".join(words[i:i + max_words])
        for i in range(0, len(words), max_words)
    ]



def process_section(section):
    lines = section.splitlines()
    result = []
    next_page_number = 0

    while lines:
        line = lines.pop(0)

        match = re.match(
            r'^(\s*[Pp]age_)(\d+)(\s*:\s*")(.*)(")\s*$',
            line
        )

        if not match:
            result.append(line)
            continue

        prefix, original_number, separator, content, suffix = match.groups()

        words = content.split()

        if not words:
            parts = [""]
        else:
            parts = [
                " ".join(words[i:i + MAX_WORDS])
                for i in range(0, len(words), MAX_WORDS)
            ]

        for part in parts:
            result.append(
                f'{prefix}{next_page_number}{separator}{part}"'
            )
            next_page_number += 1

    return "\n".join(result)



def main():
    if not SOURCE_FILE.exists():
        print(f"File not found: {SOURCE_FILE}")
        input("Press Enter to exit...")
        return

    raw = SOURCE_FILE.read_bytes()

    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = raw.decode("cp1251")

    sections = re.split(
        r'(?m)^---Name:\s*(.*?)\s*---\s*$',
        text
    )

    OUTPUT_DIR.mkdir(exist_ok=True)

    created = 0

    for index in range(1, len(sections), 2):
        name = sections[index].strip()
        content = sections[index + 1] if index + 1 < len(sections) else ""

        processed = process_section(content)

        processed = processed.strip()

        output_file = OUTPUT_DIR / f"{name}.str"

        processed = processed.replace("\u202f", " ")
        processed = processed.replace("\u00a0", " ")
        processed = processed.replace("\u2011", "-")
        processed = processed.replace("\u2013", "-")
        processed = processed.replace("\u2014", "-")
        processed = processed.replace("\u2018", "'")
        processed = processed.replace("\u2019", "'")
        processed = processed.replace("\u201c", '"')
        processed = processed.replace("\u201d", '"')

        encoded = processed.encode(ENCODING, errors="replace")
        output_file.write_bytes(encoded)
        created += 1
        print(f"File created: {output_file.name}")

    print(f"\nDone. Files created: {created}")
    print(f"The results are in: {OUTPUT_DIR}")
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
