"""
Competitor Intelligence & Side-by-Side Diff Engine: Executes simultaneous multi-domain evaluations and builds comparative matrices.
"""

import concurrent.futures
from typing import Dict, Any, Tuple
from ..utils.helpers import Colors, cprint
from ..engine import run_recon_scan

def run_competitor_diff(domain1: str, domain2: str) -> Dict[str, Any]:
    """Execute dual scans and produce a side-by-side comparative evaluation."""
    cprint(f"\n[*] Initiating Side-by-Side Assessment: {Colors.CYAN}{domain1}{Colors.RESET} vs {Colors.CYAN}{domain2}{Colors.RESET}", Colors.YELLOW)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        f1 = executor.submit(run_recon_scan, domain1, True, False)
        f2 = executor.submit(run_recon_scan, domain2, True, False)
        data1 = f1.result()
        data2 = f2.result()

    return {
        "domain1": data1,
        "domain2": data2
    }

def print_diff_report(diff_data: Dict[str, Any]):
    """Render executive side-by-side terminal comparison."""
    d1 = diff_data["domain1"]
    d2 = diff_data["domain2"]
    
    name1 = d1.get("domain", "Domain A")
    name2 = d2.get("domain", "Domain B")

    score1 = d1.get("header_analysis", {}).get("score", 0)
    score2 = d2.get("header_analysis", {}).get("score", 0)
    
    grade1 = d1.get("header_analysis", {}).get("grade", "F")
    grade2 = d2.get("header_analysis", {}).get("grade", "F")

    ttfb1 = d1.get("web_vitals", {}).get("ttfb_ms", 0)
    ttfb2 = d2.get("web_vitals", {}).get("ttfb_ms", 0)

    scale1 = d1.get("scale_estimator", {}).get("tier", "N/A")
    scale2 = d2.get("scale_estimator", {}).get("tier", "N/A")

    host1 = d1.get("domain_intel", {}).get("hosting_provider", "N/A")
    host2 = d2.get("domain_intel", {}).get("hosting_provider", "N/A")

    subs1 = len(d1.get("subdomains", []))
    subs2 = len(d2.get("subdomains", []))

    age1 = d1.get("domain_intel", {}).get("domain_age", "N/A")
    age2 = d2.get("domain_intel", {}).get("domain_age", "N/A")

    techs1 = [t for sublist in d1.get("tech_stack", {}).values() if isinstance(sublist, list) for t in sublist]
    techs2 = [t for sublist in d2.get("tech_stack", {}).values() if isinstance(sublist, list) for t in sublist]

    print("")
    print(f"{Colors.CYAN}┌─ COMPARATIVE ANALYSIS MATRIX ──────────────────────────────────────────────────────────────────┐{Colors.RESET}")
    print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.BOLD}{'Metric / Property':<24}{Colors.RESET}│  {Colors.CYAN}{name1:<32}{Colors.RESET}│  {Colors.CYAN}{name2:<32}{Colors.RESET}{Colors.CYAN}│{Colors.RESET}")
    print(f"{Colors.CYAN}├─────────────────────────┼──────────────────────────────────┼──────────────────────────────────┤{Colors.RESET}")
    
    # Rows
    print_diff_row("Security Posture", f"{score1}/100 [Grade {grade1}]", f"{score2}/100 [Grade {grade2}]", score1 > score2, score2 > score1)
    print_diff_row("Response Latency (TTFB)", f"{ttfb1} ms", f"{ttfb2} ms", ttfb1 < ttfb2 and ttfb1 > 0, ttfb2 < ttfb1 and ttfb2 > 0)
    print_diff_row("Infrastructure Scale", f"{scale1[:30]}", f"{scale2[:30]}")
    print_diff_row("Hosting / Edge Network", f"{host1[:30]}", f"{host2[:30]}")
    print_diff_row("Public Subdomain Fleet", f"{subs1} discovered", f"{subs2} discovered", subs1 > subs2, subs2 > subs1)
    print_diff_row("Domain Age", f"{age1}", f"{age2}")
    print_diff_row("Tech Stack Complexity", f"{len(techs1)} Technologies", f"{len(techs2)} Technologies")
    print_diff_row("Primary Frontend", f"{', '.join(d1.get('tech_stack', {}).get('frontend', ['Custom']))[:30]}", f"{', '.join(d2.get('tech_stack', {}).get('frontend', ['Custom']))[:30]}")
    print_diff_row("Email Security", f"SPF: {d1.get('email_intel', {}).get('spf', {}).get('policy', 'None')[:16]}", f"SPF: {d2.get('email_intel', {}).get('spf', {}).get('policy', 'None')[:16]}")
    print_diff_row("SSL Valid Period", f"{d1.get('ssl_tls', {}).get('days_remaining', 0)} days remaining", f"{d2.get('ssl_tls', {}).get('days_remaining', 0)} days remaining")
    print(f"{Colors.CYAN}└─────────────────────────┴──────────────────────────────────┴──────────────────────────────────┘{Colors.RESET}")
    print("")

    # Executive Verdict
    v1_points = (1 if score1 > score2 else 0) + (1 if ttfb1 < ttfb2 and ttfb1 > 0 else 0) + (1 if subs1 > subs2 else 0)
    v2_points = (1 if score2 > score1 else 0) + (1 if ttfb2 < ttfb1 and ttfb2 > 0 else 0) + (1 if subs2 > subs1 else 0)

    winner = name1 if v1_points >= v2_points else name2
    print(f"{Colors.CYAN}=================================================================================================={Colors.RESET}")
    print(f"  {Colors.BOLD}{Colors.WHITE}EXECUTIVE VERDICT:{Colors.RESET} {Colors.GREEN}{winner}{Colors.RESET} demonstrates superior technical infrastructure & security posture.")
    print(f"{Colors.CYAN}=================================================================================================={Colors.RESET}")

def print_diff_row(label: str, val1: str, val2: str, win1: bool = False, win2: bool = False):
    """Print an aligned 3-column comparative row."""
    c1 = Colors.GREEN if win1 else Colors.WHITE
    c2 = Colors.GREEN if win2 else Colors.WHITE
    print(f"{Colors.CYAN}│{Colors.RESET}  {label:<23}│  {c1}{val1:<32}{Colors.RESET}│  {c2}{val2:<32}{Colors.RESET}{Colors.CYAN}│{Colors.RESET}")
