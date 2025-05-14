#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import json
import webbrowser
from datetime import datetime
import subprocess
import sys
from bs4 import BeautifulSoup
import phonenumbers
from ipwhois import IPWhois
import dns.resolver
import re
from fake_useragent import UserAgent
import traceback

# =============== CONFIGURATION ===============
try:
    import colorama
    colorama.init()
    WINDOWS_MODE = True
except ImportError:
    WINDOWS_MODE = False

class Colors:
    DEMON_RED = "\033[38;2;255;36;0m" if not WINDOWS_MODE else ""
    BLOOD = "\033[38;2;200;0;0m" if not WINDOWS_MODE else ""
    FIRE = "\033[38;2;255;69;0m" if not WINDOWS_MODE else ""
    GREEN = "\033[92m" if not WINDOWS_MODE else ""
    YELLOW = "\033[93m" if not WINDOWS_MODE else ""
    CYAN = "\033[96m" if not WINDOWS_MODE else ""
    RESET = "\033[0m" if not WINDOWS_MODE else ""

# API configurations (now using real services)
API_CONFIG = {
    "breach_api": "https://haveibeenpwned.com/api/v3/breachedaccount/",
    "hibp_key": "YOUR_HIBP_API_KEY",  # Register at https://haveibeenpwned.com/API/Key
    "ip_api": "http://ip-api.com/json/",
    "social_api": "https://api.social-searcher.com/v2/search?q="
}

# =============== BANNER ===============
BANNER = f"""
{Colors.BLOOD}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠛⠋⣿⡟⠛⠛⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠃⠻⢆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⠁⠀⠀⠙⢥⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⡞⢣⢸⣇⣰⡇⡼⢵⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡟⡰⠋⠉⣸⡆⠉⠳⣤⢗⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⡰⠞⢸⡅⠀⠀⣿⡿⠀⠀⢸⡆⢳⠄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣰⠏⠀⠀⠙⠦⣄⣹⣇⣤⠶⠉⠀⠀⢛⣄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣼⣃⣀⣀⣀⣀⣀⠏⠘⠂⢙⡂⠤⣀⣀⣀⣱⣆⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⡼⢥⣼⣅⣤⣄⣤⣸⣿⣶⣾⣿⣇⢠⠤⠥⠤⠿⠜⣦⠀⠀⠀⠀
⠀⠀⠀⠀⠾⠱⠂⢲⠒⠒⠒AMIRI⠄⠊⠛⠤⠒⠒⡒⢶⠆⠘⣣⠀⠀⠀
⠀⠀⠀⠘⠛⠓⠒⠛⠒⢻⣿⣶⡏⣋⡉⠛⢩⣶⢹⣶⠒⠒⠛⠒⠛⠛⠃⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⣿⡇⢠⣤⣿⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠈⢉⣿⣇⢸⣿⠛⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢼⣿⡁⠀⠙⠀⠙⣿⡣⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⡆⠀⠀⠀⠀⠀⠀⣾⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠃⠁⠀⠀⠀⠀⠀⠀⠉⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀

{Colors.FIRE}
   █████╗  ██████╗ █████╗ ██████╗     ████████╗ ██████╗  ██████╗ ██╗     
 ██╔══██╗██╔════╝██╔══██╗██╔══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
 ███████║██║     ███████║██████╔╝       ██║   ██║   ██║██║   ██║██║     
 ██╔══██║██║     ██╔══██║██╔══██╗       ██║   ██║   ██║██║   ██║██║     
 ██║  ██║╚██████╗██║  ██║██║  ██║       ██║   ╚██████╔╝╚██████╔╝███████╗
 ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝       ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝
{Colors.RESET}
{Colors.YELLOW}
  1. 🕵️ DISCORD OSINT (Basic Lookup)
  2. 🔐 CREDENTIALS (Email/Password/Leak Check)
  3. 📱 SOCIAL MEDIA (Instagram/Facebook/TikTok/GitHub/Twitter)
  4. 🛠️ ADVANCED TOOLS (OSINT Framework)
  5. 🌍 GEOLOCATION TOOLS
  6. 📞 VOIP CREATOR (Simulated)
  7. 🛡️ OPSEC TOOLS (IP Checks)
  8. 💀 Exit
{Colors.RESET}
"""

# =============== API FUNCTIONS ===============
def check_breach_data(email):
    """Check breach data using Have I Been Pwned API"""
    try:
        headers = {
            'User-Agent': 'ACAB-Tool-V2',
            'hibp-api-key': API_CONFIG['hibp_key']
        }
        response = requests.get(
            f"{API_CONFIG['breach_api']}{email}",
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            return {"breaches": response.json()}
        elif response.status_code == 404:
            return {"breaches": []}
        return {"error": f"API request failed with status: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def get_ip_info(ip):
    """Get IP information using ip-api.com"""
    try:
        response = requests.get(f"{API_CONFIG['ip_api']}{ip}", timeout=10)
        if response.status_code == 200:
            return response.json()
        return {"error": "IP lookup failed"}
    except Exception as e:
        return {"error": str(e)}

def search_social_media(username):
    """Search for username across social media"""
    try:
        response = requests.get(
            f"{API_CONFIG['social_api']}{username}",
            headers={'User-Agent': UserAgent().random},
            timeout=15
        )
        if response.status_code == 200:
            return response.json()
        return {"error": "Social search failed"}
    except Exception as e:
        return {"error": str(e)}

# =============== REAL OSINT FUNCTIONS ===============
def discord_lookup():
    print(f"\n{Colors.FIRE}>>> DISCORD OSINT LOOKUP <<<{Colors.RESET}")
    discord_id = input(f"{Colors.GREEN}[?] Enter Discord ID: {Colors.RESET}").strip()
    
    if not discord_id.isdigit() or len(discord_id) < 17:
        print(f"{Colors.RED}[-] Invalid Discord ID format. Must be 17-18 digits.{Colors.RESET}")
        return
    
    print(f"\n{Colors.CYAN}[+] Basic Discord lookup for ID: {discord_id}{Colors.RESET}")
    print(f"{Colors.YELLOW}[!] Note: Detailed Discord lookup requires official API access{Colors.RESET}")
    
    # Basic public information only
    print(f"\n{Colors.GREEN}=== BASIC DISCORD INFO ===")
    print(f"{Colors.CYAN}User ID: {discord_id}")
    print(f"Creation Date: {datetime.fromtimestamp(((int(discord_id) >> 22) + 1420070400000) / 1000)}")
    print(f"{Colors.YELLOW}For more info, use official Discord API with proper authorization{Colors.RESET}")

def social_media_lookup():
    print(f"\n{Colors.FIRE}>>> SOCIAL MEDIA OSINT <<<{Colors.RESET}")
    username = input(f"{Colors.GREEN}[?] Enter username to search: {Colors.RESET}").strip()
    
    if not username:
        print(f"{Colors.RED}[-] Please enter a valid username{Colors.RESET}")
        return
    
    print(f"\n{Colors.CYAN}[+] Searching for username: {username}{Colors.RESET}")
    
    result = search_social_media(username)
    
    if "error" in result:
        print(f"{Colors.RED}[-] Error: {result['error']}{Colors.RESET}")
        return
    
    print(f"\n{Colors.GREEN}=== SOCIAL MEDIA RESULTS ===")
    if result.get('posts'):
        for post in result['posts'][:5]:  # Show first 5 results
            print(f"\n{Colors.YELLOW}Network: {post['network']}")
            print(f"Username: {post['username']}")
            print(f"URL: {post['url']}")
            print(f"Date: {post['date']}{Colors.RESET}")
    else:
        print(f"{Colors.RED}[-] No social media results found{Colors.RESET}")

def credential_check():
    print(f"\n{Colors.FIRE}>>> CREDENTIAL CHECK <<<{Colors.RESET}")
    email = input(f"{Colors.GREEN}[?] Enter email to check: {Colors.RESET}").strip().lower()
    
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print(f"{Colors.RED}[-] Invalid email format{Colors.RESET}")
        return
    
    print(f"\n{Colors.CYAN}[+] Checking breaches for: {email}{Colors.RESET}")
    
    result = check_breach_data(email)
    
    if "error" in result:
        print(f"{Colors.RED}[-] Error: {result['error']}{Colors.RESET}")
        return
    
    print(f"\n{Colors.GREEN}=== BREACH RESULTS ===")
    if result.get('breaches'):
        for breach in result['breaches'][:5]:  # Show first 5 breaches
            print(f"\n{Colors.RED}Breach Name: {breach['Name']}")
            print(f"{Colors.YELLOW}Date: {breach['AddedDate']}")
            print(f"Compromised Data: {', '.join(breach['DataClasses'])}{Colors.RESET}")
        print(f"\n{Colors.RED}Total breaches found: {len(result['breaches'])}{Colors.RESET}")
        print(f"{Colors.YELLOW}For full details, visit: https://haveibeenpwned.com/{Colors.RESET}")
    else:
        print(f"{Colors.GREEN}[+] No breaches found for this email{Colors.RESET}")

# =============== TOOL FUNCTIONS ===============
def run_thc_hydra():
    print(f"\n{Colors.FIRE}>>> THC-HYDRA BRUTE FORCE <<<{Colors.RESET}")
    print(f"{Colors.RED}[!] Warning: This tool is for educational purposes only{Colors.RESET}")
    target = input(f"{Colors.GREEN}[?] Enter IP/URL: {Colors.RESET}").strip()
    service = input(f"{Colors.GREEN}[?] Enter service (ssh, ftp, http-form, etc.): {Colors.RESET}").strip().lower()
    
    if not target or not service:
        print(f"{Colors.RED}[-] Target and service are required{Colors.RESET}")
        return
    
    print(f"\n{Colors.CYAN}[+] Starting brute force simulation on {target} ({service}){Colors.RESET}")
    print(f"{Colors.YELLOW}[!] This is a simulation. Real attack would require hydra installation.{Colors.RESET}")
    print(f"{Colors.GREEN}[+] Brute force simulation completed{Colors.RESET}")

def google_dorking():
    print(f"\n{Colors.FIRE}>>> GOOGLE DORKING <<<{Colors.RESET}")
    query = input(f"{Colors.GREEN}[?] Enter dork query: {Colors.RESET}").strip()
    
    if not query:
        print(f"{Colors.RED}[-] Please enter a query{Colors.RESET}")
        return
    
    dorks = [
        f"site:{query}",
        f"intitle:{query}",
        f"inurl:{query}",
        f"filetype:pdf {query}",
        f"ext:log {query}"
    ]
    
    print(f"\n{Colors.GREEN}=== GENERATED DORKS ===")
    for i, dork in enumerate(dorks, 1):
        print(f"{i}. {dork}")
    
    choice = input(f"\n{Colors.GREEN}[?] Select dork to search (1-5) or enter custom: {Colors.RESET}").strip()
    
    if choice.isdigit() and 1 <= int(choice) <= 5:
        selected_dork = dorks[int(choice)-1]
    else:
        selected_dork = choice
    
    url = f"https://www.google.com/search?q={requests.utils.quote(selected_dork)}"
    print(f"\n{Colors.CYAN}[+] Opening Google search: {selected_dork}{Colors.RESET}")
    webbrowser.open(url)

def ip_geolocation():
    print(f"\n{Colors.FIRE}>>> IP GEOLOCATION <<<{Colors.RESET}")
    ip = input(f"{Colors.GREEN}[?] Enter IP address: {Colors.RESET}").strip()
    
    if not re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", ip):
        print(f"{Colors.RED}[-] Invalid IP address format{Colors.RESET}")
        return
    
    print(f"\n{Colors.CYAN}[+] Looking up IP: {ip}{Colors.RESET}")
    
    result = get_ip_info(ip)
    
    if "error" in result:
        print(f"{Colors.RED}[-] Error: {result['error']}{Colors.RESET}")
        return
    
    print(f"\n{Colors.GREEN}=== IP GEOLOCATION RESULTS ===")
    print(f"{Colors.YELLOW}IP: {ip}")
    print(f"Country: {result.get('country', 'N/A')}")
    print(f"Region: {result.get('regionName', 'N/A')}")
    print(f"City: {result.get('city', 'N/A')}")
    print(f"ISP: {result.get('isp', 'N/A')}")
    print(f"Organization: {result.get('org', 'N/A')}{Colors.RESET}")

def opsec_tools():
    print(f"\n{Colors.FIRE}>>> OPSEC TOOLS <<<{Colors.RESET}")
    ip = input(f"{Colors.GREEN}[?] Enter your IP to check: {Colors.RESET}").strip()
    
    if not ip or not re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", ip):
        print(f"{Colors.RED}[-] Invalid IP address format{Colors.RESET}")
        return
    
    print(f"\n{Colors.CYAN}[+] Performing OPSEC check for {ip}{Colors.RESET}")
    
    result = get_ip_info(ip)
    
    if "error" in result:
        print(f"{Colors.RED}[-] Error: {result['error']}{Colors.RESET}")
        return
    
    print(f"\n{Colors.GREEN}=== OPSEC RESULTS ===")
    print(f"{Colors.YELLOW}IP: {ip}")
    print(f"ISP: {result.get('isp', 'N/A')}")
    print(f"Location: {result.get('city', 'N/A')}, {result.get('country', 'N/A')}")
    print(f"VPN/Proxy Detection: {'Possible' if result.get('proxy') else 'None detected'}")
    print(f"\nRecommendations:")
    print(f"- Use a VPN for anonymity")
    print(f"- Disable WebRTC in your browser")
    print(f"- Regularly clear cookies and cache{Colors.RESET}")

# =============== MAIN ===============
def main():
    print(BANNER)
    while True:
        try:
            choice = input(f"{Colors.DEMON_RED}ACAB{Colors.RESET}@{Colors.GREEN}ToolV2{Colors.RESET}> ").strip()
            
            if choice == "1":
                discord_lookup()
            elif choice == "2":
                credential_check()
            elif choice == "3":
                social_media_lookup()
            elif choice == "4":
                print(f"\n{Colors.YELLOW}Advanced tools would be launched here{Colors.RESET}")
            elif choice == "5":
                ip_geolocation()
            elif choice == "6":
                print(f"\n{Colors.YELLOW}VOIP number generation simulated{Colors.RESET}")
            elif choice == "7":
                opsec_tools()
            elif choice == "8":
                print(f"\n{Colors.RED}[-] Exiting...{Colors.RESET}")
                break
            else:
                print(f"{Colors.RED}[-] Invalid choice{Colors.RESET}")
        except KeyboardInterrupt:
            print(f"\n{Colors.RED}[-] Operation cancelled by user{Colors.RESET}")
            continue
        except Exception as e:
            print(f"\n{Colors.RED}[-] ERROR DETAILS:{Colors.RESET}")
            traceback.print_exc()
            print(f"\n{Colors.YELLOW}[!] The tool encountered an error but will continue running{Colors.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[-] Tool terminated by user{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}[-] FATAL ERROR:{Colors.RESET}")
        traceback.print_exc()
        sys.exit(1)
