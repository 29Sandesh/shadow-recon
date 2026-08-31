"""
Terminal Pretty-Print Exporter: Outputs high-contrast colorized cyberpunk intelligence dashboard.
"""

from typing import Dict, Any
from ..utils.helpers import Colors

def print_terminal_report(data: Dict[str, Any], scan_duration: float):
    """Render full formatted terminal report."""
    domain = data.get("domain", "Unknown")
    comp = data.get("company_intel", {})
    scale = data.get("scale_estimator", {})
    ai = data.get("ai_summary", {})
    vitals = data.get("web_vitals", {})
    routes = data.get("routes_intel", {})
    geo = data.get("geoip", {})
    dns_data = data.get("domain_intel", {})
    tech_data = data.get("tech_stack", {})
    email_data = data.get("email_intel", {})
    subs_data = data.get("subdomains", [])
    ssl_data = data.get("ssl_tls", {})
    sec_headers = data.get("header_analysis", {})
    socials = data.get("social_recon", {})
    ports = data.get("port_matrix", [])

    print("")
    
    # 1. 🧠 AI EXECUTIVE SUMMARY & PITCH ANGLE
    if ai:
        print(f"{Colors.CYAN}┌─ 🧠 AI EXECUTIVE BRIEF & PROSPECTING ANGLE ──────────────────────────────────┐{Colors.RESET}")
        print_row("Business Model", f"{Colors.WHITE}{ai.get('business_brief', 'N/A')[:52]}...{Colors.RESET}")
        warns = ai.get("security_warnings", [])
        if warns:
            print_row("Core Vulnerability", f"{Colors.YELLOW}{warns[0][:52]}...{Colors.RESET}")
        print_row("Agency Pitch Angle", f"{Colors.GREEN}{ai.get('pitch_angle', 'N/A')[:52]}...{Colors.RESET}")
        print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
        print("")

    # 2. 💼 B2B TECH BUDGET & SCALE ESTIMATOR
    if scale:
        print(f"{Colors.CYAN}┌─ 💼 B2B TECH BUDGET & COMPANY SCALE ESTIMATOR ──────────────────────────────┐{Colors.RESET}")
        print_row("Maturity Tier", f"{Colors.BOLD}{Colors.WHITE}{scale.get('tier', 'N/A')}{Colors.RESET}")
        print_row("Est. Employee Count", f"{Colors.CYAN}{scale.get('estimated_employees', 'N/A')}{Colors.RESET}")
        print_row("Est. SaaS Tech Spend", f"{Colors.GREEN}{scale.get('estimated_saas_budget', 'N/A')}{Colors.RESET}")
        print_row("Stack Complexity", f"{scale.get('infrastructure_complexity', 'N/A')}")
        print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
        print("")

    # 3. ⚡ WEB VITALS & NETWORK PROTOCOLS
    if vitals:
        print(f"{Colors.CYAN}┌─ ⚡ WEB VITALS & PROTOCOL MODERNITY ─────────────────────────────────────────┐{Colors.RESET}")
        print_row("Server TTFB Latency", f"{Colors.GREEN}{vitals.get('ttfb_ms', 0)} ms{Colors.RESET} (Time to first byte)")
        h3_badge = f"{Colors.GREEN}[HTTP/3 QUIC Ready]{Colors.RESET}" if vitals.get("http3_quic_support") else f"{Colors.CYAN}[HTTP/2 Active]{Colors.RESET}"
        print_row("Protocol Standard", h3_badge)
        print_row("Tracker Weight", f"{vitals.get('tracker_bloat_rating', 'Clean')}")
        print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
        print("")

    # 4. 🏢 COMPANY & BUSINESS IDENTITY
    print(f"{Colors.CYAN}┌─ 🏢 COMPANY & BUSINESS PROFILE ──────────────────────────────────────────────┐{Colors.RESET}")
    brand = comp.get("brand_name") or domain.split(".")[0].capitalize()
    print_row("Company / Brand", f"{Colors.BOLD}{Colors.WHITE}{brand}{Colors.RESET}")
    if comp.get("title"):
        print_row("Headline", f"{comp.get('title')[:52]}")
    if comp.get("description"):
        desc = comp.get("description").replace("\n", " ").strip()
        print_row("Summary", f"{Colors.GRAY}{desc[:52]}...{Colors.RESET}")
    print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
    print("")

    # 5. 🌍 GEOLOCATION & NETWORK ASN
    print(f"{Colors.CYAN}┌─ 🌍 SERVER GEOLOCATION & NETWORK INFRASTRUCTURE ─────────────────────────────┐{Colors.RESET}")
    flag = geo.get("flag", "🌐")
    loc_str = f"{flag} {geo.get('city', 'Unknown')}, {geo.get('region', 'Unknown')}, {geo.get('country', 'Unknown')}"
    print_row("Datacenter City", loc_str)
    print_row("Server IP", f"{Colors.WHITE}{dns_data.get('primary_ip', 'N/A')}{Colors.RESET}")
    print_row("ASN Network", f"{Colors.CYAN}{geo.get('asn', 'N/A')}{Colors.RESET}")
    print_row("Hosting / ISP", f"{geo.get('isp', 'N/A')} ({dns_data.get('hosting_provider', 'N/A')})")
    print_row("Domain Age", f"{Colors.GREEN}{dns_data.get('domain_age', 'N/A')}{Colors.RESET} (Reg: {dns_data.get('registrar', 'N/A')})")
    print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
    print("")

    # 6. 📬 PUBLIC CONTACT HARVEST & EMAIL INTEL
    print(f"{Colors.CYAN}┌─ 📬 VERIFIED CONTACTS & EMAIL DELIVERABILITY ────────────────────────────────┐{Colors.RESET}")
    emails = comp.get("public_emails", [])
    if emails:
        print_row("Public Inboxes", f"{Colors.GREEN}{', '.join(emails[:3])}{Colors.RESET}")
    phones = comp.get("phone_numbers", [])
    if phones:
        print_row("Phone Contacts", f"{Colors.CYAN}{', '.join(phones[:2])}{Colors.RESET}")
    
    print_row("Mail Provider", email_data.get("provider", "N/A"))
    
    spf = email_data.get("spf", {})
    spf_badge = f"{Colors.GREEN}[Active]{Colors.RESET}" if spf.get("configured") else f"{Colors.RED}[Missing]{Colors.RESET}"
    dmarc = email_data.get("dmarc", {})
    dmarc_badge = f"{Colors.GREEN}[Enforced]{Colors.RESET}" if dmarc.get("is_enforced") else f"{Colors.YELLOW}[Monitoring]{Colors.RESET}"
    print_row("Security Posture", f"SPF: {spf_badge}  |  DMARC: {dmarc_badge}")
    
    patterns = email_data.get("email_patterns", [])
    top_pat = patterns[0] if patterns else "None"
    print_row("Estimated Pattern", f"{Colors.YELLOW}{top_pat}{Colors.RESET} (Standard heuristic)")
    print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
    print("")

    # 7. 📜 PUBLIC ROUTES, APPS & POLICY DISCOVERY
    if routes:
        print(f"{Colors.CYAN}┌─ 📜 PUBLIC ROUTES, APPS & SECURITY POLICIES ─────────────────────────────────┐{Colors.RESET}")
        sec_txt = f"{Colors.GREEN}[Found - Official Contacts Active]{Colors.RESET}" if routes.get("security_txt", {}).get("present") else f"{Colors.GRAY}[Not Published]{Colors.RESET}"
        print_row("security.txt", sec_txt)
        rob_txt = f"{Colors.GREEN}[Published]{Colors.RESET} ({routes.get('robots_txt', {}).get('disallowed_count', 0)} rules)" if routes.get("robots_txt", {}).get("present") else f"{Colors.GRAY}[Missing]{Colors.RESET}"
        print_row("robots.txt", rob_txt)
        apps = routes.get("mobile_apps", {}).get("details", [])
        apps_str = f"{Colors.GREEN}{', '.join(apps)}{Colors.RESET}" if apps else f"{Colors.GRAY}[No Mobile App Links Found]{Colors.RESET}"
        print_row("Mobile Apps Linked", apps_str)
        print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
        print("")

    # 8. 📡 PORT MATRIX & LIVE SERVICE EXPOSURE
    if ports:
        open_ports = [p for p in ports if p.get("is_open")]
        print(f"{Colors.CYAN}┌─ 📡 SERVICE PORTS & EXPOSURE MATRIX ({len(open_ports)} Active) ──────────────────────────────┐{Colors.RESET}")
        for p in ports:
            status = f"{Colors.GREEN}[OPEN]{Colors.RESET} ({p.get('latency_ms')}ms)" if p.get("is_open") else f"{Colors.GRAY}[CLOSED]{Colors.RESET}"
            p_label = f"Port {p.get('port')} ({p.get('service')})"
            print_row(p_label, status, width=28)
        print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
        print("")

    # 9. 🛠️ TECH STACK DETECTED
    print(f"{Colors.CYAN}┌─ 🛠️  TECH STACK & INTEGRATIONS DETECTED ─────────────────────────────────────┐{Colors.RESET}")
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
        print_row("Status", f"{Colors.YELLOW}Custom built architecture / Minimal signatures matched{Colors.RESET}")
        
    print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
    print("")

    # 10. 📡 SUBDOMAINS DISCOVERED
    print(f"{Colors.CYAN}┌─ 📡 SUBDOMAINS & ASSET RECON ({len(subs_data)} found) ───────────────────────────────────┐{Colors.RESET}")
    if subs_data:
        for s in subs_data[:8]:
            sub_name = s.get("subdomain", "")
            code = s.get("status_code")
            code_str = f"[{code}]" if code else "[---]"
            code_color = Colors.GREEN if code in [200, 301, 302] else (Colors.RED if code in [403, 500] else Colors.GRAY)
            title = s.get("title") or s.get("server") or ""
            takeover = f" {Colors.RED}[TAKEOVER RISK]{Colors.RESET}" if s.get("takeover_vulnerable") else ""
            print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.WHITE}{sub_name:<30}{Colors.RESET} {code_color}{code_str:<6}{Colors.RESET} {Colors.GRAY}{title[:30]}{Colors.RESET}{takeover}")
        if len(subs_data) > 8:
            print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.GRAY}...and {len(subs_data) - 8} more subdomains{Colors.RESET}")
    else:
        print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.GRAY}No public subdomains discovered via CT or standard brute.{Colors.RESET}")
    print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
    print("")

    # 11. 🔒 SSL/TLS & SECURITY HEADERS
    score = sec_headers.get("score", 0)
    grade = sec_headers.get("grade", "F")
    grade_color = Colors.GREEN if score >= 80 else (Colors.YELLOW if score >= 50 else Colors.RED)
    
    print(f"{Colors.CYAN}┌─ 🔒 SSL/TLS & SECURITY POSTURE: {grade_color}{score}/100 [GRADE {grade}]{Colors.RESET}{Colors.CYAN} ──────────────────────────┐{Colors.RESET}")
    if ssl_data.get("valid"):
        print_row("TLS Certificate", f"{ssl_data.get('issuer', 'N/A')} ({Colors.GREEN}{ssl_data.get('days_remaining')} days left{Colors.RESET})")
        print_row("Protocol / Cipher", f"{ssl_data.get('tls_version', 'N/A')} ({ssl_data.get('cipher_name', 'N/A')})")
    
    headers_map = sec_headers.get("headers", {})
    sec_summary = []
    for h_name, h_info in headers_map.items():
        if h_info.get("present"):
            sec_summary.append(h_name.replace("Strict-Transport-Security", "HSTS").replace("Content-Security-Policy", "CSP").replace("X-Frame-Options", "X-Frame").replace("X-Content-Type-Options", "Nosniff"))
    print_row("Active Defenses", f"{Colors.GREEN}{', '.join(sec_summary) if sec_summary else 'None'}{Colors.RESET}")
    print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
    print("")

    # 12. 🔗 SOCIAL & COMMUNITY
    has_socials = any(socials.values())
    if has_socials:
        print(f"{Colors.CYAN}┌─ 🔗 SOCIAL & PUBLIC PRESENCE ────────────────────────────────────────────────┐{Colors.RESET}")
        for platform, link in socials.items():
            if link:
                print_row(platform.capitalize(), f"{Colors.BLUE}{link}{Colors.RESET}")
        print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
        print("")

    # SUMMARY FOOTER
    print(f"{Colors.CYAN}================================================================================{Colors.RESET}")
    print(f"  {Colors.BOLD}{Colors.GREEN}Scan Complete in {scan_duration:.2f}s{Colors.RESET}  |  Target: {Colors.CYAN}{domain}{Colors.RESET}  |  IP: {Colors.WHITE}{dns_data.get('primary_ip', 'N/A')}{Colors.RESET}")
    print(f"{Colors.CYAN}================================================================================{Colors.RESET}")

def print_row(label: str, value: str, width: int = 20):
    """Print an aligned row inside a box."""
    print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.WHITE}{label:<{width}}{Colors.RESET}: {value}")
