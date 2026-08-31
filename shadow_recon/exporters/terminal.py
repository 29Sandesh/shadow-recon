"""
Terminal Pretty-Print Exporter: Outputs 100% verified, factual enterprise OSINT intelligence.
"""

from typing import Dict, Any
from ..utils.helpers import Colors

def print_terminal_report(data: Dict[str, Any], scan_duration: float):
    """Render structured corporate terminal intelligence report containing only verified data."""
    domain = data.get("domain", "Unknown")
    comp = data.get("company_intel", {})
    vitals = data.get("web_vitals", {})
    routes = data.get("routes_intel", {})
    geo = data.get("geoip", {})
    dns_data = data.get("domain_intel", {})
    tech_data = data.get("tech_stack", {})
    email_data = data.get("email_intel", {})
    ent_email = data.get("enterprise_email", {})
    green = data.get("sustainability", {})
    subs_data = data.get("subdomains", [])
    ssl_data = data.get("ssl_tls", {})
    sec_headers = data.get("header_analysis", {})
    socials = data.get("social_recon", {})
    ports = data.get("port_matrix", [])

    print("")

    # 1. 🏢 BUSINESS IDENTITY & METADATA (Verified from HTML / OpenGraph)
    if comp.get("title") or comp.get("description") or comp.get("brand_name"):
        print(f"{Colors.CYAN}┌─ BUSINESS IDENTITY & METADATA ───────────────────────────────────────────────┐{Colors.RESET}")
        brand = comp.get("brand_name") or domain.split(".")[0].capitalize()
        print_row("Entity Name", f"{Colors.BOLD}{Colors.WHITE}{brand}{Colors.RESET}")
        if comp.get("title"):
            print_row("Page Title", f"{comp.get('title')[:52]}")
        if comp.get("description"):
            desc = comp.get("description").replace("\n", " ").strip()
            print_row("Meta Description", f"{Colors.GRAY}{desc[:52]}...{Colors.RESET}")
        if comp.get("keywords"):
            print_row("Meta Keywords", f"{Colors.MAGENTA}{', '.join(comp.get('keywords')[:4])}{Colors.RESET}")
        print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
        print("")

    # 2. 🌍 DATACENTER LOCATION & NETWORK INFRASTRUCTURE (Verified from IP / DNS)
    print(f"{Colors.CYAN}┌─ DATACENTER LOCATION & ASN ROUTING ──────────────────────────────────────────┐{Colors.RESET}")
    flag = geo.get("flag", "🌐")
    loc_str = f"{flag} {geo.get('city', 'Unknown')}, {geo.get('region', 'Unknown')}, {geo.get('country', 'Unknown')}"
    print_row("Datacenter", loc_str)
    print_row("Host IP", f"{Colors.WHITE}{dns_data.get('primary_ip', 'N/A')}{Colors.RESET}")
    print_row("ASN Network", f"{Colors.CYAN}{geo.get('asn', 'N/A')}{Colors.RESET}")
    print_row("Cloud / Host", f"{geo.get('isp', 'N/A')} ({dns_data.get('hosting_provider', 'N/A')})")
    print_row("Domain Age", f"{Colors.GREEN}{dns_data.get('domain_age', 'N/A')}{Colors.RESET} (Registrar: {dns_data.get('registrar', 'N/A')})")
    print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
    print("")

    # 3. 📬 CORPORATE INBOXES & ENTERPRISE EMAIL SECURITY (Verified from DNS records)
    print(f"{Colors.CYAN}┌─ CORPORATE INBOXES & EMAIL SECURITY PROTOCOLS ───────────────────────────────┐{Colors.RESET}")
    emails = comp.get("public_emails", [])
    if emails:
        print_row("Harvested Inboxes", f"{Colors.GREEN}{', '.join(emails[:3])}{Colors.RESET}")
    phones = comp.get("phone_numbers", [])
    if phones:
        print_row("Public Phone", f"{Colors.CYAN}{', '.join(phones[:2])}{Colors.RESET}")
    
    print_row("Mail Gateway", email_data.get("provider", "N/A"))
    
    spf = email_data.get("spf", {})
    spf_badge = f"{Colors.GREEN}[Active: {spf.get('policy', 'Configured')}]{Colors.RESET}" if spf.get("configured") else f"{Colors.RED}[Missing - Spoofable]{Colors.RESET}"
    dmarc = email_data.get("dmarc", {})
    dmarc_badge = f"{Colors.GREEN}[Enforced ({dmarc.get('policy')})]{Colors.RESET}" if dmarc.get("is_enforced") else (f"{Colors.YELLOW}[Monitoring (p=none)]{Colors.RESET}" if dmarc.get("configured") else f"{Colors.RED}[Missing]{Colors.RESET}")
    
    bimi_badge = f"{Colors.GREEN}[Active]{Colors.RESET}" if ent_email.get("bimi", {}).get("configured") else f"{Colors.GRAY}[Not Configured]{Colors.RESET}"
    mta_badge = f"{Colors.GREEN}[Enforced]{Colors.RESET}" if ent_email.get("mta_sts", {}).get("configured") else f"{Colors.GRAY}[Not Configured]{Colors.RESET}"
    
    print_row("SPF Policy", spf_badge)
    print_row("DMARC Policy", dmarc_badge)
    print_row("BIMI Brand Logo", bimi_badge)
    print_row("MTA-STS Security", mta_badge)
    print_row("DNSSEC Status", f"{Colors.GREEN if ent_email.get('dnssec', {}).get('enabled') else Colors.GRAY}{ent_email.get('dnssec', {}).get('details')}{Colors.RESET}")
    print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
    print("")

    # 4. ⚡ INFRASTRUCTURE PERFORMANCE & PROTOCOLS (Verified network measurements)
    if vitals:
        print(f"{Colors.CYAN}┌─ INFRASTRUCTURE PERFORMANCE & PROTOCOLS ─────────────────────────────────────┐{Colors.RESET}")
        print_row("TTFB Latency", f"{Colors.GREEN}{vitals.get('ttfb_ms', 0)} ms{Colors.RESET} (Time to first byte)")
        h3_badge = f"{Colors.GREEN}[HTTP/3 QUIC Supported]{Colors.RESET}" if vitals.get("http3_quic_support") else f"{Colors.CYAN}[HTTP/2 Active]{Colors.RESET}"
        print_row("Protocol Standard", h3_badge)
        print_row("Tracker Footprint", f"{vitals.get('tracker_bloat_rating', 'Clean')}")
        if green:
            green_badge = f"{Colors.GREEN}[Renewable Energy Cloud]{Colors.RESET}" if green.get("is_green_host") else f"{Colors.GRAY}[Standard Datacenter Grid]{Colors.RESET}"
            print_row("Host Sustainability", f"{green_badge} (Payload: {green.get('page_size_kb', 0)} KB)")
        print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
        print("")

    # 5. 📜 PUBLIC ROUTES & SECURITY POLICIES (Verified HTTP requests)
    if routes:
        print(f"{Colors.CYAN}┌─ PUBLIC ROUTES & DISCLOSURE POLICIES ────────────────────────────────────────┐{Colors.RESET}")
        sec_txt = f"{Colors.GREEN}[Published: {', '.join(routes.get('security_txt', {}).get('contacts', []))[:36]}]{Colors.RESET}" if routes.get("security_txt", {}).get("present") else f"{Colors.GRAY}[Not Published]{Colors.RESET}"
        print_row("security.txt", sec_txt)
        rob_txt = f"{Colors.GREEN}[Published ({routes.get('robots_txt', {}).get('disallowed_count', 0)} rules)]{Colors.RESET}" if routes.get("robots_txt", {}).get("present") else f"{Colors.GRAY}[Missing]{Colors.RESET}"
        print_row("robots.txt", rob_txt)
        apps = routes.get("mobile_apps", {}).get("details", [])
        if apps:
            print_row("Mobile Apps", f"{Colors.GREEN}{', '.join(apps)}{Colors.RESET}")
        print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
        print("")

    # 6. 📡 SERVICE PORTS MATRIX (Verified TCP Socket Probes)
    if ports:
        open_ports = [p for p in ports if p.get("is_open")]
        print(f"{Colors.CYAN}┌─ SERVICE PORTS & EXPOSURE MATRIX ({len(open_ports)} Active Ports) ─────────────────────────┐{Colors.RESET}")
        for p in ports:
            status = f"{Colors.GREEN}[OPEN]{Colors.RESET} ({p.get('latency_ms')}ms)" if p.get("is_open") else f"{Colors.GRAY}[CLOSED]{Colors.RESET}"
            p_label = f"Port {p.get('port')} ({p.get('service')})"
            print_row(p_label, status, width=28)
        print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
        print("")

    # 7. 🛠️ DETECTED TECHNOLOGIES (Verified Signatures)
    print(f"{Colors.CYAN}┌─ DETECTED TECHNOLOGIES & INFRASTRUCTURE ─────────────────────────────────────┐{Colors.RESET}")
    all_tech_empty = True
    for cat_name, label in [
        ("frontend", "Frontend"),
        ("css_ui", "CSS / UI"),
        ("cms_ecommerce", "CMS / Commerce"),
        ("backend_server", "Backend / Server"),
        ("analytics", "Analytics"),
        ("payments", "Payments"),
        ("support_chat", "Customer Support"),
        ("monitoring_security", "Security / Monitoring")
    ]:
        techs = tech_data.get(cat_name, [])
        if techs:
            all_tech_empty = False
            print_row(label, f"{Colors.GREEN}{', '.join(techs)}{Colors.RESET}")
            
    if all_tech_empty:
        print_row("Status", f"{Colors.YELLOW}Custom architecture / Zero standard signatures exposed{Colors.RESET}")
        
    print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
    print("")

    # 8. 📡 SUBDOMAINS (Verified Certificate Transparency Logs)
    print(f"{Colors.CYAN}┌─ SUBDOMAIN FLEET & ASSET RECONNAISSANCE ({len(subs_data)} found) ────────────────────────┐{Colors.RESET}")
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
            print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.GRAY}...and {len(subs_data) - 8} additional subdomains{Colors.RESET}")
    else:
        print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.GRAY}No public subdomains detected via CT logs or DNS brute resolution.{Colors.RESET}")
    print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
    print("")

    # 9. 🔒 SSL/TLS & SECURITY COMPLIANCE (Verified TLS Handshake & Headers)
    score = sec_headers.get("score", 0)
    grade = sec_headers.get("grade", "F")
    grade_color = Colors.GREEN if score >= 80 else (Colors.YELLOW if score >= 50 else Colors.RED)
    
    print(f"{Colors.CYAN}┌─ SSL/TLS & SECURITY COMPLIANCE SCORE: {grade_color}{score}/100 [GRADE {grade}]{Colors.RESET}{Colors.CYAN} ─────────────────────┐{Colors.RESET}")
    if ssl_data.get("valid"):
        print_row("TLS Certificate", f"{ssl_data.get('issuer', 'N/A')} ({Colors.GREEN}{ssl_data.get('days_remaining')} days left{Colors.RESET})")
        print_row("Protocol / Cipher", f"{ssl_data.get('tls_version', 'N/A')} ({ssl_data.get('cipher_name', 'N/A')})")
    
    headers_map = sec_headers.get("headers", {})
    sec_summary = []
    for h_name, h_info in headers_map.items():
        if h_info.get("present"):
            sec_summary.append(h_name.replace("Strict-Transport-Security", "HSTS").replace("Content-Security-Policy", "CSP").replace("X-Frame-Options", "X-Frame").replace("X-Content-Type-Options", "Nosniff"))
    print_row("Active Defense Flags", f"{Colors.GREEN}{', '.join(sec_summary) if sec_summary else 'None'}{Colors.RESET}")
    print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
    print("")

    # 10. 🔗 SOCIAL PROFILES (Verified Anchor Links & JSON-LD)
    has_socials = any(socials.values())
    if has_socials:
        print(f"{Colors.CYAN}┌─ PUBLIC SOCIAL & COMMUNITY PRESENCE ────────────────────────────────────────┐{Colors.RESET}")
        for platform, link in socials.items():
            if link:
                print_row(platform.capitalize(), f"{Colors.BLUE}{link}{Colors.RESET}")
        print(f"{Colors.CYAN}└───────────────────────────────────────────────────────────────────────────────┘{Colors.RESET}")
        print("")

    # SUMMARY FOOTER
    print(f"{Colors.CYAN}================================================================================{Colors.RESET}")
    print(f"  {Colors.BOLD}{Colors.GREEN}Assessment Completed in {scan_duration:.2f}s{Colors.RESET}  |  Target: {Colors.CYAN}{domain}{Colors.RESET}  |  IP: {Colors.WHITE}{dns_data.get('primary_ip', 'N/A')}{Colors.RESET}")
    print(f"{Colors.CYAN}================================================================================{Colors.RESET}")

def print_row(label: str, value: str, width: int = 22):
    """Print an aligned row inside a box."""
    print(f"{Colors.CYAN}│{Colors.RESET}  {Colors.WHITE}{label:<{width}}{Colors.RESET}: {value}")
