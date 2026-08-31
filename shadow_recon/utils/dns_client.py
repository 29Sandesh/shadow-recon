"""
DNS Client Utility using dnspython with custom resolver fallback and record querying.
"""

import socket
from typing import List, Dict, Any, Optional
import dns.resolver
import dns.rdatatype

PUBLIC_DNS_SERVERS = ["1.1.1.1", "1.0.0.1", "8.8.8.8", "8.8.4.4", "9.9.9.9"]

def get_configured_resolver(timeout: float = 3.0) -> dns.resolver.Resolver:
    """Create a configured dns.resolver with fast timeout and fallback public servers."""
    res = dns.resolver.Resolver()
    res.timeout = timeout
    res.lifetime = timeout
    res.nameservers = PUBLIC_DNS_SERVERS
    return res

def query_dns_records(domain: str, record_type: str) -> List[str]:
    """
    Query DNS records for a given domain and record type (A, AAAA, MX, NS, TXT, CNAME, SOA).
    """
    records = []
    resolver = get_configured_resolver()

    try:
        answers = resolver.resolve(domain, record_type)
        for rdata in answers:
            if record_type == "MX":
                records.append(f"{rdata.preference} {rdata.exchange.to_text().rstrip('.')}")
            elif record_type == "TXT":
                # Join multiple string parts if present
                txt_str = "".join([b.decode('utf-8', errors='ignore') if isinstance(b, bytes) else str(b) for b in rdata.strings])
                records.append(txt_str)
            else:
                records.append(rdata.to_text().rstrip("."))
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.LifetimeTimeout, dns.resolver.NoNameservers, Exception):
        pass

    return records

def resolve_ip_addresses(domain: str) -> List[str]:
    """Get all IPv4 (A) and IPv6 (AAAA) addresses."""
    ips = []
    a_records = query_dns_records(domain, "A")
    aaaa_records = query_dns_records(domain, "AAAA")
    ips.extend(a_records)
    ips.extend(aaaa_records)
    return ips

def reverse_dns_lookup(ip: str) -> Optional[str]:
    """Perform reverse DNS PTR lookup on an IP address."""
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        return hostname
    except Exception:
        return None
