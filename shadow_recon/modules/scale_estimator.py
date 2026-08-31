"""
B2B Tech Spend & Company Scale Estimator: Calibrated infrastructure cost estimation based on verified hosting tiers and detected SaaS.
"""

from typing import Dict, Any, List

ENTERPRISE_SIGNATURES = ["Datadog", "Segment", "Salesforce", "Marketo", "Workday", "Okta", "Snowflake", "Akamai Technologies", "Amazon CloudFront"]
MIDMARKET_SIGNATURES = ["HubSpot", "Intercom", "Mixpanel", "Amplitude", "Zendesk", "Sentry", "Stripe", "Next.js", "Google Tag Manager"]
STARTUP_SIGNATURES = ["Supabase", "PostHog", "Vercel", "Resend", "Tailwind CSS", "React (SPA)", "Vite Bundler", "Lemon Squeezy", "Render Platform", "Fly.io"]
BUDGET_HOSTING = ["hostinger", "godaddy", "namecheap", "bluehost", "ovh", "hetzner", "cpanel", "vps", "digitalocean", "linode"]

def estimate_company_scale(tech_data: Dict[str, Any], dns_data: Dict[str, Any], subs_data: List[Dict[str, Any]], email_data: Dict[str, Any]) -> Dict[str, Any]:
    """Compute realistic company scale and monthly tech spend using hosting infrastructure classification."""
    all_techs = []
    for cat_list in tech_data.values():
        if isinstance(cat_list, list):
            all_techs.extend(cat_list)

    tech_set = set(all_techs)
    subs_count = len(subs_data)
    hosting_provider = dns_data.get("hosting_provider", "").lower()
    mail_provider = email_data.get("provider", "")

    ent_matches = tech_set.intersection(ENTERPRISE_SIGNATURES)
    mid_matches = tech_set.intersection(MIDMARKET_SIGNATURES)
    start_matches = tech_set.intersection(STARTUP_SIGNATURES)

    # 1. Check if hosted on Budget / VPS / Hostinger / Lean infrastructure
    is_budget_infra = any(bh in hosting_provider for bh in BUDGET_HOSTING) or "hostinger" in str(dns_data)

    if is_budget_infra and len(ent_matches) == 0:
        # Lean Bootstrapped or Small Team (e.g. Axipays on Hostinger VPS)
        tier = "Bootstrapped / Lean Startup"
        emp_range = "10 – 35 Team Members"
        saas_spend = "$300 – $1,200 / mo"
        confidence = "Verified (Lean VPS infrastructure & essential cloud stack)"
        
    elif len(ent_matches) >= 2 or ("aws" in hosting_provider and "microsoft 365" in mail_provider.lower() and subs_count >= 15):
        # Major Enterprise (e.g. Stripe, Netflix)
        tier = "Enterprise Tier"
        emp_range = "500 – 5,000+ Employees"
        saas_spend = "$30,000 – $150,000+ / mo"
        confidence = "High (Enterprise observability & multi-cloud architecture)"

    elif len(mid_matches) >= 2 or ("vercel" in hosting_provider and len(tech_set) >= 4):
        # Growth / Funded Scaleup
        tier = "Funded Scaleup / Growth"
        emp_range = "30 – 100 Employees"
        saas_spend = "$2,500 – $10,000 / mo"
        confidence = "Moderate (Modern serverless edge infrastructure)"

    else:
        # General Boutique / Small Business
        tier = "Small Business / Startup"
        emp_range = "5 – 25 Team Members"
        saas_spend = "$200 – $1,000 / mo"
        confidence = "Standard (Standard cloud hosting & email setup)"

    return {
        "tier": tier,
        "estimated_employees": emp_range,
        "estimated_saas_budget": saas_spend,
        "confidence": confidence,
        "infrastructure_complexity": f"{len(tech_set)} Technologies | {subs_count} Subdomains"
    }
