"""
Email Intelligence Module: MX Server Classification, SPF/DKIM/DMARC Security Audits, & Pattern Heuristics.
"""

import re
from typing import Dict, Any, List
from ..utils.dns_client import query_dns_records

def classify_email_provider(mx_records: List[str]) -> str:
    """Identify corporate email infrastructure from MX record hostnames."""
    mx_str = " ".join(mx_records).lower()
    
    if "google" in mx_str or "aspmx" in mx_str:
        return "Google Workspace (Gmail for Business)"
    elif "outlook" in mx_str or "microsoft" in mx_str or "pphosted" in mx_str:
        return "Microsoft 365 / Exchange Online"
    elif "zoho" in mx_str:
        return "Zoho Mail"
    elif "protonmail" in mx_str or "proton" in mx_str:
        return "ProtonMail Professional"
    elif "mimecast" in mx_str:
        return "Mimecast Secure Gateway"
    elif "barracuda" in mx_str:
        return "Barracuda Email Security"
    elif "sendgrid" in mx_str:
        return "Twilio SendGrid"
    elif "amazonses" in mx_str or "aws" in mx_str:
        return "Amazon SES"
    elif "mailgun" in mx_str:
        return "Mailgun"
    elif "ovh" in mx_str:
        return "OVHcloud Mail"
    elif len(mx_records) > 0:
        return f"Self-Hosted / Custom Gateway ({mx_records[0].split()[-1]})"
    return "No MX Records Detected (Inbound Email Disabled)"

def parse_spf_record(txt_records: List[str]) -> Dict[str, Any]:
    """Inspect SPF record configuration."""
    for txt in txt_records:
        if txt.startswith("v=spf1") or "v=spf1" in txt:
            policy = "Neutral (?all)"
            if "-all" in txt:
                policy = "Strict Hardfail (-all) - High Security"
            elif "~all" in txt:
                policy = "Softfail (~all) - Standard Protection"
            elif "+all" in txt:
                policy = "Dangerous (+all) - Allows All Senders!"

            return {
                "configured": True,
                "record": txt,
                "policy": policy,
                "is_secure": "-all" in txt or "~all" in txt
            }
            
    return {
        "configured": False,
        "record": None,
        "policy": "Missing SPF Record (Vulnerable to spoofing)",
        "is_secure": False
    }

def parse_dmarc_record(domain: str) -> Dict[str, Any]:
    """Query and parse _dmarc record."""
    dmarc_records = query_dns_records(f"_dmarc.{domain}", "TXT")
    
    for txt in dmarc_records:
        if txt.startswith("v=DMARC1") or "v=DMARC1" in txt:
            policy_match = re.search(r"p=(reject|quarantine|none)", txt, re.I)
            policy = policy_match.group(1).lower() if policy_match else "none"
            
            rua_match = re.search(r"rua=mailto:([^; ]+)", txt, re.I)
            rua = rua_match.group(1) if rua_match else None
            
            pct_match = re.search(r"pct=(\d+)", txt, re.I)
            pct = pct_match.group(1) if pct_match else "100"

            policy_desc = {
                "reject": "Reject (100% Drops Unauthenticated Emails - Maximum Security)",
                "quarantine": "Quarantine (Routes spoofed emails to Spam Folder)",
                "none": "Monitoring Only (p=none - Alerts only, does not block spoofing)"
            }.get(policy, policy)

            return {
                "configured": True,
                "record": txt,
                "policy": policy,
                "policy_description": policy_desc,
                "reporting_email": rua,
                "percentage": pct,
                "is_enforced": policy in ["reject", "quarantine"]
            }

    return {
        "configured": False,
        "record": None,
        "policy": "none",
        "policy_description": "Missing DMARC Record (No spoofing policy)",
        "reporting_email": None,
        "percentage": None,
        "is_enforced": False
    }

def probe_dkim_selectors(domain: str) -> List[str]:
    """Check common DKIM selector DNS records."""
    common_selectors = ["google", "default", "k1", "s1", "s2", "selector1", "mail", "smtp", "dkim", "mandrill", "zoho", "ms", "pro1"]
    active_selectors = []

    for sel in common_selectors:
        dkim_domain = f"{sel}._domainkey.{domain}"
        records = query_dns_records(dkim_domain, "TXT")
        for r in records:
            if "v=DKIM1" in r or "k=rsa" in r or "p=" in r:
                active_selectors.append(f"{sel} (Active)")
                break

    return active_selectors

def generate_email_patterns(domain: str) -> List[str]:
    """Generate standard corporate email address formats for lead enrichment."""
    return [
        f"first.last@{domain}",
        f"first@{domain}",
        f"firstl@{domain}",
        f"f.last@{domain}",
        f"first_last@{domain}",
        f"flast@{domain}"
    ]

def scan_email_intel(domain: str) -> Dict[str, Any]:
    """Execute complete email deliverability and security scan."""
    mx = query_dns_records(domain, "MX")
    txt = query_dns_records(domain, "TXT")
    
    provider = classify_email_provider(mx)
    spf = parse_spf_record(txt)
    dmarc = parse_dmarc_record(domain)
    dkim = probe_dkim_selectors(domain)
    patterns = generate_email_patterns(domain)

    # Deliverability health score
    score = 0
    if len(mx) > 0: score += 25
    if spf["configured"]: score += 25
    if dmarc["configured"]:
        score += 25 if dmarc["is_enforced"] else 15
    if len(dkim) > 0: score += 25

    return {
        "provider": provider,
        "mx_records": mx,
        "spf": spf,
        "dmarc": dmarc,
        "dkim_selectors": dkim,
        "email_patterns": patterns,
        "deliverability_score": score,
        "spoofing_protected": spf["is_secure"] and dmarc["is_enforced"]
    }
