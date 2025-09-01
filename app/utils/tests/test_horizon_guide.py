from pathlib import Path

import pytest
from fpdf import FPDF

from app.utils.horizon_guide import (
    create_summary,
    download_programme_guide,
    parse_programme_guide,
    query_guide,
)



def generate_sample_pdf(path: Path) -> Path:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Call ID: HORIZON-423, Eligibility: open to all", ln=True)
    pdf.output(str(path))
    return path

def test_download_programme_guide_success(tmp_path, monkeypatch):
    class DummyResponse:
        status_code = 200
        content = b"pdf"

    def dummy_get(url, timeout=30):  # noqa: ARG001
        return DummyResponse()

    monkeypatch.setattr("requests.get", dummy_get)
    dest = tmp_path / "guide.pdf"
    path = download_programme_guide("http://example.com/guide.pdf", dest)
    assert path == dest
    assert dest.exists()

def test_download_programme_guide_fallback(tmp_path, monkeypatch, capsys):
    def dummy_get(url, timeout=30):  # noqa: ARG001
        raise Exception("network down")

    monkeypatch.setattr("requests.get", dummy_get)
    dest = tmp_path / "guide.pdf"
    path = download_programme_guide("http://example.com/guide.pdf", dest)
    captured = capsys.readouterr()
    assert path is None
    assert "Please download manually" in captured.out
    assert not dest.exists()

def test_parse_and_query(tmp_path):
    pdf_path = generate_sample_pdf(tmp_path / "sample.pdf")
    sections = parse_programme_guide(pdf_path)
    assert "Call" in sections
    summary_path = tmp_path / "summary.md"
    create_summary(pdf_path, summary_path)
    assert summary_path.exists()
    snippet = query_guide("HORIZON-423", pdf_path)
    assert "Eligibility" in snippet
