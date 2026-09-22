import re

def normalize_heading(html: str) -> str:
    """
    Normalize the headings in the given HTML string.
    Turns h1 into h2, h2 into h3, and so on.
    """
    def replace(match):
        level = int(match.group(1))
        new_level = min(level + 1, 6)
        return f"h{new_level}"

    return re.sub(r"h([1-6])", replace, html)