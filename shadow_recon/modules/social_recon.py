"""
Social & Public Profile Reconnaissance Module: Discovers company LinkedIn, Twitter/X, GitHub, & Crunchbase.
"""

import re
from typing import Dict, Any, Optional
from bs4 import BeautifulSoup

def discover_social_links(soup: BeautifulSoup, domain: str) -> Dict[str, Optional[str]]:
    """Scan HTML anchor tags to find official social media links."""
    socials = {
        "linkedin": None,
        "twitter": None,
        "github": None,
        "youtube": None,
        "facebook": None,
        "instagram": None,
        "crunchbase": None,
        "discord": None
    }

    if not soup:
        return socials

    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        
        if "linkedin.com/company/" in href and not socials["linkedin"]:
            socials["linkedin"] = clean_url(href)
        elif ("twitter.com/" in href or "x.com/" in href) and not socials["twitter"]:
            if not any(x in href for x in ["intent", "share", "home"]):
                socials["twitter"] = clean_url(href)
        elif "github.com/" in href and not socials["github"]:
            if not any(x in href for x in ["features", "pricing", "login", "signup"]):
                socials["github"] = clean_url(href)
        elif "youtube.com/" in href and not socials["youtube"]:
            if not any(x in href for x in ["watch", "embed"]):
                socials["youtube"] = clean_url(href)
        elif "facebook.com/" in href and not socials["facebook"]:
            if not any(x in href for x in ["sharer", "share", "dialog"]):
                socials["facebook"] = clean_url(href)
        elif "instagram.com/" in href and not socials["instagram"]:
            socials["instagram"] = clean_url(href)
        elif "crunchbase.com/organization/" in href and not socials["crunchbase"]:
            socials["crunchbase"] = clean_url(href)
        elif ("discord.gg/" in href or "discord.com/invite/" in href) and not socials["discord"]:
            socials["discord"] = clean_url(href)

    return socials

def clean_url(url: str) -> str:
    """Strip tracking query parameters from URL."""
    return url.split("?")[0].rstrip("/")
