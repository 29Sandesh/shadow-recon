"""
Executive System Branding and Typography for Shadow-Recon.
"""

from .utils.helpers import Colors

def print_banner():
    """Print clean executive system header."""
    top = "=" * 80
    sub = "  SHADOW-RECON ENTERPRISE INTELLIGENCE SYSTEM  |  OSINT & AUDIT CORE v2.0"
    meta = "  B2B Identity • Infrastructure Recon • Security Auditing • Competitor Diff"
    print(f"{Colors.CYAN}{top}\n{sub}\n{meta}\n{top}{Colors.RESET}")
