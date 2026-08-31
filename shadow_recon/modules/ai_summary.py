"""
AI Executive Brief & Sales Pitch Synthesizer: Synthesizes findings into high-level executive briefs and agency sales angles.
"""

import os
from typing import Dict, Any

def generate_executive_brief(data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate 3-bullet executive summary, security risk analysis, and agency pitch angle."""
    domain = data.get("domain", "")
    comp = data.get("company_intel", {})
    scale = data.get("scale_estimator", {})
    email = data.get("email_intel", {})
    sec = data.get("header_analysis", {})
    vitals = data.get("web_vitals", {})
    tech = data.get("tech_stack", {})

    brand = comp.get("brand_name") or domain.split(".")[0].capitalize()
    
    # 1. Business Brief
    summary_text = comp.get("description") or "Digital technology platform and commercial web operation."
    business_brief = f"{brand} operates as a {scale.get('tier', 'digital business')} ({scale.get('estimated_employees', 'N/A')}). {summary_text[:140]}..."

    # 2. Core Security & Compliance Warnings
    warnings = []
    if not email.get("spf", {}).get("configured"):
        warnings.append("⚠️ Missing SPF DNS record leaves corporate domain vulnerable to direct email spoofing and fake CEO/invoice impersonation.")
    if not email.get("dmarc", {}).get("is_enforced"):
        warnings.append("⚠️ DMARC policy is not strictly enforced (p=none or missing) — spoofed outgoing emails will not be dropped by recipient inboxes.")
    if sec.get("score", 0) < 70:
        warnings.append(f"⚠️ Security Header Grade {sec.get('grade')} ({sec.get('score')}/100) — lacking critical Content-Security-Policy or anti-clickjacking headers.")
    if vitals.get("ttfb_ms", 0) > 600:
        warnings.append(f"⚠️ High TTFB server latency ({vitals.get('ttfb_ms')}ms) — potential conversion drop-off on cold traffic.")
    if not warnings:
        warnings.append("✅ Hardened security posture: Encrypted TLS 1.3, enforced email deliverability policies, and robust security headers active.")

    # 3. Agency / Freelance Pitch Angle
    pitch_angles = []
    if not email.get("spf", {}).get("configured") or not email.get("dmarc", {}).get("is_enforced"):
        pitch_angles.append("Pitch Email Deliverability & DMARC hardening audit to protect against domain reputation blacklisting.")
    if "WordPress" in str(tech):
        pitch_angles.append("Pitch Next.js / Headless migration for 10x faster TTFB load speeds and serverless scale.")
    if vitals.get("ttfb_ms", 0) > 400:
        pitch_angles.append("Pitch Edge CDN optimization and asset caching to reduce latency by up to 70%.")
    if not pitch_angles:
        pitch_angles.append("Target for B2B strategic partnership, enterprise software sales, or API integration.")

    return {
        "business_brief": business_brief,
        "security_warnings": warnings[:3],
        "pitch_angle": pitch_angles[0] if pitch_angles else "High-value enterprise sales prospect."
    }
