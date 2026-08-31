"""
Core Orchestration Engine: Runs all intelligence modules concurrently with robust error isolation.
"""

import time
import concurrent.futures
from typing import Dict, Any, Optional

from .utils.helpers import print_step, Colors, cprint
from .utils.http_client import fetch_domain_html
from .modules.domain_intel import scan_domain_intel
from .modules.tech_stack import analyze_tech_stack
from .modules.email_intel import scan_email_intel
from .modules.subdomain_scan import scan_subdomains
from .modules.ssl_audit import scan_ssl_tls
from .modules.header_analysis import analyze_security_headers
from .modules.social_recon import discover_social_links

def run_recon_scan(domain: str, quick: bool = False, verbose: bool = False) -> Dict[str, Any]:
    """
    Execute full reconnaissance scan across all 7 intelligence modules.
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

    # Step 2: Concurrently execute independent scanning modules
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        print_step("Analyzing DNS, MX, SSL, Tech Stack & Subdomains in parallel", "RUNNING")
        
        future_dns = executor.submit(scan_domain_intel, domain)
        future_tech = executor.submit(analyze_tech_stack, resp, soup)
        future_email = executor.submit(scan_email_intel, domain)
        future_ssl = executor.submit(scan_ssl_tls, domain)
        future_headers = executor.submit(analyze_security_headers, resp)
        future_socials = executor.submit(discover_social_links, soup, domain)
        future_subs = executor.submit(scan_subdomains, domain, quick)

        # Collect results with graceful error recovery
        try:
            results["domain_intel"] = future_dns.result(timeout=15)
        except Exception as e:
            if verbose: cprint(f"DNS Intel Error: {e}", Colors.RED)
            results["domain_intel"] = {}

        try:
            results["tech_stack"] = future_tech.result(timeout=10)
        except Exception as e:
            if verbose: cprint(f"Tech Stack Error: {e}", Colors.RED)
            results["tech_stack"] = {}

        try:
            results["email_intel"] = future_email.result(timeout=15)
        except Exception as e:
            if verbose: cprint(f"Email Intel Error: {e}", Colors.RED)
            results["email_intel"] = {}

        try:
            results["ssl_tls"] = future_ssl.result(timeout=10)
        except Exception as e:
            if verbose: cprint(f"SSL TLS Error: {e}", Colors.RED)
            results["ssl_tls"] = {}

        try:
            results["header_analysis"] = future_headers.result(timeout=5)
        except Exception as e:
            if verbose: cprint(f"Header Analysis Error: {e}", Colors.RED)
            results["header_analysis"] = {}

        try:
            results["social_recon"] = future_socials.result(timeout=5)
        except Exception as e:
            if verbose: cprint(f"Social Recon Error: {e}", Colors.RED)
            results["social_recon"] = {}

        try:
            results["subdomains"] = future_subs.result(timeout=30)
        except Exception as e:
            if verbose: cprint(f"Subdomains Error: {e}", Colors.RED)
            results["subdomains"] = []

    elapsed = time.time() - start_time
    results["scan_duration_seconds"] = round(elapsed, 2)
    print_step("All intelligence vectors correlated successfully", "DONE")

    return results
