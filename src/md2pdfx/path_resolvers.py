from pathlib import Path
from md2pdfx.path_utils import wsl_to_windows


def resolve_section_paths(config_path: Path, sections: list[str]) -> list[Path]:
    base_dir = config_path.parent
    md_files = []

    for s in sections:
        file_path = (base_dir / s).resolve()

        if not file_path.exists():
            raise FileNotFoundError(
                f"File not found relative to document.yml:\n  {file_path}"
            )

        md_files.append(file_path)

    return md_files


def resolve_custom_styles_paths(config_path: Path, custom_styles: list[str], debug_html: bool) -> list[str]:
    base_dir = config_path.parent
    resolved_paths = []

    for s in custom_styles:
        file_path = (base_dir / s).resolve()

        if not file_path.exists():
            raise FileNotFoundError(
                f"Custom style file not found relative to document.yml:\n  {file_path}"
            )

        if debug_html:
            file_path = wsl_to_windows(file_path)

        resolved_paths.append(file_path)

    return resolved_paths