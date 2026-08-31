"""
GeoIP & Network ASN Intelligence Module: Resolves Server Location, Country, City, ASN, and ISP.
"""

import requests
from typing import Dict, Any

def scan_geoip(ip: str, timeout: int = 4) -> Dict[str, Any]:
    """Resolve IP geolocation and ASN data."""
    geo = {
        "ip": ip,
        "country": "Unknown",
        "country_code": "UN",
        "region": "Unknown",
        "city": "Unknown",
        "isp": "Unknown",
        "org": "Unknown",
        "asn": "Unknown",
        "timezone": "Unknown",
        "flag": "🌐"
    }

    if not ip or ip in ["None", "127.0.0.1", "::1"]:
        return geo

    # Free high-reliability IP geolocation API
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,as"
        r = requests.get(url, timeout=timeout, headers={"User-Agent": "ShadowRecon/1.0"})
        if r.status_code == 200:
            data = r.json()
            if data.get("status") == "success":
                geo["country"] = data.get("country", "Unknown")
                geo["country_code"] = data.get("countryCode", "UN")
                geo["region"] = data.get("regionName", "Unknown")
                geo["city"] = data.get("city", "Unknown")
                geo["isp"] = data.get("isp", "Unknown")
                geo["org"] = data.get("org", "Unknown")
                geo["asn"] = data.get("as", "Unknown")
                geo["timezone"] = data.get("timezone", "Unknown")
                
                # Convert country code to emoji flag
                cc = data.get("countryCode", "")
                if len(cc) == 2:
                    geo["flag"] = "".join(chr(127397 + ord(c)) for c in cc.upper())
    except Exception:
        pass

    return geo
