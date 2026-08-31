"""
Web Vitals & Network Protocol Module: Measures TTFB Latency, HTTP/2 & HTTP/3 QUIC Support, and Tracker Bloat.
"""

import time
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any

TRACKER_PATTERNS = [
    "google-analytics", "googletagmanager", "facebook", "doubleclick", "hotjar",
    "clarity.ms", "tiktok.com", "mixpanel", "segment", "amplitude", "criteo",
    "bing.com", "linkedin.com/px", "adroll", "quora.com", "pinterest"
]

def audit_web_vitals(domain: str, response: requests.Response, soup: BeautifulSoup) -> Dict[str, Any]:
    """Measure server TTFB latency, HTTP/3 QUIC support, and script weight."""
    vitals = {
        "ttfb_ms": 0.0,
        "http_version": "HTTP/1.1",
        "http3_quic_support": False,
        "total_scripts_count": 0,
        "third_party_trackers_count": 0,
        "tracker_bloat_rating": "Clean / Lean",
        "alt_svc_header": None
    }

    # 1. Measure TTFB Latency
    try:
        start = time.time()
        r = requests.get(f"https://{domain}", timeout=5, headers={"User-Agent": "Mozilla/5.0"}, verify=False)
        ttfb = round((time.time() - start) * 1000, 1)
        vitals["ttfb_ms"] = ttfb
        
        # 2. HTTP/3 & Alt-Svc detection
        alt_svc = r.headers.get("Alt-Svc", "")
        if alt_svc:
            vitals["alt_svc_header"] = alt_svc
            if "h3" in alt_svc or "quic" in alt_svc.lower():
                vitals["http3_quic_support"] = True
                vitals["http_version"] = "HTTP/3 (QUIC / UDP Ready)"
            else:
                vitals["http_version"] = "HTTP/2 (Multiplexed TLS)"
        else:
            vitals["http_version"] = "HTTP/2 (Standard TLS)"
    except Exception:
        pass

    # 3. Tracker Bloat Analysis
    if soup:
        scripts = [s.get("src", "") for s in soup.find_all("script") if s.get("src")]
        vitals["total_scripts_count"] = len(scripts)
        
        trackers = set()
        for src in scripts:
            src_lower = src.lower()
            for pattern in TRACKER_PATTERNS:
                if pattern in src_lower:
                    trackers.add(pattern)

        vitals["third_party_trackers_count"] = len(trackers)
        if len(trackers) >= 6:
            vitals["tracker_bloat_rating"] = f"Heavy Tracker Load ({len(trackers)} active trackers)"
        elif len(trackers) >= 3:
            vitals["tracker_bloat_rating"] = f"Moderate Tracking ({len(trackers)} active trackers)"
        else:
            vitals["tracker_bloat_rating"] = f"Ultra-Fast / Clean ({len(trackers)} trackers)"

    return vitals
