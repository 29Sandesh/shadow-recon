"""
SSL / TLS Security Audit Module: Certificate Chain, Expiry Warning, TLS 1.3 / 1.2, & SANs.
"""

import ssl
import socket
import datetime
from typing import Dict, Any, List

def scan_ssl_tls(domain: str, port: int = 443, timeout: int = 5) -> Dict[str, Any]:
    """Inspect the target's TLS certificate chain, expiration, and supported protocols."""
    result = {
        "valid": False,
        "issuer": "Unknown",
        "subject": "Unknown",
        "valid_from": None,
        "valid_until": None,
        "days_remaining": None,
        "is_expired": False,
        "expiring_soon": False,
        "sans": [],
        "tls_version": None,
        "cipher_name": None,
        "key_bits": None
    }

    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((domain, port), timeout=timeout) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                version = ssock.version()

                result["valid"] = True
                result["tls_version"] = version
                if cipher:
                    result["cipher_name"] = cipher[0]
                    result["key_bits"] = cipher[2]

                # Issuer
                issuer_dict = dict(x[0] for x in cert.get("issuer", []))
                result["issuer"] = issuer_dict.get("organizationName") or issuer_dict.get("commonName") or "Unknown Issuer"

                # Subject
                subject_dict = dict(x[0] for x in cert.get("subject", []))
                result["subject"] = subject_dict.get("commonName") or "Unknown"

                # SANs
                sans = [item[1] for item in cert.get("subjectAltName", []) if item[0] == "DNS"]
                result["sans"] = sans[:10]

                # Dates
                not_before = cert.get("notBefore")
                not_after = cert.get("notAfter")

                if not_before:
                    dt_before = datetime.datetime.strptime(not_before, "%b %d %H:%M:%S %Y %Z")
                    result["valid_from"] = dt_before.strftime("%Y-%m-%d")

                if not_after:
                    dt_after = datetime.datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
                    result["valid_until"] = dt_after.strftime("%Y-%m-%d")
                    
                    now = datetime.datetime.utcnow()
                    remaining = (dt_after - now).days
                    result["days_remaining"] = remaining
                    result["is_expired"] = remaining < 0
                    result["expiring_soon"] = 0 <= remaining <= 30

    except Exception:
        pass

    return result
