"""
CLI Entrypoint for Shadow-Recon: Executive Interactive TUI, Comparative Diff, and Microservice Server.
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

def run_single_scan(target_raw: str, args):
    """Execute a single domain scan and export results."""
    try:
        clean_target = sanitize_domain(target_raw)
    except ValueError as err:
        cprint(f"Error: {err}", Colors.RED)
        return

    scan_data = run_recon_scan(clean_target, quick=getattr(args, "quick", False), verbose=getattr(args, "verbose", False))
    print_terminal_report(scan_data, scan_data.get("scan_duration_seconds", 0.0))

    if getattr(args, "json_out", None):
        export_json(scan_data, args.json_out)
        cprint(f"[✓] JSON Report Saved: {args.json_out}", Colors.GREEN)

    if getattr(args, "html_out", None):
        generate_html_report(scan_data, args.html_out)
        cprint(f"[✓] HTML Dashboard Report Saved: {args.html_out}", Colors.GREEN)

    if getattr(args, "pdf_out", None):
        export_pdf_report(scan_data, args.pdf_out)
        cprint(f"[✓] Client Audit Report Saved: {args.pdf_out}", Colors.GREEN)

    if getattr(args, "csv_out", None):
        export_csv([scan_data], args.csv_out)
        cprint(f"[✓] CSV Row Appended: {args.csv_out}", Colors.GREEN)

def show_interactive_menu():
    """Display clean professional executive interactive menu."""
    while True:
        print_banner()
        print(f"  {Colors.BOLD}{Colors.WHITE}EXECUTIVE CONTROL PANEL:{Colors.RESET}")
        print(f"   [1] Domain Intelligence Assessment    (Single Target Deep Recon)")
        print(f"   [2] Comparative Competitor Analysis   (Side-by-Side Domain Diff)")
        print(f"   [3] Batch Domain Assessment           (Scan File -> Export CSV)")
        print(f"   [4] Launch REST API Microservice      (Start Local HTTP Server)")
        print(f"   [0] Exit System")
        print(f"{Colors.CYAN}--------------------------------------------------------------------------------{Colors.RESET}")
        
        cprint("Select Option [0-4]: ", Colors.YELLOW, end="")
        try:
            choice = input().strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break

        if choice == "1":
            cprint("\nEnter target domain (e.g. stripe.com): ", Colors.CYAN, end="")
            target = input().strip()
            if target:
                args = argparse.Namespace(quick=False, verbose=False, json_out=None, html_out=None, pdf_out=None, csv_out=None)
                run_single_scan(target, args)
            input("\nPress Enter to return to menu...")

        elif choice == "2":
            cprint("\nEnter First Domain (e.g. stripe.com): ", Colors.CYAN, end="")
            d1 = input().strip()
            cprint("Enter Second Domain (e.g. adyen.com): ", Colors.CYAN, end="")
            d2 = input().strip()
            if d1 and d2:
                try:
                    c1 = sanitize_domain(d1)
                    c2 = sanitize_domain(d2)
                    diff_res = run_competitor_diff(c1, c2)
                    print_diff_report(diff_res)
                except Exception as e:
                    cprint(f"Error: {e}", Colors.RED)
            input("\nPress Enter to return to menu...")

        elif choice == "3":
            cprint("\nEnter file path with domains (one per line): ", Colors.CYAN, end="")
            fpath = input().strip()
            if fpath and os.path.exists(fpath):
                cprint("Enter CSV output path (e.g. results.csv): ", Colors.CYAN, end="")
                csv_path = input().strip() or "results.csv"
                with open(fpath, "r", encoding="utf-8") as f:
                    raw_domains = [line.strip() for line in f if line.strip() and not line.startswith("#")]
                
                cprint(f"[*] Processing {len(raw_domains)} domains...", Colors.YELLOW)
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
                
                export_csv(all_res, csv_path)
                cprint(f"\n[✓] Batch CSV Saved: {csv_path}", Colors.GREEN, bold=True)
            else:
                cprint("Error: File does not exist.", Colors.RED)
            input("\nPress Enter to return to menu...")

        elif choice == "4":
            cprint("\nEnter server port [Default 5000]: ", Colors.CYAN, end="")
            port_in = input().strip()
            port = int(port_in) if port_in.isdigit() else 5000
            start_server(port)
            break

        elif choice in ["0", "q", "exit"]:
            cprint("Terminating Shadow-Recon session.", Colors.CYAN)
            break

def main():
    parser = argparse.ArgumentParser(
        description="Shadow-Recon Enterprise Intelligence System",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="subcommand")

    # diff subcommand: shadow-recon diff stripe.com adyen.com
    diff_parser = subparsers.add_parser("diff", help="Compare two domains side-by-side")
    diff_parser.add_argument("domain1", help="Primary domain")
    diff_parser.add_argument("domain2", help="Competitor domain")

    # serve subcommand: shadow-recon serve --port 5000
    serve_parser = subparsers.add_parser("serve", help="Launch local REST API server")
    serve_parser.add_argument("--port", type=int, default=5000, help="Port to listen on")

    # Default scan options
    parser.add_argument("domain", nargs="?", help="Target domain name (e.g. stripe.com)")
    parser.add_argument("-o", "--json", dest="json_out", help="Export as JSON file")
    parser.add_argument("--html", dest="html_out", help="Export as HTML dashboard")
    parser.add_argument("--pdf", dest="pdf_out", help="Export as client audit report")
    parser.add_argument("--csv", dest="csv_out", help="Export row to CSV")
    parser.add_argument("-f", "--file", dest="file_in", help="Scan domains from text file")
    parser.add_argument("-q", "--quick", action="store_true", help="Quick scan mode")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose debug output")

    args = parser.parse_args()

    # Subcommand: diff
    if args.subcommand == "diff":
        print_banner()
        c1 = sanitize_domain(args.domain1)
        c2 = sanitize_domain(args.domain2)
        diff_res = run_competitor_diff(c1, c2)
        print_diff_report(diff_res)
        return

    # Subcommand: serve
    if args.subcommand == "serve":
        print_banner()
        start_server(args.port)
        return

    # Direct domain passed on CLI
    if args.domain:
        print_banner()
        run_single_scan(args.domain, args)
        return

    # Direct file passed on CLI
    if args.file_in:
        print_banner()
        with open(args.file_in, "r", encoding="utf-8") as f:
            raw_domains = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        all_results = []
        for idx, raw in enumerate(raw_domains, 1):
            try:
                target = sanitize_domain(raw)
                cprint(f"\n[{idx}/{len(raw_domains)}] Scanning: {target}", Colors.CYAN, bold=True)
                data = run_recon_scan(target, quick=True)
                all_results.append(data)
                print_terminal_report(data, data.get("scan_duration_seconds", 0.0))
            except Exception as e:
                cprint(f"Skipping {raw}: {e}", Colors.RED)
        if args.csv_out:
            export_csv(all_results, args.csv_out)
            cprint(f"\n[✓] Batch CSV Saved: {args.csv_out}", Colors.GREEN, bold=True)
        return

    # No arguments passed -> Launch Professional Interactive TUI Menu
    show_interactive_menu()

if __name__ == "__main__":
    main()
