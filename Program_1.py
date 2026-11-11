from pathlib import Path
import html
import re
import sys


BASE_DIR = Path(sys.executable).resolve().parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent
OUTPUT_FILE = BASE_DIR / "All.html"

PAGE_PATTERN = re.compile(
    r'((?:Page|page)_\d+:\s*")((?:\\.|[^"\\])*)(")'
)


def read_text_file(path):
    data = path.read_bytes()

    for encoding in ("utf-8-sig", "cp1251", "utf-8"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue

    raise UnicodeError(f"Failed to read the file: {path.name}")


def escape_text(text):
    return html.escape(text, quote=False)


def convert_content(content):
    result = []
    position = 0

    for match in PAGE_PATTERN.finditer(content):
        before = content[position:match.start()]

        result.extend(
            f"<p>{escape_text(line)}</p>"
            for line in before.splitlines()
        )

        prefix, text, closing_quote = match.groups()

        result.append(
            '<p><span translate="no">'
            + escape_text(prefix)
            + '</span>'
            + escape_text(text)
            + '<span translate="no">'
            + escape_text(closing_quote)
            + '</span></p>'
        )

        position = match.end()

    remaining = content[position:]

    result.extend(
        f"<p>{escape_text(line)}</p>"
        for line in remaining.splitlines()
    )

    return result


def main():
    files = sorted(
        (
            path for path in BASE_DIR.iterdir()
            if path.is_file()
            and path.suffix.lower() == ".str"
        ),
        key=lambda path: path.name.lower()
    )

    if not files:
        print(".str files were not found next to the program.")
        input("Press Enter to exit...")
        return

    document = [
        "<!DOCTYPE html>",
        '<html>',
        "<head>",
        '<meta charset="UTF-8">',
        "<title>All</title>",
        "</head>",
        "<body>",
    ]

    for path in files:
        try:
            content = read_text_file(path)
        except (OSError, UnicodeError) as error:
            print(f"Read error {path.name}: {error}")
            continue

        filename_header = f"---Name: {path.stem}---"

        document.append(
            '<p><span translate="no">'
            + escape_text(filename_header)
            + '</span></p>'
        )

        document.extend(convert_content(content))

        print(f"File processed: {path.name}")

    document.extend(["</body>", "</html>"])

    OUTPUT_FILE.write_text(
        "\n".join(document),
        encoding="utf-8",
        newline="\n"
    )

    print(f"\nFile created: {OUTPUT_FILE.name}")
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()
