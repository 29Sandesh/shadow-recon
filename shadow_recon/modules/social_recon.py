"""
Social & Public Profile Reconnaissance Module: Discovers LinkedIn, Twitter/X, GitHub, YouTube, Discord, etc.
"""

import re
import json
from typing import Dict, Any, Optional
from bs4 import BeautifulSoup

def discover_social_links(soup: BeautifulSoup, domain: str) -> Dict[str, Optional[str]]:
    """Scan HTML anchor tags, meta tags, and JSON-LD schema to find social links."""
    socials = {
        "linkedin": None,
        "twitter": None,
        "github": None,
        "youtube": None,
        "facebook": None,
        "instagram": None,
        "discord": None,
        "crunchbase": None
    }

    if not soup:
        return socials

    # 1. Inspect JSON-LD 'sameAs' array
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            if not script.string:
                continue
            data = json.loads(script.string.strip())
            same_as = []
            if isinstance(data, dict):
                same_as = data.get("sameAs", [])
            elif isinstance(data, list):
                for d in data:
                    if isinstance(d, dict) and "sameAs" in d:
                        same_as.extend(d.get("sameAs", []))
            
            if isinstance(same_as, str):
                same_as = [same_as]
                
            for url in same_as:
                match_social_url(url, socials)
        except Exception:
            continue

    # 2. Inspect Meta Tags (e.g. twitter:site)
    for meta in soup.find_all("meta"):
        name = meta.get("name", "").lower()
        content = meta.get("content", "").strip()
        if name in ["twitter:site", "twitter:creator"] and content and not socials["twitter"]:
            handle = content.replace("@", "")
            socials["twitter"] = f"https://x.com/{handle}"

    # 3. Inspect Anchor Href Tags
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        match_social_url(href, socials)

    return socials

def match_social_url(href: str, socials: Dict[str, Optional[str]]):
    """Match and assign social link."""
    href_lower = href.lower()
    
    if "linkedin.com/company/" in href_lower and not socials["linkedin"]:
        socials["linkedin"] = clean_url(href)
    elif ("twitter.com/" in href_lower or "x.com/" in href_lower) and not socials["twitter"]:
        if not any(x in href_lower for x in ["intent", "share", "home", "privacy", "tos"]):
            socials["twitter"] = clean_url(href)
    elif "github.com/" in href_lower and not socials["github"]:
        if not any(x in href_lower for x in ["features", "pricing", "login", "signup", "about", "site"]):
            socials["github"] = clean_url(href)
    elif ("youtube.com/" in href_lower or "youtu.be/" in href_lower) and not socials["youtube"]:
        if not any(x in href_lower for x in ["watch", "embed"]):
            socials["youtube"] = clean_url(href)
    elif "facebook.com/" in href_lower and not socials["facebook"]:
        if not any(x in href_lower for x in ["sharer", "share", "dialog", "policy"]):
            socials["facebook"] = clean_url(href)
    elif "instagram.com/" in href_lower and not socials["instagram"]:
        socials["instagram"] = clean_url(href)
    elif ("discord.gg/" in href_lower or "discord.com/invite/" in href_lower) and not socials["discord"]:
        socials["discord"] = clean_url(href)
    elif "crunchbase.com/organization/" in href_lower and not socials["crunchbase"]:
        socials["crunchbase"] = clean_url(href)

def clean_url(url: str) -> str:
    """Strip query parameters from URL."""
    return url.split("?")[0].rstrip("/")
