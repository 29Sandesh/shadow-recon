# 🌐 SHADOW-RECON v1.0
[![GitHub Stars](https://img.shields.io/github/stars/29Sandesh/shadow-recon?style=for-the-badge&color=brightgreen)](https://github.com/29Sandesh/shadow-recon/stargazers)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue?style=for-the-badge)](https://github.com/29Sandesh/shadow-recon)
[![Python Version](https://img.shields.io/badge/Python-3.9+-yellow?style=for-the-badge&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)](LICENSE)

> **Instant B2B Company & Domain Intelligence OSINT Scanner.**
> *A high-speed terminal reconnaissance tool that extracts verified company intelligence, tech stack fingerprints (150+ technologies), email deliverability (MX, SPF, DKIM, DMARC), subdomain maps, SSL/TLS certificates, and security headers in seconds.*

---

## ⚡ 1-Line Quick Install

### Windows (PowerShell):
```powershell
irm https://raw.githubusercontent.com/29Sandesh/shadow-recon/main/install.ps1 | iex
```

### Linux & macOS (Bash):
```bash
curl -sSL https://raw.githubusercontent.com/29Sandesh/shadow-recon/main/install.sh | bash
```

---

## 🎯 Usage & CLI Examples

```bash
# Instant scan on any domain
shadow-recon stripe.com

# Short alias
recon vercel.com

# Export to Interactive Dark-Mode HTML Report
shadow-recon github.com --html report.html

# Export to JSON
shadow-recon openai.com --json report.json

# Export to CSV (Spreadsheet / Lead enrichment)
shadow-recon shopify.com --csv leads.csv

# Bulk scan multiple domains from a text file
shadow-recon --file targets.txt --csv bulk_leads.csv

# Quick scan mode (skips heavy DNS brute)
shadow-recon netflix.com --quick
```

---

## 📺 Terminal Interface

```
================================================================================
   _____ __  _____    ____  ____ _       __     ____  ____________  _   __
  / ___// / / /   |  / __ \/ __ \ |     / /    / __ \/ ____/ ____/ / | / /
  \__ \/ /_/ / /| | / / / / / / / | /| / /____/ /_/ / __/ / /     /  |/ / 
 ___/ / __  / ___ |/ /_/ / /_/ /| |/ |/ /_____/ _, _/ /___/ /___  / /|  /  
/____/_/ /_/_/  |_/_____/\____/ |__/|__/     /_/ |_/_____/\____/ /_/ |_/   
                                                          [ RECON v1.0 ]
================================================================================
  B2B Company Intelligence  |  Tech Stack OSINT  |  Email & Subdomain Recon
================================================================================

┌─ DOMAIN INTELLIGENCE ────────────────────────────────────────────────────────┐
│  IP Address        : 185.166.143.28 (Cloudflare CDN & Edge)
│  Registrar         : MarkMonitor Inc.
│  Domain Age        : 14 years, 3 months
│  Nameservers       : ns1.p36.dynect.net, ns2.p36.dynect.net
│  Hosting           : Cloudflare CDN & Edge
└───────────────────────────────────────────────────────────────────────────────┘

┌─ TECH STACK DETECTED ────────────────────────────────────────────────────────┐
│  Frontend          : Next.js, React
│  Analytics         : Segment, Google Tag Manager
│  Payments          : Stripe
│  Security / Mon    : Sentry
└───────────────────────────────────────────────────────────────────────────────┘

┌─ EMAIL INTELLIGENCE ─────────────────────────────────────────────────────────┐
│  Provider          : Google Workspace (Gmail for Business)
│  SPF Policy        : [Configured] (Softfail (~all) - Standard Protection)
│  DMARC Policy      : [Enforced]
│  DKIM Signing      : [Active (1 found)]
│  Likely Pattern    : first.last@stripe.com
└───────────────────────────────────────────────────────────────────────────────┘

┌─ SUBDOMAINS DISCOVERED (12 found) ───────────────────────────────────────────┐
│  api.stripe.com                 [200]  Stripe API
│  dashboard.stripe.com           [200]  Stripe Dashboard
│  docs.stripe.com                [200]  Stripe Documentation
│  status.stripe.com              [200]  Stripe System Status
│  connect.stripe.com             [200]  Stripe Connect
└───────────────────────────────────────────────────────────────────────────────┘

┌─ SSL/TLS SECURITY ───────────────────────────────────────────────────────────┐
│  Issuer            : DigiCert Inc
│  Valid Until       : 2027-01-15 - [Active (502 days left)]
│  TLS Version       : TLSv1.3
│  Cipher / Key      : TLS_AES_256_GCM_SHA384 (256 bits)
└───────────────────────────────────────────────────────────────────────────────┘

┌─ SECURITY HEADER SCORE: 92/100 [GRADE A+] ────────────────────────────────┐
│  Strict-Transport-Security: [Present]
│  Content-Security-Policy  : [Present]
│  X-Frame-Options          : [Present]
│  X-Content-Type-Options   : [Present]
│  Referrer-Policy          : [Present]
│  Permissions-Policy       : [Missing]
└───────────────────────────────────────────────────────────────────────────────┘

┌─ SOCIAL PROFILES & CHANNELS ─────────────────────────────────────────────────┐
│  Linkedin          : https://www.linkedin.com/company/stripe
│  Twitter           : https://x.com/stripe
│  Github            : https://github.com/stripe
└───────────────────────────────────────────────────────────────────────────────┘

================================================================================
  Scan Complete in 3.42 seconds  |  Target: stripe.com
================================================================================
```

---

## 🔍 The 7 Intelligence Vectors

1. **🌐 Domain Intelligence**: IP resolution, reverse PTR hostnames, RDAP registration, creation/expiration dates, domain age, and CDN detection.
2. **🛠️ Tech Stack Fingerprinting**: 150+ technology signatures spanning React, Next.js, Vue, Tailwind, WordPress, Shopify, Express, Django, Stripe, Segment, Hotjar, Sentry, Cloudflare.
3. **📧 Email Deliverability**: MX server classification (Google Workspace, Microsoft 365, Zoho), SPF policy validation, DMARC policy enforcement, DKIM active selector discovery, and email pattern heuristics (`first.last@company.com`).
4. **📡 Subdomain Discovery**: Certificate Transparency logs (crt.sh & HackerTarget) + DNS brute-forcing + concurrent HTTP status probing.
5. **🔒 SSL / TLS Audit**: Issuer certificate authority, days until expiration, TLS 1.3 / 1.2 protocol verification, and Subject Alternative Names (SANs).
6. **🛡️ Security Header Score**: 0-100 score + letter grade (A+ through F) evaluating HSTS, CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, and Permissions-Policy.
7. **🔗 Social Discovery**: Automatic extraction of official LinkedIn, Twitter/X, GitHub, YouTube, Facebook, and Instagram company profiles.

---

## 📊 Export Formats

* **Terminal UI**: High-contrast, colorized box-drawn tables.
* **HTML Dashboard (`--html`)**: Standalone, responsive dark-mode HTML dashboard.
* **JSON File (`--json`)**: Machine-readable structured JSON for automated pipelines.
* **CSV Spreadsheet (`--csv`)**: Flat spreadsheet output for bulk B2B lead enrichment.

---

## ⚖️ Disclaimer
*Shadow-Recon is designed for cybersecurity auditing, penetration testing, and B2B research on domains you own or have permission to inspect. It queries only publicly available DNS, SSL certificate transparency logs, and HTTP headers.*

---

## 👤 Author
* **Developer**: [Sandesh Agrawal (@29Sandesh)](https://github.com/29Sandesh)
* **Website**: [sandeshagrawal.tech](https://sandeshagrawal.tech) | [codehtml.in](https://codehtml.in)
* **License**: MIT Open-Source License
