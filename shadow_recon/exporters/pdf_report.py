"""
PDF / Print Audit Report Generator: Generates a high-res printable vector HTML document formatted as an executive client deliverable.
"""

from typing import Dict, Any
from .html_report import generate_html_report

def export_pdf_report(data: Dict[str, Any], filepath: str) -> str:
    """Generate high-resolution printable audit report."""
    if not filepath.endswith(".html") and not filepath.endswith(".pdf"):
        filepath += ".html"
    return generate_html_report(data, filepath)
