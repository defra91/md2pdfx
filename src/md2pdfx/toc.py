import re
from pathlib import Path

HEADING_RE = re.compile(r'^(#{1,6})\s+(.*)$')
HEADING_HTML_RE = re.compile(r'<h([1-6])>(.*?)</h\1>')

def extract_headings(md_path: Path):
    headings = []

    for line in md_path.read_text(encoding="utf-8").splitlines():
        match = HEADING_RE.match(line)
        if not match:
            continue

        level = len(match.group(1))
        title = match.group(2).strip()

        headings.append({
            "level": level,
            "title": title,
            "file": md_path.name
        })

    return headings


def number_toc(headings):
    counters = [0] * 6  
    numbered = []

    for h in headings:
        level = h["level"]

        counters[level - 1] += 1

        for i in range(level, 6):
            counters[i] = 0

        number = ".".join(str(counters[i]) for i in range(level) if counters[i] > 0)

        numbered.append({
            "level": level,
            "title": h["title"],
            "number": number,
            "file": h["file"]
        })

    return numbered


def apply_heading_numbers(html: str, toc: list[dict]) -> str:
    """
    Inserisce la numerazione nei titoli HTML basandosi sulla TOC numerata.
    """
    def replace(match):
        level = int(match.group(1))
        title = match.group(2).strip()

        # Trova la voce corrispondente nella TOC
        for item in toc:
            if item["level"] == level and item["title"] == title:
                number = item["number"]
                anchor = slugify(title)
                return f'<h{level} id="{anchor}">{number} {title}</h{level}>'

        # fallback: nessuna numerazione
        return match.group(0)

    return HEADING_HTML_RE.sub(replace, html)


def slugify(text: str) -> str:
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
