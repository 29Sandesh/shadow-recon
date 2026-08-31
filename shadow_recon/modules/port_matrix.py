"""
Port Matrix & Service Exposure Module: Fast non-intrusive TCP socket ping across standard web/admin ports.
"""

import socket
import time
import concurrent.futures
from typing import Dict, Any, List

TARGET_PORTS = [
    {"port": 80, "service": "HTTP (Web)", "critical": False},
    {"port": 443, "service": "HTTPS (SSL/TLS)", "critical": False},
    {"port": 8080, "service": "HTTP-Alt / Proxy", "critical": True},
    {"port": 8443, "service": "HTTPS-Alt / Admin", "critical": True},
    {"port": 3000, "service": "Node / React Dev", "critical": True},
    {"port": 5000, "service": "Flask / API Service", "critical": True},
    {"port": 8000, "service": "Django / Dev Server", "critical": True},
    {"port": 22, "service": "SSH Remote Shell", "critical": True}
]

def probe_single_port(ip: str, port_info: Dict[str, Any], timeout: float = 1.5) -> Dict[str, Any]:
    """Test TCP socket connection and measure latency in milliseconds."""
    port = port_info["port"]
    service = port_info["service"]
    res = {
        "port": port,
        "service": service,
        "is_open": False,
        "latency_ms": None,
        "critical": port_info["critical"]
    }

    try:
        start = time.time()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        code = s.connect_ex((ip, port))
        latency = round((time.time() - start) * 1000, 1)
        s.close()
        if code == 0:
            res["is_open"] = True
            res["latency_ms"] = latency
    except Exception:
        pass

    return res

def scan_port_matrix(ip: str, max_workers: int = 8) -> List[Dict[str, Any]]:
    """Probe all target ports concurrently."""
    if not ip or ip in ["None", "127.0.0.1", "::1"]:
        return []

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(probe_single_port, ip, p) for p in TARGET_PORTS]
        for f in concurrent.futures.as_completed(futures):
            try:
                results.append(f.result())
            except Exception:
                pass

    results.sort(key=lambda x: x["port"])
    return results
