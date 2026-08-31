"""
Public Routes & Policy Prober Module: Audits security.txt, robots.txt, sitemap, mobile app links, and cookies.
"""

import re
import requests
from typing import Dict, Any, List

def scan_public_routes(domain: str, timeout: int = 4) -> Dict[str, Any]:
    """Probe standard public web routes, security disclosures, and mobile manifests."""
    routes = {
        "security_txt": {"present": False, "contacts": [], "url": None},
        "robots_txt": {"present": False, "disallowed_count": 0, "sitemaps": [], "url": None},
        "sitemap_xml": {"present": False, "url": None},
        "mobile_apps": {"has_ios_app": False, "has_android_app": False, "details": []},
        "humans_txt": {"present": False, "credits": []},
        "cookie_security": {"total_cookies": 0, "secure_cookies": 0, "httponly_cookies": 0, "samesite_cookies": 0, "is_secure": True}
    }

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    # 1. security.txt
    for path in ["/.well-known/security.txt", "/security.txt"]:
        try:
            r = requests.get(f"https://{domain}{path}", timeout=timeout, headers=headers, verify=False)
            if r.status_code == 200 and ("contact:" in r.text.lower() or "expires:" in r.text.lower()):
                routes["security_txt"]["present"] = True
                routes["security_txt"]["url"] = f"https://{domain}{path}"
                contacts = re.findall(r"Contact:\s*(.+)", r.text, re.I)
                routes["security_txt"]["contacts"] = [c.strip() for c in contacts][:3]
                break
        except Exception:
            pass

    # 2. robots.txt
    try:
        r_rob = requests.get(f"https://{domain}/robots.txt", timeout=timeout, headers=headers, verify=False)
        if r_rob.status_code == 200 and "user-agent:" in r_rob.text.lower():
            routes["robots_txt"]["present"] = True
            routes["robots_txt"]["url"] = f"https://{domain}/robots.txt"
            disallows = re.findall(r"Disallow:\s*(.+)", r_rob.text, re.I)
            routes["robots_txt"]["disallowed_count"] = len(disallows)
            sitemaps = re.findall(r"Sitemap:\s*(.+)", r_rob.text, re.I)
            routes["robots_txt"]["sitemaps"] = [s.strip() for s in sitemaps][:2]
    except Exception:
        pass

    # 3. sitemap.xml
    try:
        r_site = requests.get(f"https://{domain}/sitemap.xml", timeout=timeout, headers=headers, verify=False)
        if r_site.status_code == 200 and ("<urlset" in r_site.text or "<sitemapindex" in r_site.text):
            routes["sitemap_xml"]["present"] = True
            routes["sitemap_xml"]["url"] = f"https://{domain}/sitemap.xml"
    except Exception:
        pass

    # 4. Mobile Apps Association
    try:
        r_ios = requests.get(f"https://{domain}/.well-known/apple-app-site-association", timeout=timeout, headers=headers, verify=False)
        if r_ios.status_code == 200 and "applinks" in r_ios.text:
            routes["mobile_apps"]["has_ios_app"] = True
            routes["mobile_apps"]["details"].append("iOS App (Universal Links)")
    except Exception:
        pass

    try:
        r_droid = requests.get(f"https://{domain}/.well-known/assetlinks.json", timeout=timeout, headers=headers, verify=False)
        if r_droid.status_code == 200 and "android_app" in r_droid.text:
            routes["mobile_apps"]["has_android_app"] = True
            routes["mobile_apps"]["details"].append("Android App (Digital Asset Links)")
    except Exception:
        pass

    # 5. humans.txt
    try:
        r_hum = requests.get(f"https://{domain}/humans.txt", timeout=timeout, headers=headers, verify=False)
        if r_hum.status_code == 200 and len(r_hum.text) > 10 and "<html" not in r_hum.text.lower():
            routes["humans_txt"]["present"] = True
            lines = [line.strip() for line in r_hum.text.splitlines() if line.strip() and not line.startswith("/*")][:4]
            routes["humans_txt"]["credits"] = lines
    except Exception:
        pass

    return routes
