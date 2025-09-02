"""Utilities for fetching and parsing the Horizon Europe Programme Guide."""
from __future__ import annotations

from pathlib import Path
from typing import Dict

import requests
from pypdf import PdfReader

DEFAULT_GUIDE_URL = (
    "https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/"
    "horizon/guidance/programme-guide_horizon_en.pdf"
)
DEFAULT_GUIDE_PATH = Path("docs/horizon_europe/Horizon_Europe_Programme_Guide.pdf")
DEFAULT_SUMMARY_PATH = Path(
    "docs/horizon_europe/programme_guide_summary.md"
)


def download_programme_guide(
    url: str = DEFAULT_GUIDE_URL, dest: Path | str = DEFAULT_GUIDE_PATH
) -> Path | None:
    """Download the Horizon Europe Programme Guide PDF.

    Attempts to download the guide from ``url`` and save it to ``dest``. If the
    download fails, ``None`` is returned and the user is expected to manually
    place the PDF at ``dest``.
    """
    dest_path = Path(dest)
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            dest_path.write_bytes(response.content)
            return dest_path
        print(
            "Failed to download programme guide. "
            f"Status code {response.status_code}. Please download manually "
            f"and place the PDF at {dest_path}."
        )
    except Exception as exc:  # pragma: no cover - defensive
        print(
            "Error downloading programme guide. "
            f"Please download manually and place the PDF at {dest_path}. "
            f"Details: {exc}"
        )
    return None


def parse_programme_guide(pdf_path: Path | str = DEFAULT_GUIDE_PATH) -> Dict[str, str]:
    """Parse the programme guide PDF and return key sections.

    The parser is lightweight: it extracts text from the PDF and searches for
    a few relevant sections such as "Call" requirements and eligibility rules.
    The returned dictionary maps section titles to extracted text snippets.
    """
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Programme Guide PDF not found at {path}. "
            "Download it or provide it manually."
        )

    reader = PdfReader(str(path))
    full_text = "\n".join(page.extract_text() or "" for page in reader.pages)
    sections: Dict[str, str] = {}
    for title in ["Call", "Eligibility"]:
        idx = full_text.lower().find(title.lower())
        if idx != -1:
            sections[title] = full_text[idx : idx + 500]
    return sections


def create_summary(
    pdf_path: Path | str = DEFAULT_GUIDE_PATH,
    output_md: Path | str = DEFAULT_SUMMARY_PATH,
) -> Path:
    """Create a Markdown summary from the programme guide."""
    sections = parse_programme_guide(pdf_path)
    output = Path(output_md)
    output.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Horizon Europe Programme Guide Summary", ""]
    for heading, content in sections.items():
        lines.append(f"## {heading}\n\n{content.strip()}\n")
    output.write_text("\n".join(lines))
    return output


def query_guide(topic: str, pdf_path: Path | str = DEFAULT_GUIDE_PATH) -> str:
    """Return the first snippet in the guide that mentions ``topic``."""
    sections = parse_programme_guide(pdf_path)
    for content in sections.values():
        if topic.lower() in content.lower():
            return content
    return ""
