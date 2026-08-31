"""
HTTP Header Security & Server Fingerprint Analysis: Computes a 0-100 Security Score with Grade.
"""

from typing import Dict, Any
import requests

SECURITY_HEADERS = {
    "Strict-Transport-Security": {"weight": 25, "desc": "Forces HTTPS connection (HSTS)"},
    "Content-Security-Policy": {"weight": 25, "desc": "Mitigates XSS and data injection attacks"},
    "X-Frame-Options": {"weight": 15, "desc": "Prevents Clickjacking UI redressing"},
    "X-Content-Type-Options": {"weight": 15, "desc": "Blocks MIME-type sniffing (nosniff)"},
    "Referrer-Policy": {"weight": 10, "desc": "Controls referrer data leaked in requests"},
    "Permissions-Policy": {"weight": 10, "desc": "Restricts browser APIs (camera, mic, geo)"}
}

def analyze_security_headers(response: requests.Response) -> Dict[str, Any]:
    """Audit HTTP security headers and compute weighted score (0-100)."""
    headers = {k.lower(): v for k, v in response.headers.items()} if response else {}
    
    audit_results = {}
    total_score = 0

    for header_name, config in SECURITY_HEADERS.items():
        h_lower = header_name.lower()
        present = h_lower in headers
        value = headers.get(h_lower, None)
        
        if present:
            total_score += config["weight"]

        audit_results[header_name] = {
            "present": present,
            "value": value,
            "description": config["desc"],
            "weight": config["weight"]
        }

    # Assign Letter Grade
    if total_score >= 90:
        grade = "A+"
    elif total_score >= 80:
        grade = "A"
    elif total_score >= 65:
        grade = "B"
    elif total_score >= 50:
        grade = "C"
    elif total_score >= 35:
        grade = "D"
    else:
        grade = "F"

    # Server banner
    server_banner = headers.get("server", "Hidden / Not Disclosed")

    return {
        "score": total_score,
        "grade": grade,
        "headers": audit_results,
        "server_banner": server_banner
    }
