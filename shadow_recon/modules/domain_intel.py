"""
Domain Intelligence Module: DNS Records, WHOIS/RDAP Registration Info, Hosting & CDN Detection.
"""

import socket
import datetime
import requests
from typing import Dict, Any, List
from ..utils.dns_client import query_dns_records, resolve_ip_addresses, reverse_dns_lookup

def get_rdap_info(domain: str, timeout: int = 5) -> Dict[str, Any]:
    """Fetch structured domain registration data via RDAP API."""
    info = {
        "registrar": "Unknown / Private",
        "created_date": None,
        "expiry_date": None,
        "domain_age": None,
        "registrant_country": None,
        "status": []
    }
    
    try:
        url = f"https://rdap.org/domain/{domain}"
        r = requests.get(url, timeout=timeout, headers={"User-Agent": "ShadowRecon-OSINT/1.0"})
        if r.status_code == 200:
            data = r.json()
            # Statuses
            info["status"] = data.get("status", [])
            
            # Entities (Registrar)
            for entity in data.get("entities", []):
                roles = entity.get("roles", [])
                if "registrar" in roles:
                    vcard = entity.get("vcardArray", [])
                    if len(vcard) > 1:
                        for field in vcard[1]:
                            if field[0] == "fn":
                                info["registrar"] = field[3]
                                break
                                
            # Events (Created, Expiry)
            for event in data.get("events", []):
                action = event.get("eventAction")
                date_str = event.get("eventDate")
                if action == "registration" and date_str:
                    info["created_date"] = date_str[:10]
                    try:
                        created_dt = datetime.datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                        now = datetime.datetime.now(datetime.timezone.utc)
                        age_days = (now - created_dt).days
                        years = age_days // 365
                        months = (age_days % 365) // 30
                        info["domain_age"] = f"{years} years, {months} months" if years > 0 else f"{months} months ({age_days} days)"
                    except Exception:
                        pass
                elif action == "expiration" and date_str:
                    info["expiry_date"] = date_str[:10]
    except Exception:
        pass
        
    return info

def detect_hosting_provider(ips: List[str], nameservers: List[str], cnames: List[str]) -> str:
    """Identify CDN or cloud hosting provider based on IP PTR and NS records."""
    combined = (" ".join(nameservers) + " " + " ".join(cnames)).lower()
    
    for ip in ips:
        ptr = reverse_dns_lookup(ip)
        if ptr:
            combined += " " + ptr.lower()

    if "cloudflare" in combined:
        return "Cloudflare CDN & Edge"
    elif "vercel" in combined:
        return "Vercel Cloud Platform"
    elif "netlify" in combined:
        return "Netlify Hosting"
    elif "awsdns" in combined or "cloudfront" in combined or "amazon" in combined:
        return "Amazon Web Services (AWS / CloudFront)"
    elif "google" in combined or "googledomains" in combined or "1e100.net" in combined:
        return "Google Cloud Platform"
    elif "azure" in combined or "trafficmanager.net" in combined:
        return "Microsoft Azure Cloud"
    elif "fastly" in combined:
        return "Fastly CDN"
    elif "akamai" in combined:
        return "Akamai Technologies"
    elif "digitalocean" in combined:
        return "DigitalOcean Cloud"
    elif "fly.io" in combined or "fly.dev" in combined:
        return "Fly.io"
    elif "render.com" in combined or "render" in combined:
        return "Render Platform"
    elif "github.io" in combined:
        return "GitHub Pages"
        
    return "Dedicated / Custom VPS Hosting"

def scan_domain_intel(domain: str) -> Dict[str, Any]:
    """Execute complete domain intelligence scan."""
    a_records = query_dns_records(domain, "A")
    aaaa_records = query_dns_records(domain, "AAAA")
    mx_records = query_dns_records(domain, "MX")
    ns_records = query_dns_records(domain, "NS")
    txt_records = query_dns_records(domain, "TXT")
    cname_records = query_dns_records(domain, "CNAME")
    soa_records = query_dns_records(domain, "SOA")

    ips = a_records + aaaa_records
    primary_ip = a_records[0] if a_records else (aaaa_records[0] if aaaa_records else "None")
    
    rdap = get_rdap_info(domain)
    hosting = detect_hosting_provider(ips, ns_records, cname_records)

    return {
        "domain": domain,
        "primary_ip": primary_ip,
        "all_ips": ips,
        "nameservers": ns_records,
        "a_records": a_records,
        "aaaa_records": aaaa_records,
        "mx_records": mx_records,
        "txt_records": txt_records,
        "cname_records": cname_records,
        "soa_records": soa_records,
        "registrar": rdap.get("registrar"),
        "created_date": rdap.get("created_date"),
        "expiry_date": rdap.get("expiry_date"),
        "domain_age": rdap.get("domain_age"),
        "hosting_provider": hosting
    }
