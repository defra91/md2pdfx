from pathlib import Path
from weasyprint import HTML

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TPL_DIR = BASE_DIR / "templates"

def html_to_pdf(html: str, output_path: str):
    HTML(
        string=html,
        base_url=str(TPL_DIR)
    ).write_pdf(output_path)
