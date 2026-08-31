"""
Core Orchestration Engine: Runs all intelligence modules concurrently with robust error isolation.
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
from .modules.subdomain_scan import scan_subdomains
from .modules.ssl_audit import scan_ssl_tls
from .modules.header_analysis import analyze_security_headers
from .modules.social_recon import discover_social_links

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
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        print_step("Analyzing DNS, GeoIP, Tech Stack, Emails, Ports & Subdomains in parallel", "RUNNING")
        
        future_dns = executor.submit(scan_domain_intel, domain)
        future_comp = executor.submit(extract_company_intel, soup, resp, domain)
        future_tech = executor.submit(analyze_tech_stack, resp, soup)
        future_email = executor.submit(scan_email_intel, domain)
        future_ssl = executor.submit(scan_ssl_tls, domain)
        future_headers = executor.submit(analyze_security_headers, resp)
        future_socials = executor.submit(discover_social_links, soup, domain)
        future_subs = executor.submit(scan_subdomains, domain, quick)

        # Collect DNS first to get IP for GeoIP and Port Matrix
        try:
            results["domain_intel"] = future_dns.result(timeout=15)
        except Exception:
            results["domain_intel"] = {}

        primary_ip = results.get("domain_intel", {}).get("primary_ip")

        # Launch GeoIP and Port Scan using primary IP
        future_geo = executor.submit(scan_geoip, primary_ip)
        future_ports = executor.submit(scan_port_matrix, primary_ip)

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
            results["subdomains"] = future_subs.result(timeout=25)
        except Exception:
            results["subdomains"] = []

    elapsed = time.time() - start_time
    results["scan_duration_seconds"] = round(elapsed, 2)
    print_step("All intelligence vectors correlated successfully", "DONE")

    return results
