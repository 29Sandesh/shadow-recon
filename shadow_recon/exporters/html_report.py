"""
HTML Report Exporter: Generates a beautiful standalone dark-theme responsive dashboard.
"""

from typing import Dict, Any

def generate_html_report(data: Dict[str, Any], filepath: str) -> str:
    """Generate self-contained dark-mode HTML intelligence report."""
    domain = data.get("domain", "Unknown")
    dns_data = data.get("domain_intel", {})
    tech_data = data.get("tech_stack", {})
    email_data = data.get("email_intel", {})
    subs_data = data.get("subdomains", [])
    ssl_data = data.get("ssl_tls", {})
    sec_headers = data.get("header_analysis", {})
    socials = data.get("social_recon", {})
    score = sec_headers.get("score", 0)
    grade = sec_headers.get("grade", "F")

    # Generate Tech Pills
    tech_pills = ""
    for cat, items in tech_data.items():
        if items:
            for item in items:
                tech_pills += f'<span class="badge badge-tech">{item}</span>'
    if not tech_pills:
        tech_pills = '<span class="text-muted">Custom built / No standard signatures detected</span>'

    # Generate Subdomains Rows
    sub_rows = ""
    for sub in subs_data:
        code = sub.get("status_code", "---")
        badge_cls = "badge-success" if code in [200, 301, 302] else ("badge-danger" if code in [403, 500] else "badge-muted")
        sub_rows += f"""
        <tr>
            <td><code>{sub.get('subdomain')}</code></td>
            <td><span class="badge {badge_cls}">{code}</span></td>
            <td>{sub.get('title') or sub.get('server') or '<span class="text-muted">N/A</span>'}</td>
        </tr>
        """
    if not sub_rows:
        sub_rows = '<tr><td colspan="3" class="text-muted">No public subdomains discovered</td></tr>'

    # Generate Security Headers Rows
    header_rows = ""
    for h_name, h_info in sec_headers.get("headers", {}).items():
        present = h_info.get("present", False)
        badge = '<span class="badge badge-success">Present</span>' if present else '<span class="badge badge-danger">Missing</span>'
        header_rows += f"""
        <tr>
            <td><strong>{h_name}</strong><br><small class="text-muted">{h_info.get('description')}</small></td>
            <td>{badge}</td>
        </tr>
        """

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
            --accent-cyan: #39c5bb;
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
                <p>Generated by <strong>Shadow-Recon OSINT Scanner</strong> • Developer Intelligence Report</p>
            </div>
            <div class="score-circle">
                <span class="score-num">{score}</span>
                <span class="score-lbl">Grade {grade}</span>
            </div>
        </div>

        <div class="grid">
            <!-- Domain Intelligence -->
            <div class="card">
                <h2>🌐 Domain Intelligence</h2>
                <div class="row"><span class="row-label">Primary IP</span><span class="row-val">{dns_data.get('primary_ip', 'N/A')}</span></div>
                <div class="row"><span class="row-label">Hosting / CDN</span><span class="row-val">{dns_data.get('hosting_provider', 'N/A')}</span></div>
                <div class="row"><span class="row-label">Registrar</span><span class="row-val">{dns_data.get('registrar', 'N/A')}</span></div>
                <div class="row"><span class="row-label">Domain Age</span><span class="row-val">{dns_data.get('domain_age', 'N/A')}</span></div>
                <div class="row"><span class="row-label">Nameservers</span><span class="row-val">{", ".join(dns_data.get('nameservers', [])[:2])}</span></div>
            </div>

            <!-- Email Intelligence -->
            <div class="card">
                <h2>📧 Email Deliverability</h2>
                <div class="row"><span class="row-label">Provider</span><span class="row-val">{email_data.get('provider', 'N/A')}</span></div>
                <div class="row"><span class="row-label">SPF Record</span><span class="row-val">{'<span class="badge badge-success">Configured</span>' if email_data.get('spf', {}).get('configured') else '<span class="badge badge-danger">Missing</span>'}</span></div>
                <div class="row"><span class="row-label">DMARC Policy</span><span class="row-val">{email_data.get('dmarc', {}).get('policy', 'None').upper()}</span></div>
                <div class="row"><span class="row-label">Likely Pattern</span><span class="row-val"><code>{email_data.get('email_patterns', ['N/A'])[0]}</code></span></div>
                <div class="row"><span class="row-label">Spoofing Defense</span><span class="row-val">{'<span class="badge badge-success">Hardened</span>' if email_data.get('spoofing_protected') else '<span class="badge badge-danger">Vulnerable</span>'}</span></div>
            </div>

            <!-- SSL/TLS Security -->
            <div class="card">
                <h2>🔒 SSL / TLS Configuration</h2>
                <div class="row"><span class="row-label">Issuer</span><span class="row-val">{ssl_data.get('issuer', 'N/A')}</span></div>
                <div class="row"><span class="row-label">Valid Until</span><span class="row-val">{ssl_data.get('valid_until', 'N/A')} ({ssl_data.get('days_remaining', '0')} days)</span></div>
                <div class="row"><span class="row-label">Protocol</span><span class="row-val">{ssl_data.get('tls_version', 'N/A')}</span></div>
                <div class="row"><span class="row-label">Cipher</span><span class="row-val">{ssl_data.get('cipher_name', 'N/A')}</span></div>
            </div>

            <!-- Social Profiles -->
            <div class="card">
                <h2>🔗 Public Social Profiles</h2>
                <div class="row"><span class="row-label">LinkedIn</span><span class="row-val">{'<a href="' + socials.get('linkedin') + '" target="_blank" style="color:var(--accent);">View Company</a>' if socials.get('linkedin') else '<span class="text-muted">Not Found</span>'}</span></div>
                <div class="row"><span class="row-label">Twitter / X</span><span class="row-val">{'<a href="' + socials.get('twitter') + '" target="_blank" style="color:var(--accent);">View Profile</a>' if socials.get('twitter') else '<span class="text-muted">Not Found</span>'}</span></div>
                <div class="row"><span class="row-label">GitHub</span><span class="row-val">{'<a href="' + socials.get('github') + '" target="_blank" style="color:var(--accent);">View Org</a>' if socials.get('github') else '<span class="text-muted">Not Found</span>'}</span></div>
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

            <!-- Security Headers -->
            <div class="card">
                <h2>🛡️ Security Headers Audit</h2>
                <table>
                    <thead>
                        <tr><th>Header</th><th>Status</th></tr>
                    </thead>
                    <tbody>
                        {header_rows}
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
