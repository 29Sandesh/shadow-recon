"""
Headless REST API Microservice for Shadow-Recon: Provides real-time JSON endpoints for integrations.
"""

import json
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from .engine import run_recon_scan
from .modules.diff_engine import run_competitor_diff
from .utils.helpers import Colors, cprint

class ReconAPIHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Clean logging
        sys_msg = format % args
        cprint(f" [API {self.address_string()}] {sys_msg}", Colors.GRAY)

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        params = urllib.parse.parse_qs(parsed_url.query)

        # CORS Headers
        headers = {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        }

        if path == "/":
            self.send_response(200)
            for k, v in headers.items(): self.send_header(k, v)
            self.end_headers()
            doc = {
                "system": "Shadow-Recon REST API Microservice",
                "version": "2.0.0",
                "status": "online",
                "endpoints": {
                    "GET /api/scan?domain=example.com": "Execute full intelligence assessment",
                    "GET /api/diff?domain1=a.com&domain2=b.com": "Execute comparative competitor assessment",
                    "GET /api/health": "Service health check"
                }
            }
            self.wfile.write(json.dumps(doc, indent=2).encode("utf-8"))
            return

        elif path == "/api/health":
            self.send_response(200)
            for k, v in headers.items(): self.send_header(k, v)
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy", "service": "shadow-recon-api"}).encode("utf-8"))
            return

        elif path == "/api/scan":
            domain = params.get("domain", [None])[0]
            if not domain:
                self.send_response(400)
                for k, v in headers.items(): self.send_header(k, v)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Missing 'domain' query parameter"}).encode("utf-8"))
                return

            quick = params.get("quick", ["false"])[0].lower() == "true"
            data = run_recon_scan(domain, quick=quick)
            self.send_response(200)
            for k, v in headers.items(): self.send_header(k, v)
            self.end_headers()
            self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))
            return

        elif path == "/api/diff":
            d1 = params.get("domain1", [None])[0]
            d2 = params.get("domain2", [None])[0]
            if not d1 or not d2:
                self.send_response(400)
                for k, v in headers.items(): self.send_header(k, v)
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Provide both 'domain1' and 'domain2' query parameters"}).encode("utf-8"))
                return

            diff_res = run_competitor_diff(d1, d2)
            self.send_response(200)
            for k, v in headers.items(): self.send_header(k, v)
            self.end_headers()
            self.wfile.write(json.dumps(diff_res, indent=2).encode("utf-8"))
            return

        else:
            self.send_response(404)
            for k, v in headers.items(): self.send_header(k, v)
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Endpoint not found"}).encode("utf-8"))

def start_server(port: int = 5000):
    """Start local REST API service."""
    server_address = ("", port)
    httpd = HTTPServer(server_address, ReconAPIHandler)
    cprint(f"\n================================================================================", Colors.CYAN)
    cprint(f"  SHADOW-RECON REST API MICROSERVICE IS RUNNING ON PORT {port}", Colors.GREEN, bold=True)
    cprint(f"================================================================================", Colors.CYAN)
    cprint(f"  Endpoint 1: http://localhost:{port}/api/scan?domain=stripe.com", Colors.WHITE)
    cprint(f"  Endpoint 2: http://localhost:{port}/api/diff?domain1=stripe.com&domain2=adyen.com", Colors.WHITE)
    cprint(f"  Documentation: http://localhost:{port}/", Colors.GRAY)
    cprint(f"  Press Ctrl+C to terminate server.\n", Colors.YELLOW)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        cprint("\nStopping REST API server. Done.", Colors.CYAN)
        httpd.server_close()
