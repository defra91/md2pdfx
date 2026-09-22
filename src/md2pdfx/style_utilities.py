from pathlib import Path
import sass

BASE_DIR = Path(__file__).resolve().parent.parent.parent
STYLES_DIR = BASE_DIR / "styles"
TPL_DIR = BASE_DIR / "templates"

def compile_sass(main_sass_file: str = "main.scss", output_css_file: str = "styles.css"):
    """
    Compiles the main SASS file into a CSS file and writes it to the templates directory.
    """
    input_scss = STYLES_DIR / main_sass_file
    output_css = TPL_DIR / output_css_file

    css = sass.compile(filename=str(input_scss))

    output_css.write_text(css, encoding="utf-8")

    print(f"🎨 CSS generated: {output_css}")
