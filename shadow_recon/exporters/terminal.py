"""
Terminal Pretty-Print Exporter: Outputs high-contrast colorized box-drawn tables.
"""

from typing import Dict, Any
from ..utils.helpers import Colors

def print_terminal_report(data: Dict[str, Any], scan_duration: float):
    """Render full formatted terminal report."""
    domain = data.get("domain", "Unknown")
    dns_data = data.get("domain_intel", {})
    tech_data = data.get("tech_stack", {})
    email_data = data.get("email_intel", {})
    subs_data = data.get("subdomains", [])
    ssl_data = data.get("ssl_tls", {})
    sec_headers = data.get("header_analysis", {})
    socials = data.get("social_recon", {})

    print("")
    
    # 1. DOMAIN INTELLIGENCE BOX
    print(f"{Colors.CYAN}┌─ DOMAIN INTELLIGENCE ────────────────────────────────────────────────────────┐{Colors.RESET}")
    print_row("IP Address", f"{dns_data.get('primary_ip', 'N/A')} ({dns_data.get('hosting_provider', 'N/A')})")
    print_row("Registrar", dns_data.get("registrar", "N/A"))
    print_row("Domain Age", dns_data.get("domain_age", "N/A"))
    
    ns_str = ", ".join(dns_data.get("nameservers", [])[:2]) if dns_data.get("nameservers") else "None"
    print_row("Nameservers", ns_str)
    print_row("Hosting", dns_data.get("hosting_provider", "N/A"))
    print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
    print("")

    # 2. TECH STACK BOX
    print(f"{Colors.CYAN}┌─ TECH STACK DETECTED ────────────────────────────────────────────────────────┐{Colors.RESET}")
    all_tech_empty = True
    for cat_name, label in [
        ("frontend", "Frontend"),
        ("css_ui", "CSS / UI"),
        ("cms_ecommerce", "CMS / Store"),
        ("backend_server", "Backend / Server"),
        ("analytics", "Analytics"),
        ("payments", "Payments"),
        ("support_chat", "Customer Chat"),
        ("monitoring_security", "Security / Mon")
    ]:
        techs = tech_data.get(cat_name, [])
        if techs:
            all_tech_empty = False
            print_row(label, f"{Colors.GREEN}{', '.join(techs)}{Colors.RESET}")
            
    if all_tech_empty:
        print_row("Status", f"{Colors.YELLOW}Custom built / No standard signatures matched{Colors.RESET}")
        
    print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
    print("")

    # 3. EMAIL INTELLIGENCE BOX
    print(f"{Colors.CYAN}┌─ EMAIL INTELLIGENCE ─────────────────────────────────────────────────────────┐{Colors.RESET}")
    print_row("Provider", email_data.get("provider", "N/A"))
    
    spf = email_data.get("spf", {})
    spf_badge = f"{Colors.GREEN}[Configured]{Colors.RESET}" if spf.get("configured") else f"{Colors.RED}[Missing]{Colors.RESET}"
    print_row("SPF Policy", f"{spf_badge} ({spf.get('policy', 'None')})")

    dmarc = email_data.get("dmarc", {})
    dmarc_badge = f"{Colors.GREEN}[Enforced]{Colors.RESET}" if dmarc.get("is_enforced") else f"{Colors.YELLOW}[{dmarc.get('policy_description', 'None')}]{Colors.RESET}"
    print_row("DMARC Policy", dmarc_badge)

    dkims = email_data.get("dkim_selectors", [])
    dkim_badge = f"{Colors.GREEN}[Active ({len(dkims)} found)]{Colors.RESET}" if len(dkims) > 0 else f"{Colors.GRAY}Not Disclosed{Colors.RESET}"
    print_row("DKIM Signing", dkim_badge)

    patterns = email_data.get("email_patterns", [])
    top_pat = patterns[0] if patterns else "None"
    print_row("Likely Pattern", f"{Colors.CYAN}{top_pat}{Colors.RESET}")
    print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
    print("")

    # 4. SUBDOMAINS DISCOVERY BOX
    print(f"{Colors.CYAN}┌─ SUBDOMAINS DISCOVERED ({len(subs_data)} found) ───────────────────────────────────────────┐{Colors.RESET}")
    if subs_data:
        for s in subs_data[:10]:
            sub_name = s.get("subdomain", "")
            code = s.get("status_code")
            code_str = f"[{code}]" if code else "[---]"
            code_color = Colors.GREEN if code in [200, 301, 302] else (Colors.RED if code in [403, 500] else Colors.GRAY)
            title = s.get("title") or s.get("server") or ""
            print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.WHITE}{sub_name:<30}{Colors.RESET} {code_color}{code_str:<6}{Colors.RESET} {Colors.GRAY}{title[:36]}{Colors.RESET}")
        if len(subs_data) > 10:
            print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.GRAY}...and {len(subs_data) - 10} more subdomains{Colors.RESET}")
    else:
        print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.GRAY}No public subdomains discovered via CT or standard brute.{Colors.RESET}")
    print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
    print("")

    # 5. SSL/TLS AUDIT BOX
    print(f"{Colors.CYAN}┌─ SSL/TLS SECURITY ───────────────────────────────────────────────────────────┐{Colors.RESET}")
    if ssl_data.get("valid"):
        print_row("Issuer", ssl_data.get("issuer", "N/A"))
        exp_badge = f"{Colors.GREEN}[Active ({ssl_data.get('days_remaining')} days left)]{Colors.RESET}"
        if ssl_data.get("expiring_soon"):
            exp_badge = f"{Colors.YELLOW}[Expiring soon ({ssl_data.get('days_remaining')} days left)]{Colors.RESET}"
        elif ssl_data.get("is_expired"):
            exp_badge = f"{Colors.RED}[EXPIRED ({ssl_data.get('days_remaining')} days ago)]{Colors.RESET}"
            
        print_row("Valid Until", f"{ssl_data.get('valid_until', 'N/A')} - {exp_badge}")
        print_row("TLS Version", f"{Colors.GREEN}{ssl_data.get('tls_version', 'N/A')}{Colors.RESET}")
        print_row("Cipher / Key", f"{ssl_data.get('cipher_name', 'N/A')} ({ssl_data.get('key_bits', 0)} bits)")
    else:
        print_row("Status", f"{Colors.RED}[SSL Handshake Failed / Insecure]{Colors.RESET}")
    print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
    print("")

    # 6. SECURITY HEADERS BOX
    score = sec_headers.get("score", 0)
    grade = sec_headers.get("grade", "F")
    grade_color = Colors.GREEN if score >= 80 else (Colors.YELLOW if score >= 50 else Colors.RED)
    
    print(f"{Colors.CYAN}┌─ SECURITY HEADER SCORE: {grade_color}{score}/100 [GRADE {grade}]{Colors.RESET}{Colors.CYAN} ────────────────────────────────┐{Colors.RESET}")
    headers_map = sec_headers.get("headers", {})
    for h_name, h_info in headers_map.items():
        present = h_info.get("present", False)
        icon = f"{Colors.GREEN}[Present]{Colors.RESET}" if present else f"{Colors.RED}[Missing]{Colors.RESET}"
        print_row(h_name, icon, width=28)
    print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
    print("")

    # 7. SOCIAL LINKS BOX
    has_socials = any(socials.values())
    if has_socials:
        print(f"{Colors.CYAN}┌─ SOCIAL PROFILES & CHANNELS ─────────────────────────────────────────────────┐{Colors.RESET}")
        for platform, link in socials.items():
            if link:
                print_row(platform.capitalize(), f"{Colors.BLUE}{link}{Colors.RESET}")
        print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
        print("")

    # SUMMARY FOOTER
    print(f"{Colors.CYAN}================================================================================{Colors.RESET}")
    print(f"  {Colors.BOLD}{Colors.GREEN}Scan Complete in {scan_duration:.2f} seconds{Colors.RESET}  |  Target: {Colors.CYAN}{domain}{Colors.RESET}")
    print(f"{Colors.CYAN}================================================================================{Colors.RESET}")

def print_row(label: str, value: str, width: int = 20):
    """Print an aligned row inside a box."""
    print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.WHITE}{label:<{width}}{Colors.RESET}: {value}")
