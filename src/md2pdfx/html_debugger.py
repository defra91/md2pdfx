from pathlib import Path
import shutil

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def dump_debug_html(html: str, css_source: Path):
    """
    Creates a temporary directory called tmp/ in the current working directory,
    resets it if it already exists, and saves the provided HTML and CSS files for debugging purposes.
    """
    tmp_dir = BASE_DIR / "tmp"

    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)

    tmp_dir.mkdir()

    html_path = tmp_dir / "output.html"
    html_path.write_text(html, encoding="utf-8")

    css_target = tmp_dir / "styles.css"
    shutil.copy(css_source, css_target)

    print(f"🔍 Debug HTML saved in: {html_path}")
    print(f"🎨 CSS copied to: {css_target}")
