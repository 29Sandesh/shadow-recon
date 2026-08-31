"""
HTTP Client Utility with retry logic, random user-agents, timeout handling, and HTML parsing.
"""

import random
import requests
import urllib3
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any, Tuple

# Suppress unverified HTTPS warnings for OSINT probing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14.6; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
]

def get_random_headers() -> Dict[str, str]:
    """Generate realistic browser headers."""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
    }

def fetch_domain_html(domain: str, timeout: int = 8) -> Tuple[Optional[requests.Response], Optional[BeautifulSoup], Optional[str]]:
    """
    Attempt to fetch target domain over HTTPS then HTTP.
    Returns (Response, BeautifulSoup, final_url) or (None, None, None) on failure.
    """
    schemes = [f"https://{domain}", f"http://{domain}"]
    session = requests.Session()
    session.headers.update(get_random_headers())

    for url in schemes:
        try:
            resp = session.get(url, timeout=timeout, allow_redirects=True, verify=False)
            soup = BeautifulSoup(resp.text, "html.parser")
            return resp, soup, resp.url
        except Exception:
            continue

    return None, None, None

def probe_subdomain_status(subdomain: str, timeout: int = 4) -> Dict[str, Any]:
    """
    Probes an individual subdomain to check HTTP status code, title, and redirects.
    """
    result = {
        "subdomain": subdomain,
        "is_live": False,
        "status_code": None,
        "title": None,
        "redirect_url": None,
        "server": None,
    }
    
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    for scheme in ["https", "http"]:
        url = f"{scheme}://{subdomain}"
        try:
            r = requests.get(url, timeout=timeout, headers=headers, allow_redirects=True, verify=False)
            result["is_live"] = True
            result["status_code"] = r.status_code
            result["server"] = r.headers.get("Server", "")
            if len(r.history) > 0:
                result["redirect_url"] = r.url
            
            # Extract title
            soup = BeautifulSoup(r.text[:50000], "html.parser")
            if soup.title and soup.title.string:
                clean_title = " ".join(soup.title.string.split()).strip()
                result["title"] = clean_title[:80]
            break
        except Exception:
            continue

    return result
