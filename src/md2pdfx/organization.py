from pathlib import Path

from md2pdfx.path_utils import wsl_to_windows

class OrganizationLogo:
    def __init__(self, file: str, rounded: bool, base_dir: Path):
        self.path_linux = (base_dir / file).resolve()
        self.path_windows = self._to_windows(self.path_linux)
        self.rounded = rounded


    def _to_windows(self, path: Path) -> str:
        p = str(path)
        if p.startswith("/mnt/"):
            drive = p[5].upper() + ":"
            rest = p[7:].replace("/", "\\")
            return f"{drive}\\{rest}"

        return p

class Organization:
    def __init__(self, data: dict, base_dir: Path):
        self.name = data.get("name")
        self.address_line_1 = data.get("address_line_1")
        self.address_line_2 = data.get("address_line_2")
        self.tax_code = data.get("tax_code")

        self.logos = [
            OrganizationLogo(
                file=logo["file"],
                rounded=logo.get("rounded", False),
                base_dir=base_dir
            )
            for logo in data.get("logos", [])
        ]

