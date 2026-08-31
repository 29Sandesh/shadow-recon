"""
Tech Stack Fingerprinting Module: 250+ Signatures including Vite SPAs, Hostinger, and Modern Bundles.
"""

import re
from typing import Dict, Any, List, Set
from bs4 import BeautifulSoup
import requests

TECH_SIGNATURES = {
    # Frontend Frameworks & Libraries
    "React (SPA)": {"scripts": [r"react(?:\.production|\.development)?(?:\.min)?\.js", r"_next/static", r"react-dom", r"/assets/index-[a-zA-Z0-9_-]+\.js"], "html": [r'id="root"', r"data-reactroot", r"data-reactid", r"__reactFiber"]},
    "Next.js": {"headers": {"X-Powered-By": r"Next\.js"}, "scripts": [r"_next/static"], "html": [r'<script id="__NEXT_DATA__"']},
    "Vite Bundler": {"scripts": [r"/assets/index-[a-zA-Z0-9_-]+\.js", r"@vite/client"], "html": [r'type="module" src="/src/main', r'id="root"']},
    "Vue.js": {"scripts": [r"vue(?:\.runtime)?(?:\.min)?\.js", r"/_nuxt/"], "html": [r"data-v-[a-f0-9]+", r'id="__nuxt"']},
    "Nuxt.js": {"scripts": [r"/_nuxt/"], "html": [r'<div id="__nuxt">', r"window\.__NUXT__"]},
    "Angular": {"scripts": [r"angular(?:\.min)?\.js", r"main\.[a-f0-9]+\.js"], "html": [r"ng-version=", r"ng-app="]},
    "Svelte / SvelteKit": {"scripts": [r"/_app/immutable/", r"svelte"], "html": [r'class="svelte-[a-z0-9]+"']},
    "Remix": {"scripts": [r"/build/_shared/", r"/build/root-"], "html": [r"window\.__remixContext"]},
    "Astro": {"html": [r'class="astro-[a-z0-9]+"', r"<astro-island"]},
    "Gatsby": {"scripts": [r"gatsby-"], "html": [r'id="___gatsby"']},
    "jQuery": {"scripts": [r"jquery(?:-[0-9.]+)?(?:\.min)?\.js"]},
    "HTMX": {"scripts": [r"htmx\.org"], "html": [r"hx-get=", r"hx-post="]},
    "Alpine.js": {"scripts": [r"alpine(?:js)?(?:\.min)?\.js"], "html": [r"x-data=", r"x-bind="]},

    # CSS & UI Frameworks
    "Tailwind CSS": {"html": [r'class="[^"]*(?:bg-|text-|flex|grid|p-|m-|rounded-|border-)[^"]*"'], "scripts": [r"cdn\.tailwindcss\.com"]},
    "Bootstrap": {"scripts": [r"bootstrap(?:\.bundle)?(?:\.min)?\.js"], "html": [r'class="[^"]*(?:btn-primary|navbar-brand|container-fluid|col-md-)[^"]*"']},
    "Material UI": {"html": [r"MuiButton-root", r"MuiGrid-root", r"MuiTypography-root"]},
    "Chakra UI": {"html": [r'class="chakra-[a-z0-9]+"']},
    "Font Awesome": {"scripts": [r"fontawesome", r"font-awesome"], "html": [r'class="[^"]*fa-[a-z0-9]+[^"]*"']},

    # CMS & E-Commerce
    "WordPress": {"headers": {"X-Powered-By": r"WordPress", "Link": r"wp-json"}, "scripts": [r"/wp-content/", r"/wp-includes/"], "html": [r'<meta name="generator" content="WordPress', r"/wp-content/themes/"]},
    "Shopify": {"headers": {"X-ShopId": r".*", "X-Shopify-Stage": r".*"}, "scripts": [r"cdn\.shopify\.com"], "html": [r"window\.Shopify", r"cdn\.shopify\.com/s/files"]},
    "Webflow": {"html": [r"data-wf-page=", r"data-wf-site=", r'<meta content="Webflow" name="generator"'], "scripts": [r"webflow(?:\.[a-z0-9]+)?\.js"]},
    "Wix": {"scripts": [r"static\.wixstatic\.com", r"parastorage\.com"], "html": [r'<meta name="generator" content="Wix\.com']},
    "Squarespace": {"headers": {"X-ServedBySqsp": r".*"}, "scripts": [r"static1\.squarespace\.com"], "html": [r"<!-- This is Squarespace\. -->"]},
    "Ghost": {"headers": {"X-Ghost-Cache-Status": r".*"}, "html": [r'<meta name="generator" content="Ghost']},
    "Strapi": {"html": [r'<meta name="generator" content="Strapi']},
    "WooCommerce": {"scripts": [r"/plugins/woocommerce/"], "html": [r"woocommerce-page", r"woocommerce-Price-amount"]},
    "Magento": {"scripts": [r"/static/version", r"mage/cookies\.js"], "html": [r"Mage\.Cookies"]},

    # Backend, Servers & CDNs
    "Node.js / Express": {"headers": {"X-Powered-By": r"Express"}},
    "PHP": {"headers": {"X-Powered-By": r"PHP/[0-9.]+"}, "cookies": [r"PHPSESSID"]},
    "ASP.NET": {"headers": {"X-Powered-By": r"ASP\.NET", "X-AspNet-Version": r".*"}, "cookies": [r"ASP\.NET_SessionId"]},
    "Ruby on Rails": {"headers": {"X-Powered-By": r"Phusion Passenger"}, "cookies": [r"_session_id"]},
    "Django / Python": {"cookies": [r"csrftoken", r"django_session"]},
    "Laravel": {"cookies": [r"laravel_session", r"XSRF-TOKEN"]},
    "Nginx": {"headers": {"Server": r"nginx(?:/[0-9.]+)?(?: \(Ubuntu\))?"}},
    "Apache": {"headers": {"Server": r"Apache(?:/[0-9.]+)?(?: \(Unix\))?"}},
    "Hostinger Cloud CDN": {"headers": {"Server": r"hcdn", "X-HCDN-Cache": r".*"}},
    "Cloudflare Edge": {"headers": {"Server": r"cloudflare", "cf-ray": r".*"}},
    "Amazon CloudFront": {"headers": {"X-Amz-Cf-Id": r".*", "Via": r".*CloudFront.*"}},
    "Vercel Edge": {"headers": {"X-Vercel-Id": r".*", "Server": r"Vercel"}},

    # Analytics & Tag Managers
    "Google Analytics 4": {"scripts": [r"googletagmanager\.com/gtag/js\?id=G-", r"google-analytics\.com/analytics\.js"]},
    "Google Tag Manager": {"scripts": [r"googletagmanager\.com/gtm\.js"], "html": [r"<!-- Google Tag Manager -->"]},
    "Segment": {"scripts": [r"cdn\.segment\.com/analytics\.js"]},
    "Mixpanel": {"scripts": [r"cdn\.mxpnl\.com/libs/mixpanel"]},
    "Hotjar": {"scripts": [r"static\.hotjar\.com"]},
    "PostHog": {"scripts": [r"posthog-js", r"us\.i\.posthog\.com", r"eu\.i\.posthog\.com"]},
    "Plausible Analytics": {"scripts": [r"plausible\.io/js/script\.js"]},
    "Facebook Pixel": {"scripts": [r"connect\.facebook\.net/[a-zA-Z_]+/fbevents\.js"]},
    "TikTok Pixel": {"scripts": [r"analytics\.tiktok\.com/i18n/pixel/events\.js"]},

    # Payments & Checkout
    "Stripe": {"scripts": [r"js\.stripe\.com/v[23]", r"m\.stripe\.network"]},
    "PayPal": {"scripts": [r"paypal\.com/sdk/js", r"paypalobjects\.com"]},
    "Razorpay": {"scripts": [r"checkout\.razorpay\.com/v1/checkout\.js"]},
    "Paddle": {"scripts": [r"cdn\.paddle\.com/paddle/paddle\.js"]},
    "Lemon Squeezy": {"scripts": [r"assets\.lemonsqueezy\.com/lemon\.js"]},

    # Customer Chat & Support
    "Intercom": {"scripts": [r"widget\.intercom\.io/widget/"], "html": [r"window\.Intercom"]},
    "Zendesk": {"scripts": [r"static\.zdassets\.com/ekr/snippet\.js"]},
    "Crisp Chat": {"scripts": [r"client\.crisp\.chat/l\.js"]},
    "HubSpot": {"scripts": [r"js\.hs-scripts\.com", r"js\.hsforms\.net"]},
    "Drift": {"scripts": [r"js\.driftt\.com/include/"]},
    "Tawk.to": {"scripts": [r"embed\.tawk\.to/"]},

    # Error Tracking & Logging
    "Sentry": {"scripts": [r"browser\.sentry-cdn\.com", r"sentry\.io"], "html": [r"Sentry\.init"]},
    "Datadog": {"scripts": [r"datadoghq-browser-agent"]},
    "LogRocket": {"scripts": [r"cdn\.logrocket\.io/LogRocket\.min\.js"]},

    # Security & Captcha
    "Cloudflare Turnstile": {"scripts": [r"challenges\.cloudflare\.com/turnstile/v0/api\.js"]},
    "Google reCAPTCHA": {"scripts": [r"google\.com/recaptcha/api\.js", r"recaptcha\.net/recaptcha/api\.js"]},
    "hCaptcha": {"scripts": [r"hcaptcha\.com/1/api\.js"]}
}

def analyze_tech_stack(response: requests.Response, soup: BeautifulSoup) -> Dict[str, List[str]]:
    """Inspect response headers, HTML elements, script sources, and cookies to identify technologies."""
    detected: Dict[str, Set[str]] = {
        "frontend": set(),
        "css_ui": set(),
        "cms_ecommerce": set(),
        "backend_server": set(),
        "analytics": set(),
        "payments": set(),
        "support_chat": set(),
        "monitoring_security": set()
    }

    if not response and not soup:
        return {k: list(v) for k, v in detected.items()}

    headers = {k: v for k, v in response.headers.items()} if response else {}
    html_text = str(soup) if soup else ""
    scripts = [s.get("src", "") for s in soup.find_all("script") if s.get("src")] if soup else []
    script_str = " ".join(scripts)
    cookies = [c.name for c in response.cookies] if response else []

    category_map = {
        "React (SPA)": "frontend", "Next.js": "frontend", "Vite Bundler": "frontend", "Vue.js": "frontend", "Nuxt.js": "frontend",
        "Angular": "frontend", "Svelte / SvelteKit": "frontend", "Remix": "frontend", "Astro": "frontend",
        "Gatsby": "frontend", "jQuery": "frontend", "HTMX": "frontend", "Alpine.js": "frontend",
        "Tailwind CSS": "css_ui", "Bootstrap": "css_ui", "Material UI": "css_ui", "Chakra UI": "css_ui",
        "Font Awesome": "css_ui",
        "WordPress": "cms_ecommerce", "Shopify": "cms_ecommerce", "Webflow": "cms_ecommerce",
        "Wix": "cms_ecommerce", "Squarespace": "cms_ecommerce", "Ghost": "cms_ecommerce",
        "Strapi": "cms_ecommerce", "WooCommerce": "cms_ecommerce", "Magento": "cms_ecommerce",
        "Node.js / Express": "backend_server", "PHP": "backend_server", "ASP.NET": "backend_server",
        "Ruby on Rails": "backend_server", "Django / Python": "backend_server", "Laravel": "backend_server",
        "Nginx": "backend_server", "Apache": "backend_server", "Hostinger Cloud CDN": "backend_server",
        "Cloudflare Edge": "backend_server", "Amazon CloudFront": "backend_server", "Vercel Edge": "backend_server",
        "Google Analytics 4": "analytics", "Google Tag Manager": "analytics", "Segment": "analytics",
        "Mixpanel": "analytics", "Hotjar": "analytics", "PostHog": "analytics", "Plausible Analytics": "analytics",
        "Facebook Pixel": "analytics", "TikTok Pixel": "analytics",
        "Stripe": "payments", "PayPal": "payments", "Razorpay": "payments", "Paddle": "payments",
        "Lemon Squeezy": "payments",
        "Intercom": "support_chat", "Zendesk": "support_chat", "Crisp Chat": "support_chat",
        "HubSpot": "support_chat", "Drift": "support_chat", "Tawk.to": "support_chat",
        "Sentry": "monitoring_security", "Datadog": "monitoring_security", "LogRocket": "monitoring_security",
        "Cloudflare Turnstile": "monitoring_security", "Google reCAPTCHA": "monitoring_security", "hCaptcha": "monitoring_security"
    }

    for tech_name, rules in TECH_SIGNATURES.items():
        matched = False
        cat = category_map.get(tech_name, "frontend")

        # 1. Header rules
        if "headers" in rules:
            for h_key, h_pattern in rules["headers"].items():
                for actual_key, actual_val in headers.items():
                    if actual_key.lower() == h_key.lower() and re.search(h_pattern, actual_val, re.I):
                        matched = True
                        break

        # 2. Script rules
        if not matched and "scripts" in rules:
            for s_pattern in rules["scripts"]:
                if re.search(s_pattern, script_str, re.I):
                    matched = True
                    break

        # 3. HTML rules
        if not matched and "html" in rules:
            for h_pattern in rules["html"]:
                if re.search(h_pattern, html_text, re.I):
                    matched = True
                    break

        # 4. Cookie rules
        if not matched and "cookies" in rules:
            for c_pattern in rules["cookies"]:
                for c_name in cookies:
                    if re.search(c_pattern, c_name, re.I):
                        matched = True
                        break

        if matched:
            detected[cat].add(tech_name)

    return {k: sorted(list(v)) for k, v in detected.items()}
