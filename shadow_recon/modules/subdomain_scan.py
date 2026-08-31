"""
Subdomain Discovery & Takeover Audit Module: Certificate Transparency, DNS Brute, & Dangling CNAME Takeover Check.
"""

import requests
import concurrent.futures
from typing import List, Dict, Any, Set
from ..utils.dns_client import query_dns_records
from ..utils.http_client import probe_subdomain_status

COMMON_SUBDOMAINS = [
    "api", "admin", "app", "dashboard", "portal", "dev", "staging", "test", "beta", "docs",
    "status", "auth", "login", "sso", "mail", "webmail", "smtp", "vpn", "cdn", "static",
    "assets", "blog", "shop", "store", "billing", "pay", "checkout", "help", "support",
    "community", "forum", "internal", "corp", "hub", "connect", "ws", "graphql", "v1",
    "v2", "m", "mobile", "preview", "demo", "sandbox", "stage", "git", "jenkins", "jira"
]

TAKEOVER_SIGNATURES = {
    "github.io": "There isn't a GitHub Pages site here",
    "herokuapp.com": "No such app",
    "s3.amazonaws.com": "The specified bucket does not exist",
    "azurewebsites.net": "404 Web Site not found",
    "myshopify.com": "Sorry, this shop is currently unavailable",
    "surge.sh": "project not found",
    "tumblr.com": "There's nothing here",
    "ghost.io": "The thing you were looking for is no longer here",
    "zendesk.com": "Help Center Closed"
}

def query_cert_transparency(domain: str, timeout: int = 3) -> Set[str]:
    """Fetch subdomains recorded in Certificate Transparency logs."""
    discovered = set()
    try:
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        r = requests.get(url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            data = r.json()
            for entry in data:
                name_val = entry.get("name_value", "")
                for sub in name_val.split("\n"):
                    sub = sub.strip().lower()
                    if "*" not in sub and sub.endswith(f".{domain}") and sub != domain:
                        discovered.add(sub)
    except Exception:
        pass

    if len(discovered) == 0:
        try:
            ht_url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
            r2 = requests.get(ht_url, timeout=timeout, headers={"User-Agent": "Mozilla/5.0"})
            if r2.status_code == 200 and "error" not in r2.text.lower():
                for line in r2.text.splitlines():
                    parts = line.split(",")
                    if parts and parts[0].endswith(f".{domain}"):
                        discovered.add(parts[0].strip().lower())
        except Exception:
            pass

    return discovered

def brute_force_subdomains(domain: str, max_workers: int = 25) -> Set[str]:
    """Multi-threaded DNS resolution against top common subdomain list."""
    live_subs = set()

    def check_sub(prefix: str):
        candidate = f"{prefix}.{domain}"
        a_rec = query_dns_records(candidate, "A")
        cname_rec = query_dns_records(candidate, "CNAME")
        if a_rec or cname_rec:
            return candidate
        return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(check_sub, prefix): prefix for prefix in COMMON_SUBDOMAINS}
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res:
                live_subs.add(res)

    return live_subs

def check_subdomain_takeover(subdomain: str, cnames: List[str], status_code: int) -> bool:
    """Check if subdomain CNAME points to an unclaimed cloud service."""
    cname_str = " ".join(cnames).lower()
    for provider_host, error_fingerprint in TAKEOVER_SIGNATURES.items():
        if provider_host in cname_str and status_code == 404:
            return True
    return False

def scan_subdomains(domain: str, quick_mode: bool = False, max_probe_workers: int = 15) -> List[Dict[str, Any]]:
    """Execute complete subdomain reconnaissance and HTTP status probing."""
    all_subdomains = set()

    # 1. CT logs & APIs
    ct_subs = query_cert_transparency(domain)
    all_subdomains.update(ct_subs)

    # 2. DNS Brute force
    if not quick_mode or len(all_subdomains) < 5:
        brute_subs = brute_force_subdomains(domain)
        all_subdomains.update(brute_subs)

    sorted_subs = sorted(list(all_subdomains))[:25]

    # 3. HTTP Probe for live status and page titles
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_probe_workers) as executor:
        future_map = {executor.submit(probe_subdomain_status, sub): sub for sub in sorted_subs}
        for future in concurrent.futures.as_completed(future_map):
            try:
                probe_res = future.result()
                cnames = query_dns_records(probe_res["subdomain"], "CNAME")
                probe_res["cnames"] = cnames
                probe_res["takeover_vulnerable"] = check_subdomain_takeover(probe_res["subdomain"], cnames, probe_res.get("status_code", 0))
                results.append(probe_res)
            except Exception:
                pass

    results.sort(key=lambda x: (not x.get("is_live", False), x.get("status_code") or 999))
    return results
