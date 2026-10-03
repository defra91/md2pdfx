from pathlib import Path
import yaml

from md2pdfx.organization import Organization

class DocumentConfig:
    def __init__(self, path: Path):
        self.path = path
        self.base_dir = path.parent
        self.data = yaml.safe_load(path.read_text(encoding="utf-8"))

        self.organization = Organization(self.data["organization"], self.base_dir)

    @property
    def title(self):
        return self.data.get("title")

    @property
    def subtitle(self):
        return self.data.get("subtitle")

    @property
    def version(self):
        return self.data.get("version")

    @property
    def date(self):
        return self.data.get("date")

    @property
    def authors(self):
        return self.data.get("authors", [])

    @property
    def sections(self):
        return self.data.get("sections", [])

    @property
    def signature(self):
        return self.data.get("signature", {})

    @property
    def custom_styles(self):
        return self.data.get("custom_styles", {})