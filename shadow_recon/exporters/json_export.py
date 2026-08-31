"""
JSON Exporter: Saves complete intelligence data as structured JSON file.
"""

import json
from typing import Dict, Any

def export_json(data: Dict[str, Any], filepath: str) -> str:
    """Save scan data to JSON file."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return filepath
