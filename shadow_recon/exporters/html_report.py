"""
HTML Report Exporter: Generates a beautiful standalone dark-theme responsive dashboard.
"""

from typing import Dict, Any

def generate_html_report(data: Dict[str, Any], filepath: str) -> str:
    """Generate self-contained dark-mode HTML intelligence report."""
    domain = data.get("domain", "Unknown")
    comp = data.get("company_intel", {})
    geo = data.get("geoip", {})
    dns_data = data.get("domain_intel", {})
    tech_data = data.get("tech_stack", {})
    email_data = data.get("email_intel", {})
    subs_data = data.get("subdomains", [])
    ssl_data = data.get("ssl_tls", {})
    sec_headers = data.get("header_analysis", {})
    socials = data.get("social_recon", {})
    ports = data.get("port_matrix", [])
    score = sec_headers.get("score", 0)
    grade = sec_headers.get("grade", "F")

    # Tech Pills
    tech_pills = ""
    for cat, items in tech_data.items():
        if items:
            for item in items:
                tech_pills += f'<span class="badge badge-tech">{item}</span>'
    if not tech_pills:
        tech_pills = '<span class="text-muted">Custom built / No standard signatures detected</span>'

    # Port Rows
    port_rows = ""
    for p in ports:
        status_badge = f'<span class="badge badge-success">OPEN ({p.get("latency_ms")}ms)</span>' if p.get("is_open") else '<span class="badge badge-muted">CLOSED</span>'
        port_rows += f"""
        <tr>
            <td><code>Port {p.get('port')}</code></td>
            <td>{p.get('service')}</td>
            <td>{status_badge}</td>
        </tr>
        """

    # Subdomains Rows
    sub_rows = ""
    for sub in subs_data:
        code = sub.get("status_code", "---")
        badge_cls = "badge-success" if code in [200, 301, 302] else ("badge-danger" if code in [403, 500] else "badge-muted")
        takeover_alert = '<span class="badge badge-danger">TAKEOVER RISK</span> ' if sub.get("takeover_vulnerable") else ''
        sub_rows += f"""
        <tr>
            <td><code>{sub.get('subdomain')}</code></td>
            <td><span class="badge {badge_cls}">{code}</span></td>
            <td>{takeover_alert}{sub.get('title') or sub.get('server') or '<span class="text-muted">N/A</span>'}</td>
        </tr>
        """
    if not sub_rows:
        sub_rows = '<tr><td colspan="3" class="text-muted">No public subdomains discovered</td></tr>'

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shadow-Recon OSINT Intelligence Report: {domain}</title>
    <style>
        :root {{
            --bg: #0d1117;
            --card-bg: #161b22;
            --border: #30363d;
            --text: #c9d1d9;
            --text-white: #f0f6fc;
            --accent: #58a6ff;
            --success: #238636;
            --danger: #da3633;
            --warning: #d29922;
            --muted: #8b949e;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
        body {{ background-color: var(--bg); color: var(--text); padding: 2rem 1rem; line-height: 1.6; }}
        .container {{ max-width: 1100px; margin: 0 auto; }}
        
        .header {{ background: linear-gradient(135deg, #1f2937, #111827); border: 1px solid var(--border); border-radius: 12px; padding: 2rem; margin-bottom: 2rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }}
        .header h1 {{ color: var(--text-white); font-size: 1.8rem; display: flex; align-items: center; gap: 0.5rem; }}
        .header p {{ color: var(--muted); font-size: 0.95rem; }}
        
        .score-circle {{ width: 85px; height: 85px; border-radius: 50%; background: #21262d; border: 3px solid {"var(--success)" if score >= 80 else ("var(--warning)" if score >= 50 else "var(--danger)")}; display: flex; flex-direction: column; align-items: center; justify-content: center; }}
        .score-num {{ font-size: 1.4rem; font-weight: bold; color: var(--text-white); }}
        .score-lbl {{ font-size: 0.7rem; color: var(--muted); text-transform: uppercase; }}

        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 1.5rem; margin-bottom: 1.5rem; }}
        .card {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 10px; padding: 1.5rem; }}
        .card h2 {{ color: var(--text-white); font-size: 1.15rem; margin-bottom: 1rem; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem; }}
        
        .row {{ display: flex; justify-content: space-between; margin-bottom: 0.75rem; font-size: 0.9rem; }}
        .row-label {{ color: var(--muted); }}
        .row-val {{ color: var(--text-white); font-weight: 500; text-align: right; word-break: break-all; }}

        .badge {{ display: inline-block; padding: 0.2rem 0.6rem; border-radius: 20px; font-size: 0.75rem; font-weight: bold; }}
        .badge-tech {{ background: #1f6feb22; color: #58a6ff; border: 1px solid #1f6feb66; margin: 0.2rem; }}
        .badge-success {{ background: #23863633; color: #3fb950; border: 1px solid #238636; }}
        .badge-danger {{ background: #da363333; color: #f85149; border: 1px solid #da3633; }}
        .badge-muted {{ background: #30363d; color: #8b949e; }}
        .text-muted {{ color: var(--muted); }}

        table {{ width: 100%; border-collapse: collapse; margin-top: 0.5rem; font-size: 0.85rem; }}
        th, td {{ padding: 0.6rem; text-align: left; border-bottom: 1px solid var(--border); }}
        th {{ color: var(--muted); font-weight: 600; text-transform: uppercase; font-size: 0.75rem; }}
        
        .footer {{ text-align: center; color: var(--muted); font-size: 0.85rem; margin-top: 3rem; padding-top: 1rem; border-top: 1px solid var(--border); }}
        .footer a {{ color: var(--accent); text-decoration: none; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <h1>🌐 {domain}</h1>
                <p><strong>{comp.get('brand_name') or domain}</strong> • {comp.get('description', 'Company OSINT Intelligence Report')[:90]}</p>
            </div>
            <div class="score-circle">
                <span class="score-num">{score}</span>
                <span class="score-lbl">Grade {grade}</span>
            </div>
        </div>

        <div class="grid">
            <!-- Company Profile -->
            <div class="card">
                <h2>🏢 Company Profile</h2>
                <div class="row"><span class="row-label">Brand Name</span><span class="row-val">{comp.get('brand_name', 'N/A')}</span></div>
                <div class="row"><span class="row-label">Inboxes</span><span class="row-val">{", ".join(comp.get('public_emails', ['N/A'])[:2])}</span></div>
                <div class="row"><span class="row-label">Phones</span><span class="row-val">{", ".join(comp.get('phone_numbers', ['N/A'])[:1])}</span></div>
                <div class="row"><span class="row-label">Keywords</span><span class="row-val">{", ".join(comp.get('keywords', ['N/A'])[:3])}</span></div>
            </div>

            <!-- Geolocation & Infrastructure -->
            <div class="card">
                <h2>🌍 Geolocation & Network</h2>
                <div class="row"><span class="row-label">Location</span><span class="row-val">{geo.get('flag', '🌐')} {geo.get('city', 'N/A')}, {geo.get('country', 'N/A')}</span></div>
                <div class="row"><span class="row-label">Primary IP</span><span class="row-val">{dns_data.get('primary_ip', 'N/A')}</span></div>
                <div class="row"><span class="row-label">ASN</span><span class="row-val">{geo.get('asn', 'N/A')}</span></div>
                <div class="row"><span class="row-label">Hosting / CDN</span><span class="row-val">{dns_data.get('hosting_provider', 'N/A')}</span></div>
                <div class="row"><span class="row-label">Domain Age</span><span class="row-val">{dns_data.get('domain_age', 'N/A')}</span></div>
            </div>

            <!-- Email Intelligence -->
            <div class="card">
                <h2>📧 Email Deliverability</h2>
                <div class="row"><span class="row-label">Provider</span><span class="row-val">{email_data.get('provider', 'N/A')}</span></div>
                <div class="row"><span class="row-label">SPF Record</span><span class="row-val">{'<span class="badge badge-success">Configured</span>' if email_data.get('spf', {}).get('configured') else '<span class="badge badge-danger">Missing</span>'}</span></div>
                <div class="row"><span class="row-label">DMARC Policy</span><span class="row-val">{email_data.get('dmarc', {}).get('policy', 'None').upper()}</span></div>
                <div class="row"><span class="row-label">Likely Pattern</span><span class="row-val"><code>{email_data.get('email_patterns', ['N/A'])[0]}</code></span></div>
            </div>

            <!-- SSL/TLS Security -->
            <div class="card">
                <h2>🔒 SSL / TLS Configuration</h2>
                <div class="row"><span class="row-label">Issuer</span><span class="row-val">{ssl_data.get('issuer', 'N/A')}</span></div>
                <div class="row"><span class="row-label">Valid Until</span><span class="row-val">{ssl_data.get('valid_until', 'N/A')} ({ssl_data.get('days_remaining', '0')} days)</span></div>
                <div class="row"><span class="row-label">Protocol</span><span class="row-val">{ssl_data.get('tls_version', 'N/A')}</span></div>
                <div class="row"><span class="row-label">Cipher</span><span class="row-val">{ssl_data.get('cipher_name', 'N/A')}</span></div>
            </div>
        </div>

        <!-- Tech Stack -->
        <div class="card" style="margin-bottom: 1.5rem;">
            <h2>🛠️ Detected Tech Stack & Integrations</h2>
            <div style="margin-top: 0.5rem;">
                {tech_pills}
            </div>
        </div>

        <div class="grid">
            <!-- Port Matrix Table -->
            <div class="card">
                <h2>📡 Service Ports & Exposure Matrix</h2>
                <table>
                    <thead>
                        <tr><th>Port</th><th>Service</th><th>Status</th></tr>
                    </thead>
                    <tbody>
                        {port_rows}
                    </tbody>
                </table>
            </div>

            <!-- Subdomains Table -->
            <div class="card">
                <h2>📡 Discovered Subdomains ({len(subs_data)})</h2>
                <table>
                    <thead>
                        <tr><th>Subdomain</th><th>Status</th><th>Title / Server</th></tr>
                    </thead>
                    <tbody>
                        {sub_rows}
                    </tbody>
                </table>
            </div>
        </div>

        <div class="footer">
            Built with precision by <a href="https://github.com/29Sandesh" target="_blank">Sandesh Agrawal (@29Sandesh)</a> • <a href="https://github.com/29Sandesh/shadow-recon" target="_blank">Shadow-Recon GitHub</a>
        </div>
    </div>
</body>
</html>
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
    return filepath
