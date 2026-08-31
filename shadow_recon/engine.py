"""
Core Orchestration Engine: Runs all 14 intelligence modules concurrently.
"""

import time
import concurrent.futures
from typing import Dict, Any

from .utils.helpers import print_step, Colors, cprint
from .utils.http_client import fetch_domain_html
from .modules.company_intel import extract_company_intel
from .modules.geoip_intel import scan_geoip
from .modules.port_matrix import scan_port_matrix
from .modules.domain_intel import scan_domain_intel
from .modules.tech_stack import analyze_tech_stack
from .modules.email_intel import scan_email_intel
from .modules.enterprise_email import scan_enterprise_email_protocols
from .modules.sustainability import audit_sustainability
from .modules.subdomain_scan import scan_subdomains
from .modules.ssl_audit import scan_ssl_tls
from .modules.header_analysis import analyze_security_headers
from .modules.social_recon import discover_social_links
from .modules.routes_intel import scan_public_routes
from .modules.scale_estimator import estimate_company_scale
from .modules.web_vitals import audit_web_vitals
from .modules.ai_summary import generate_executive_brief

def run_recon_scan(domain: str, quick: bool = False, verbose: bool = False) -> Dict[str, Any]:
    """
    Execute full reconnaissance scan across all intelligence modules.
    Returns aggregated dictionary with complete findings.
    """
    start_time = time.time()
    
    print_step(f"Initiating reconnaissance on {Colors.CYAN}{domain}{Colors.RESET}", "INFO")

    # Step 1: Fetch Base HTML & Headers
    print_step("Fetching HTTP response headers and web source", "RUNNING")
    resp, soup, final_url = fetch_domain_html(domain)
    print_step("HTTP headers and HTML payload captured", "DONE")

    results = {
        "domain": domain,
        "final_url": final_url or f"https://{domain}",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "quick_mode": quick
    }

    # Step 2: Concurrently execute scanning modules
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        print_step("Correlating AI Brief, DNS, GeoIP, BIMI/MTA-STS, Vitals, Ports & Subdomains", "RUNNING")
        
        future_dns = executor.submit(scan_domain_intel, domain)
        future_comp = executor.submit(extract_company_intel, soup, resp, domain)
        future_tech = executor.submit(analyze_tech_stack, resp, soup)
        future_email = executor.submit(scan_email_intel, domain)
        future_ent_email = executor.submit(scan_enterprise_email_protocols, domain)
        future_ssl = executor.submit(scan_ssl_tls, domain)
        future_headers = executor.submit(analyze_security_headers, resp)
        future_socials = executor.submit(discover_social_links, soup, domain)
        future_routes = executor.submit(scan_public_routes, domain)
        future_vitals = executor.submit(audit_web_vitals, domain, resp, soup)
        future_subs = executor.submit(scan_subdomains, domain, quick)

        # Collect DNS first for IP
        try:
            results["domain_intel"] = future_dns.result(timeout=15)
        except Exception:
            results["domain_intel"] = {}

        primary_ip = results.get("domain_intel", {}).get("primary_ip")
        hosting_prov = results.get("domain_intel", {}).get("hosting_provider", "Dedicated")

        # Launch GeoIP and Port Scan using primary IP
        future_geo = executor.submit(scan_geoip, primary_ip)
        future_ports = executor.submit(scan_port_matrix, primary_ip)
        future_green = executor.submit(audit_sustainability, domain, resp, soup, hosting_prov)

        try:
            results["company_intel"] = future_comp.result(timeout=8)
        except Exception:
            results["company_intel"] = {}

        try:
            results["geoip"] = future_geo.result(timeout=5)
        except Exception:
            results["geoip"] = {}

        try:
            results["port_matrix"] = future_ports.result(timeout=6)
        except Exception:
            results["port_matrix"] = []

        try:
            results["tech_stack"] = future_tech.result(timeout=10)
        except Exception:
            results["tech_stack"] = {}

        try:
            results["email_intel"] = future_email.result(timeout=15)
        except Exception:
            results["email_intel"] = {}

        try:
            results["enterprise_email"] = future_ent_email.result(timeout=6)
        except Exception:
            results["enterprise_email"] = {}

        try:
            results["sustainability"] = future_green.result(timeout=4)
        except Exception:
            results["sustainability"] = {}

        try:
            results["ssl_tls"] = future_ssl.result(timeout=8)
        except Exception:
            results["ssl_tls"] = {}

        try:
            results["header_analysis"] = future_headers.result(timeout=5)
        except Exception:
            results["header_analysis"] = {}

        try:
            results["social_recon"] = future_socials.result(timeout=5)
        except Exception:
            results["social_recon"] = {}

        try:
            results["routes_intel"] = future_routes.result(timeout=8)
        except Exception:
            results["routes_intel"] = {}

        try:
            results["web_vitals"] = future_vitals.result(timeout=8)
        except Exception:
            results["web_vitals"] = {}

        try:
            results["subdomains"] = future_subs.result(timeout=25)
        except Exception:
            results["subdomains"] = []

    # Step 3: Compute Scale & AI Synthesis
    results["scale_estimator"] = estimate_company_scale(
        results.get("tech_stack", {}),
        results.get("domain_intel", {}),
        results.get("subdomains", []),
        results.get("email_intel", {})
    )

    results["ai_summary"] = generate_executive_brief(results)

    elapsed = time.time() - start_time
    results["scan_duration_seconds"] = round(elapsed, 2)
    print_step("All intelligence vectors correlated successfully", "DONE")

    return results
