"""
Enterprise Email Security & DNSSEC Audit Module: BIMI, MTA-STS, TLS-RPT, and DNSSEC validation.
"""

from typing import Dict, Any, List
from ..utils.dns_client import query_dns_records

def scan_enterprise_email_protocols(domain: str) -> Dict[str, Any]:
    """Inspect advanced enterprise email protocols and DNS cryptographic signatures."""
    results = {
        "bimi": {"configured": False, "record": None, "logo_url": None},
        "mta_sts": {"configured": False, "record": None, "mode": None},
        "tls_rpt": {"configured": False, "record": None, "rua": None},
        "dnssec": {"enabled": False, "details": "Unsigned Zone (No DNSSEC signatures detected)"}
    }

    # 1. BIMI Record (Brand Indicators for Message Identification)
    bimi_records = query_dns_records(f"default._bimi.{domain}", "TXT")
    for r in bimi_records:
        if "v=bimi1" in r.lower():
            results["bimi"]["configured"] = True
            results["bimi"]["record"] = r
            # Extract SVG logo if present
            if "l=" in r:
                for part in r.split(";"):
                    if part.strip().startswith("l="):
                        results["bimi"]["logo_url"] = part.strip()[2:].strip()
            break

    # 2. MTA-STS Record (Strict Transport Security for SMTP)
    mta_records = query_dns_records(f"_mta-sts.{domain}", "TXT")
    for r in mta_records:
        if "v=stsv1" in r.lower() or "v=sts" in r.lower():
            results["mta_sts"]["configured"] = True
            results["mta_sts"]["record"] = r
            if "mode=enforce" in r.lower():
                results["mta_sts"]["mode"] = "Enforce (Strict TLS required)"
            elif "mode=testing" in r.lower():
                results["mta_sts"]["mode"] = "Testing (Monitoring only)"
            break

    # 3. TLS-RPT Record (SMTP TLS Reporting)
    tls_rpt_records = query_dns_records(f"_smtp._tls.{domain}", "TXT")
    for r in tls_rpt_records:
        if "v=tlsrptv1" in r.lower() or "v=tlsrpt" in r.lower():
            results["tls_rpt"]["configured"] = True
            results["tls_rpt"]["record"] = r
            for part in r.split(";"):
                if "rua=mailto:" in part.lower():
                    results["tls_rpt"]["rua"] = part.strip().split("mailto:")[-1]
            break

    # 4. DNSSEC (DNS Security Extensions check)
    dnskey_records = query_dns_records(domain, "DNSKEY")
    rrsig_records = query_dns_records(domain, "RRSIG")
    if dnskey_records or rrsig_records:
        results["dnssec"]["enabled"] = True
        results["dnssec"]["details"] = "Cryptographically Signed (DNSSEC Active)"

    return results
