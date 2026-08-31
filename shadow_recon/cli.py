"""
CLI Entrypoint for Shadow-Recon: Argument parsing, interactive wizard, and output dispatching.
"""

import sys
import os
import argparse
from typing import List

from .banner import print_banner
from .engine import run_recon_scan
from .utils.helpers import sanitize_domain, cprint, Colors
from .exporters.terminal import print_terminal_report
from .exporters.json_export import export_json
from .exporters.csv_export import export_csv
from .exporters.html_report import generate_html_report

def main():
    parser = argparse.ArgumentParser(
        description="Shadow-Recon: Instant B2B Company & Domain Intelligence OSINT Scanner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  shadow-recon stripe.com
  shadow-recon github.com --html report.html
  shadow-recon vercel.com --json results.json --csv leads.csv
  shadow-recon --file targets.txt --csv bulk_leads.csv
  shadow-recon openai.com --quick
        """
    )

    parser.add_argument("domain", nargs="?", help="Target domain name (e.g. stripe.com)")
    parser.add_argument("-o", "--json", dest="json_out", help="Export full report as JSON file (e.g. report.json)")
    parser.add_argument("--html", dest="html_out", help="Export interactive HTML report (e.g. report.html)")
    parser.add_argument("--csv", dest="csv_out", help="Export summary row to CSV spreadsheet (e.g. leads.csv)")
    parser.add_argument("-f", "--file", dest="file_in", help="Scan multiple domains from a text file (one domain per line)")
    parser.add_argument("-q", "--quick", action="store_true", help="Quick mode (skips heavy DNS brute force)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose debug output")

    args = parser.parse_args()

    print_banner()

    # Bulk file scan mode
    if args.file_in:
        if not os.path.exists(args.file_in):
            cprint(f"Error: Target file '{args.file_in}' not found!", Colors.RED)
            sys.exit(1)

        with open(args.file_in, "r", encoding="utf-8") as f:
            raw_domains = [line.strip() for line in f if line.strip() and not line.startswith("#")]

        cprint(f"[*] Loaded {len(raw_domains)} domains for bulk intelligence scan.", Colors.YELLOW)
        all_results = []

        for idx, raw in enumerate(raw_domains, 1):
            try:
                target = sanitize_domain(raw)
                cprint(f"\n[{idx}/{len(raw_domains)}] Scanning: {target}", Colors.CYAN, bold=True)
                data = run_recon_scan(target, quick=True, verbose=args.verbose)
                all_results.append(data)
                print_terminal_report(data, data.get("scan_duration_seconds", 0.0))
            except Exception as e:
                cprint(f"Skipping '{raw}': {e}", Colors.RED)

        if args.csv_out:
            export_csv(all_results, args.csv_out)
            cprint(f"\n[✓] Bulk CSV Export Saved: {args.csv_out}", Colors.GREEN, bold=True)

        if args.json_out:
            export_json(all_results, args.json_out)
            cprint(f"[✓] Bulk JSON Export Saved: {args.json_out}", Colors.GREEN, bold=True)

        sys.exit(0)

    # Single domain target
    target_raw = args.domain

    if not target_raw:
        # Interactive prompt if no argument provided
        cprint("Enter target domain to scan (e.g. stripe.com): ", Colors.YELLOW, end="")
        try:
            target_raw = input().strip()
        except KeyboardInterrupt:
            print("\nExiting.")
            sys.exit(0)

    if not target_raw:
        cprint("Error: No target domain provided.", Colors.RED)
        sys.exit(1)

    try:
        clean_target = sanitize_domain(target_raw)
    except ValueError as err:
        cprint(f"Error: {err}", Colors.RED)
        sys.exit(1)

    # Execute Scan
    scan_data = run_recon_scan(clean_target, quick=args.quick, verbose=args.verbose)

    # Print Terminal View
    print_terminal_report(scan_data, scan_data.get("scan_duration_seconds", 0.0))

    # Export Dispatches
    if args.json_out:
        export_json(scan_data, args.json_out)
        cprint(f"[✓] JSON Report Saved: {args.json_out}", Colors.GREEN)

    if args.html_out:
        generate_html_report(scan_data, args.html_out)
        cprint(f"[✓] HTML Dashboard Report Saved: {args.html_out}", Colors.GREEN)

    if args.csv_out:
        export_csv([scan_data], args.csv_out)
        cprint(f"[✓] CSV Lead Row Saved: {args.csv_out}", Colors.GREEN)

if __name__ == "__main__":
    main()
