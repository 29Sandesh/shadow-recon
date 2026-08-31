"""
CSV Exporter: Saves single or bulk domain intelligence rows to CSV for spreadsheet tools.
"""

import csv
import os
from typing import Dict, Any, List

CSV_COLUMNS = [
    "Domain",
    "Primary IP",
    "Hosting Provider",
    "Registrar",
    "Domain Age",
    "Nameservers",
    "Frontend Tech",
    "CSS Tech",
    "CMS Tech",
    "Backend Tech",
    "Analytics Tech",
    "Payments Tech",
    "Email Provider",
    "SPF Status",
    "DMARC Policy",
    "Likely Email Pattern",
    "Subdomains Count",
    "SSL Issuer",
    "SSL Days Remaining",
    "Security Score",
    "Security Grade",
    "LinkedIn URL",
    "Twitter URL",
    "GitHub URL"
]

def format_domain_csv_row(data: Dict[str, Any]) -> List[str]:
    """Convert scan dict into a flat CSV row."""
    dns = data.get("domain_intel", {})
    tech = data.get("tech_stack", {})
    email = data.get("email_intel", {})
    subs = data.get("subdomains", [])
    ssl_data = data.get("ssl_tls", {})
    sec = data.get("header_analysis", {})
    soc = data.get("social_recon", {})

    return [
        data.get("domain", ""),
        dns.get("primary_ip", ""),
        dns.get("hosting_provider", ""),
        dns.get("registrar", ""),
        dns.get("domain_age", ""),
        "; ".join(dns.get("nameservers", [])),
        "; ".join(tech.get("frontend", [])),
        "; ".join(tech.get("css_ui", [])),
        "; ".join(tech.get("cms_ecommerce", [])),
        "; ".join(tech.get("backend_server", [])),
        "; ".join(tech.get("analytics", [])),
        "; ".join(tech.get("payments", [])),
        email.get("provider", ""),
        "Configured" if email.get("spf", {}).get("configured") else "Missing",
        email.get("dmarc", {}).get("policy", "None"),
        email.get("email_patterns", [""])[0] if email.get("email_patterns") else "",
        str(len(subs)),
        ssl_data.get("issuer", ""),
        str(ssl_data.get("days_remaining", "")),
        str(sec.get("score", 0)),
        sec.get("grade", "F"),
        soc.get("linkedin", "") or "",
        soc.get("twitter", "") or "",
        soc.get("github", "") or ""
    ]

def export_csv(records: List[Dict[str, Any]], filepath: str) -> str:
    """Export single or multiple domain scans into a CSV file."""
    write_header = not os.path.exists(filepath)
    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(CSV_COLUMNS)
        for rec in records:
            writer.writerow(format_domain_csv_row(rec))
    return filepath
