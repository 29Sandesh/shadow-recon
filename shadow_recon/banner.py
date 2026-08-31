"""
ASCII Art Banner and Terminal Branding for Shadow-Recon.
"""

from .utils.helpers import Colors

def print_banner():
    """Print the official Shadow-Recon ASCII logo and header."""
    top_line = "=" * 80
    logo = r"""   _____ __  _____    ____  ____ _       __     ____  ____________  _   __
  / ___// / / /   |  / __ \/ __ \ |     / /    / __ \/ ____/ ____/ / | / /
  \__ \/ /_/ / /| | / / / / / / / | /| / /____/ /_/ / __/ / /     /  |/ / 
 ___/ / __  / ___ |/ /_/ / /_/ /| |/ |/ /_____/ _, _/ /___/ /___  / /|  /  
/____/_/ /_/_/  |_/_____/\____/ |__/|__/     /_/ |_/_____/\____/ /_/ |_/   
                                                          [ RECON v1.0 ]"""
    sub_line = "  B2B Company Intelligence  |  Tech Stack OSINT  |  Email & Subdomain Recon"
    
    print(f"{Colors.CYAN}{top_line}\n{logo}\n{top_line}\n{sub_line}\n{top_line}{Colors.RESET}")
