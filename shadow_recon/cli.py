"""
CLI Entrypoint for Shadow-Recon: Clean Argument Parser and Smart 1-Step Interactive Prompt.
"""

import sys
import os
import argparse
from typing import List

from .banner import print_banner
from .engine import run_recon_scan
from .server import start_server
from .modules.diff_engine import run_competitor_diff, print_diff_report
from .utils.helpers import sanitize_domain, cprint, Colors
from .exporters.terminal import print_terminal_report
from .exporters.json_export import export_json
from .exporters.csv_export import export_csv
from .exporters.html_report import generate_html_report
from .exporters.pdf_report import export_pdf_report

def run_single_scan(target_raw: str, args=None):
    """Execute a single domain scan and export results."""
    try:
        clean_target = sanitize_domain(target_raw)
    except ValueError as err:
        cprint(f"Error: {err}", Colors.RED)
        return

    quick = getattr(args, "quick", False) if args else False
    verbose = getattr(args, "verbose", False) if args else False

    scan_data = run_recon_scan(clean_target, quick=quick, verbose=verbose)
    print_terminal_report(scan_data, scan_data.get("scan_duration_seconds", 0.0))

    if args and getattr(args, "json_out", None):
        export_json(scan_data, args.json_out)
        cprint(f"[✓] JSON Report Saved: {args.json_out}", Colors.GREEN)

    if args and getattr(args, "html_out", None):
        generate_html_report(scan_data, args.html_out)
        cprint(f"[✓] HTML Dashboard Report Saved: {args.html_out}", Colors.GREEN)

    if args and getattr(args, "pdf_out", None):
        export_pdf_report(scan_data, args.pdf_out)
        cprint(f"[✓] Client Audit Report Saved: {args.pdf_out}", Colors.GREEN)

    if args and getattr(args, "csv_out", None):
        export_csv([scan_data], args.csv_out)
        cprint(f"[✓] CSV Row Appended: {args.csv_out}", Colors.GREEN)

def handle_user_input(user_input: str, args=None):
    """Smart input dispatcher that auto-detects single domain, competitor diff, file, or serve command."""
    cmd = user_input.strip()
    if not cmd:
        return

    # 1. Exit commands
    if cmd.lower() in ["exit", "quit", "q", "0"]:
        cprint("Exiting Shadow-Recon. Goodbye!", Colors.CYAN)
        sys.exit(0)

    # 2. Serve command
    if cmd.lower() in ["serve", "api", "server"]:
        start_server(5000)
        return

    # 3. Competitor Diff commands
    if " vs " in cmd.lower() or cmd.lower().startswith("diff ") or len(cmd.split()) == 2:
        clean_str = cmd.replace("diff", "").replace("VS", "vs")
        parts = clean_str.split("vs") if "vs" in clean_str else clean_str.split()
        if len(parts) == 2:
            try:
                d1 = sanitize_domain(parts[0].strip())
                d2 = sanitize_domain(parts[1].strip())
                diff_res = run_competitor_diff(d1, d2)
                print_diff_report(diff_res)
                return
            except Exception as e:
                cprint(f"Diff Error: {e}", Colors.RED)
                return

    # 4. File input (e.g. 'domains.txt')
    if cmd.endswith(".txt") and os.path.exists(cmd):
        with open(cmd, "r", encoding="utf-8") as f:
            raw_domains = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        cprint(f"[*] Processing {len(raw_domains)} domains from {cmd}...", Colors.YELLOW)
        all_res = []
        for idx, raw in enumerate(raw_domains, 1):
            try:
                clean_d = sanitize_domain(raw)
                cprint(f"\n[{idx}/{len(raw_domains)}] Scanning: {clean_d}", Colors.CYAN, bold=True)
                data = run_recon_scan(clean_d, quick=True)
                all_res.append(data)
                print_terminal_report(data, data.get("scan_duration_seconds", 0.0))
            except Exception as e:
                cprint(f"Skipping {raw}: {e}", Colors.RED)
        export_csv(all_res, "bulk_leads.csv")
        cprint(f"\n[✓] Bulk CSV Saved: bulk_leads.csv", Colors.GREEN, bold=True)
        return

    # 5. Standard single domain scan
    run_single_scan(cmd, args)

def main():
    # Fast path for 'diff' command
    if len(sys.argv) >= 2 and sys.argv[1] == "diff":
        print_banner()
        if len(sys.argv) >= 4:
            d1 = sanitize_domain(sys.argv[2])
            d2 = sanitize_domain(sys.argv[3])
            diff_res = run_competitor_diff(d1, d2)
            print_diff_report(diff_res)
        else:
            cprint("Usage: shadow-recon diff domain1.com domain2.com", Colors.RED)
        return

    # Fast path for 'serve' command
    if len(sys.argv) >= 2 and sys.argv[1] == "serve":
        print_banner()
        port = 5000
        if "--port" in sys.argv:
            try:
                p_idx = sys.argv.index("--port")
                port = int(sys.argv[p_idx + 1])
            except Exception:
                pass
        start_server(port)
        return

    parser = argparse.ArgumentParser(
        description="Shadow-Recon: Instant B2B Company & Domain Intelligence Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("domain", nargs="?", help="Target domain name (e.g. stripe.com)")
    parser.add_argument("-o", "--json", dest="json_out", help="Export as JSON file")
    parser.add_argument("--html", dest="html_out", help="Export as HTML dashboard")
    parser.add_argument("--pdf", dest="pdf_out", help="Export as client audit report")
    parser.add_argument("--csv", dest="csv_out", help="Export row to CSV")
    parser.add_argument("-f", "--file", dest="file_in", help="Scan domains from text file")
    parser.add_argument("-q", "--quick", action="store_true", help="Quick scan mode")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose debug output")

    args = parser.parse_args()

    # Direct domain passed via terminal (e.g. shadow-recon stripe.com)
    if args.domain:
        print_banner()
        run_single_scan(args.domain, args)
        return

    # Direct file passed via terminal
    if args.file_in:
        print_banner()
        handle_user_input(args.file_in, args)
        return

    # Super-clean, 1-step interactive loop for non-technical users
    print_banner()
    while True:
        cprint("\nEnter domain name to scan (e.g. stripe.com) or 'exit' to quit: ", Colors.YELLOW, end="")
        try:
            user_input = input().strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break

        if not user_input:
            continue

        handle_user_input(user_input, args)

if __name__ == "__main__":
    main()
