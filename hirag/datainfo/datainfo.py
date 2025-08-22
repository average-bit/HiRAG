from abc import ABC
from pathlib import Path
from typing import List, Dict, Any

class DataInfo(ABC):
    def __init__(self, data: str, meta: Dict[str, Any] = None):
        self._data = data
        self._meta = meta or {}

    @property
    def text(self) -> str:
        return self._data

    @property
    def meta(self) -> Dict[str, Any]:
        return self._meta

    @classmethod
    def from_path(cls, path: str) -> "DataInfo":
        file_path = Path(path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        suffix = file_path.suffix.lower()
        if suffix == ".txt":
            return TxtInfo.from_path(path)
        elif suffix == ".md":
            return MdInfo.from_path(path)
        elif suffix == ".pdf":
            return PdfInfo.from_path(path)
        else:
            raise ValueError(f"Unsupported file type: {suffix}")

class TxtInfo(DataInfo):
    @classmethod
    def from_path(cls, path: str) -> "TxtInfo":
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        return cls(data=text, meta={"source": path})

class MdInfo(DataInfo):
    @classmethod
    def from_path(cls, path: str) -> "MdInfo":
        try:
            from markdown_it import MarkdownIt
        except ImportError:
            raise ImportError("Please install markdown-it-py with `pip install markdown-it-py`")

        with open(path, "r", encoding="utf-8") as f:
            md_content = f.read()

        md = MarkdownIt()
        text = md.render(md_content)
        return cls(data=text, meta={"source": path})

class PdfInfo(DataInfo):
    @classmethod
    def from_path(cls, path: str) -> "PdfInfo":
        try:
            import pypdf
        except ImportError:
            raise ImportError("Please install pypdf with `pip install pypdf`")

        with open(path, "rb") as f:
            pdf_reader = pypdf.PdfReader(f)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
        return cls(data=text, meta={"source": path})
