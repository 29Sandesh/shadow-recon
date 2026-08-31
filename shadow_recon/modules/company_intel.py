"""
Company Intelligence Module: Extracts Business Identity, Meta Descriptions, OpenGraph, JSON-LD Schema, Public Contact Inboxes, and Phone Numbers.
"""

import re
import json
from typing import Dict, Any, List, Set
from bs4 import BeautifulSoup
import requests

def extract_company_intel(soup: BeautifulSoup, response: requests.Response, domain: str) -> Dict[str, Any]:
    """Scrape and parse company metadata, descriptions, contact emails, and phone numbers."""
    intel = {
        "title": None,
        "tagline": None,
        "description": None,
        "brand_name": None,
        "public_emails": [],
        "phone_numbers": [],
        "keywords": [],
        "og_metadata": {}
    }

    if not soup:
        return intel

    # 1. Page Title & Brand Name
    if soup.title and soup.title.string:
        raw_title = " ".join(soup.title.string.split()).strip()
        intel["title"] = raw_title
        parts = re.split(r"[\s\-_\|•:]+", raw_title)
        if parts:
            intel["brand_name"] = parts[0] if len(parts[0]) > 2 else domain.split(".")[0].capitalize()

    # 2. Meta Descriptions & OpenGraph
    for meta in soup.find_all("meta"):
        name = meta.get("name", "").lower()
        prop = meta.get("property", "").lower()
        content = meta.get("content", "").strip()
        
        if not content:
            continue

        if name in ["description", "twitter:description"] and not intel["description"]:
            intel["description"] = content
        elif prop in ["og:description"] and not intel["description"]:
            intel["description"] = content
        elif prop in ["og:title"] and not intel["tagline"]:
            intel["tagline"] = content
        elif prop in ["og:site_name"] and not intel["brand_name"]:
            intel["brand_name"] = content
        elif name == "keywords":
            intel["keywords"] = [k.strip() for k in content.split(",") if k.strip()][:8]

        if prop.startswith("og:"):
            intel["og_metadata"][prop] = content

    # 3. JSON-LD Structured Data
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            if not script.string:
                continue
            data = json.loads(script.string.strip())
            if isinstance(data, list):
                for item in data:
                    process_json_ld(item, intel)
            elif isinstance(data, dict):
                process_json_ld(data, intel)
        except Exception:
            continue

    # 4. Harvest Public Operational Emails
    emails = set()
    html_text = str(soup)
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    raw_matches = re.findall(email_pattern, html_text)
    
    ignored_exts = (".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif", ".js", ".css")
    for em in raw_matches:
        em_clean = em.strip().lower()
        if not any(em_clean.endswith(ext) for ext in ignored_exts) and len(em_clean) <= 60:
            if domain in em_clean or any(k in em_clean for k in ["support", "sales", "contact", "info", "hello", "press", "media", "jobs", "careers", "security", "legal", "team"]):
                emails.add(em_clean)

    for a in soup.find_all("a", href=True):
        if a["href"].startswith("mailto:"):
            mailto_email = a["href"].replace("mailto:", "").split("?")[0].strip().lower()
            if re.match(email_pattern, mailto_email):
                emails.add(mailto_email)

    intel["public_emails"] = sorted(list(emails))[:8]

    # 5. Extract Phone Numbers
    phone_pattern = r'(?:\+?[0-9]{1,3}[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}'
    phone_matches = re.findall(phone_pattern, soup.get_text())
    clean_phones = set()
    for p in phone_matches:
        p_clean = p.strip()
        if len(re.sub(r'\D', '', p_clean)) >= 10:
            clean_phones.add(p_clean)
    intel["phone_numbers"] = sorted(list(clean_phones))[:4]

    return intel

def process_json_ld(data: Dict[str, Any], intel: Dict[str, Any]):
    """Extract organization details from JSON-LD schema."""
    schema_type = data.get("@type", "")
    if isinstance(schema_type, list):
        schema_type = " ".join(schema_type)
    
    if any(k in str(schema_type) for k in ["Organization", "Corporation", "Company", "LocalBusiness", "WebSite"]):
        if data.get("name") and not intel["brand_name"]:
            intel["brand_name"] = data["name"]
        if data.get("description") and not intel["description"]:
            intel["description"] = data["description"]
        if data.get("email"):
            em = data["email"]
            if isinstance(em, list):
                intel["public_emails"].extend(em)
            elif isinstance(em, str):
                intel["public_emails"].append(em)
        if data.get("telephone"):
            tel = data["telephone"]
            if isinstance(tel, list):
                intel["phone_numbers"].extend(tel)
            elif isinstance(tel, str):
                intel["phone_numbers"].append(tel)
