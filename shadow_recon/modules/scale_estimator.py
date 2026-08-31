"""
B2B Tech Spend & Company Scale Estimator Module: Estimates employee count range, SaaS budget tier, and business maturity.
"""

from typing import Dict, Any, List

ENTERPRISE_SIGNATURES = ["Datadog", "Segment", "Salesforce", "Marketo", "Workday", "Okta", "Snowflake", "Akamai Technologies", "Amazon CloudFront"]
MIDMARKET_SIGNATURES = ["HubSpot", "Intercom", "Mixpanel", "Amplitude", "Zendesk", "Sentry", "Stripe", "Next.js", "Google Tag Manager"]
STARTUP_SIGNATURES = ["Supabase", "PostHog", "Vercel", "Resend", "Tailwind CSS", "React (SPA)", "Vite Bundler", "Lemon Squeezy", "Render Platform", "Fly.io"]

def estimate_company_scale(tech_data: Dict[str, Any], dns_data: Dict[str, Any], subs_data: List[Dict[str, Any]], email_data: Dict[str, Any]) -> Dict[str, Any]:
    """Compute estimated company size, monthly SaaS tech spend, and market maturity tier."""
    all_techs = []
    for cat_list in tech_data.values():
        if isinstance(cat_list, list):
            all_techs.extend(cat_list)

    tech_set = set(all_techs)
    subs_count = len(subs_data)
    domain_age_str = dns_data.get("domain_age", "")
    mail_provider = email_data.get("provider", "")

    # Calculate Enterprise Score
    ent_matches = tech_set.intersection(ENTERPRISE_SIGNATURES)
    mid_matches = tech_set.intersection(MIDMARKET_SIGNATURES)
    start_matches = tech_set.intersection(STARTUP_SIGNATURES)

    # Scale Tier Heuristic
    if len(ent_matches) >= 2 or subs_count >= 20 or "Microsoft 365" in mail_provider:
        tier = "Enterprise Tier"
        emp_range = "250 – 5,000+ Employees"
        saas_spend = "$25,000 – $150,000+ / mo"
        confidence = "High (Enterprise tooling & multi-subdomain asset fleet)"
    elif len(mid_matches) >= 2 or subs_count >= 8 or len(tech_set) >= 6:
        tier = "Growth / Mid-Market Scaleup"
        emp_range = "50 – 250 Employees"
        saas_spend = "$5,000 – $25,000 / mo"
        confidence = "High (Modern mid-market SaaS infrastructure)"
    elif len(start_matches) >= 2 or "Vercel" in dns_data.get("hosting_provider", ""):
        tier = "Venture Startup / Seed - Series A"
        emp_range = "5 – 50 Employees"
        saas_spend = "$1,000 – $5,000 / mo"
        confidence = "Moderate (High-velocity modern stack)"
    else:
        tier = "SMB / Boutique Operator"
        emp_range = "1 – 15 Employees"
        saas_spend = "$100 – $1,000 / mo"
        confidence = "Standard (Lean custom or boutique setup)"

    return {
        "tier": tier,
        "estimated_employees": emp_range,
        "estimated_saas_budget": saas_spend,
        "confidence": confidence,
        "infrastructure_complexity": f"{len(tech_set)} Technologies | {subs_count} Subdomains Detected"
    }
