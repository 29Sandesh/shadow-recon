"""
Helper functions: Terminal styling, color printing, domain sanitization, box drawing.
"""

import sys
import os
import re
import time
from typing import Optional, List

# Ensure UTF-8 stdout on Windows
if sys.platform == "win32":
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        pass
    try:
        if sys.stdout and hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if sys.stderr and hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

class Colors:
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"

def colorize(text: str, color: str) -> str:
    """Wrap text in ANSI color codes."""
    return f"{color}{text}{Colors.RESET}"

def cprint(text: str, color: str = Colors.WHITE, bold: bool = False, end: str = "\n"):
    """Print colorized text to console."""
    prefix = Colors.BOLD if bold else ""
    try:
        sys.stdout.write(f"{prefix}{color}{text}{Colors.RESET}{end}")
        sys.stdout.flush()
    except Exception:
        try:
            safe_text = text.encode("ascii", errors="replace").decode("ascii")
            sys.stdout.write(f"{prefix}{color}{safe_text}{Colors.RESET}{end}")
            sys.stdout.flush()
        except Exception:
            pass

def sanitize_domain(target: str) -> str:
    """
    Sanitize user input into a clean canonical domain name.
    Example: 'https://www.example.com/api/v1' -> 'example.com'
    """
    target = target.strip().lower()
    # Strip protocol
    target = re.sub(r"^https?://", "", target)
    # Strip path, query params, hash
    target = target.split("/")[0].split("?")[0].split("#")[0]
    # Strip port if present
    target = target.split(":")[0]
    
    # Basic domain regex validation
    domain_regex = r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$"
    if not re.match(domain_regex, target):
        raise ValueError(f"Invalid domain format: '{target}'. Please provide a valid domain like 'stripe.com'.")
    return target

def print_step(message: str, status: str = "RUNNING"):
    """Print an active execution step marker."""
    if status == "RUNNING":
        cprint(f" [*] {message}...", Colors.YELLOW)
    elif status == "DONE":
        cprint(f" [OK] {message}", Colors.GREEN, bold=True)
    elif status == "FAIL":
        cprint(f" [ERR] {message}", Colors.RED)
    elif status == "INFO":
        cprint(f" [i] {message}", Colors.CYAN)
