# src/cli.py

import click
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from md2pdfx.toc import apply_heading_numbers, number_toc
from md2pdfx.path_resolvers import resolve_section_paths, resolve_custom_styles_paths
from md2pdfx.style_utilities import compile_sass
from md2pdfx.pdf import html_to_pdf
from md2pdfx.heading_normalizer import normalize_heading
from md2pdfx.html_debugger import dump_debug_html
from md2pdfx.config import DocumentConfig
from md2pdfx.toc import extract_headings
from md2pdfx.md import render_md

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TPL_DIR = BASE_DIR / "templates"

env = Environment(loader=FileSystemLoader(str(TPL_DIR)))
template = env.get_template("base.html")

@click.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True, dir_okay=False),
    default="document.yml",
    help="Path to the document configuration file in YAML format."
)
@click.option(
    "--output",
    "-o",
    type=click.Path(dir_okay=False),
    default="output.pdf",
    help="Path to the final PDF."
)
@click.option(
    "--debug-html",
    is_flag=True,
    help="If specified, generates a debug HTML and CSS dump in the tmp/ directory."
)
@click.option(
    "--show-toc",
    is_flag=True,
    default=False,
    help="If specified, includes a table of contents in the generated PDF."
)
def main(config, output, debug_html, show_toc):

    config_path = Path(config)
    cfg = DocumentConfig(config_path)
    out_path = Path(output)

    compile_sass()
    md_files = resolve_section_paths(Path(config), cfg.sections)

    toc_raw = []
    for md_file in md_files:
        toc_raw.extend(extract_headings(md_file))
    toc_numbered = number_toc(toc_raw)
    toc = [item for item in toc_numbered if item["level"] == 1]

    if not show_toc:
        toc = []

    html_parts = []

    for file in md_files:
        raw = file.read_text(encoding="utf-8")
        rendered = render_md(raw)
        normalized  = normalize_heading(rendered)
        numbered_html = apply_heading_numbers(normalized, toc)
        html_parts.append(numbered_html)

    logos = [
       (logo.path_windows if debug_html else logo.path_linux, logo.rounded)
        for logo in cfg.organization.logos
    ]

    full_html = template.render(
        organization=cfg.organization,
        title=cfg.title,
        subtitle=cfg.subtitle,
        content="\n".join(html_parts),
        toc=toc,
        logos=logos,
        signature=cfg.signature,
        custom_styles_href_list=resolve_custom_styles_paths(config_path, cfg.custom_styles, debug_html)
    )

    if debug_html:
        css_source = TPL_DIR / "styles.css"
        dump_debug_html(full_html, css_source)

    html_to_pdf(full_html, out_path)

    click.echo(f"✔️ PDF generated: {out_path}")