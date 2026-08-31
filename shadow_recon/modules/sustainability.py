"""
Digital Sustainability & Carbon Footprint Module: Evaluates green hosting and estimated CO2 per request.
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, Any

GREEN_HOSTING_PROVIDERS = [
    "google", "gcp", "vercel", "cloudflare", "aws", "amazon", "microsoft", "azure", "hetzner", "ovh", "kinsta"
]

def audit_sustainability(domain: str, response: requests.Response, soup: BeautifulSoup, hosting_provider: str) -> Dict[str, Any]:
    """Calculate environmental sustainability metrics and page weight carbon footprint."""
    result = {
        "is_green_host": False,
        "hosting_compliance": "Standard Datacenter Grid",
        "page_size_kb": 0.0,
        "estimated_co2_grams": 0.0,
        "rating": "B"
    }

    # 1. Green Host Check
    h_lower = hosting_provider.lower()
    if any(p in h_lower for p in GREEN_HOSTING_PROVIDERS):
        result["is_green_host"] = True
        result["hosting_compliance"] = "Renewable Energy / Carbon-Neutral Cloud Provider"
    
    # 2. Calculate Page Payload Size
    html_bytes = len(response.content) if response else 0
    size_kb = round(html_bytes / 1024, 1)
    result["page_size_kb"] = size_kb

    # 3. Sustainable Web Design Model (Carbon Estimator)
    # Average ~0.2g to 0.8g CO2 per MB transferred
    co2_grams = round((size_kb / 1024.0) * 0.35, 3)
    result["estimated_co2_grams"] = max(co2_grams, 0.02)

    # 4. Sustainability Grade
    if result["is_green_host"] and size_kb < 150:
        result["rating"] = "A+ (Low Emissions)"
    elif result["is_green_host"] or size_kb < 300:
        result["rating"] = "A (Efficient)"
    elif size_kb < 800:
        result["rating"] = "B (Moderate)"
    else:
        result["rating"] = "C (High Data Weight)"

    return result
