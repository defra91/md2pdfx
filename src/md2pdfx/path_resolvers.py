from pathlib import Path

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
