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
    "social_api": "https://api.social-searcher.com/v2/search?q=",
    "discord_lookup": "https://discordlookup.mesavire.pl/api/v1/user/"
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
  1. 🕵️ DISCORD OSINT (Advanced Lookup)
  2. 🔐 CREDENTIALS (Email/Password/Leak Check)
  3. 📱 SOCIAL MEDIA (Instagram/Facebook/TikTok/GitHub/Twitter)
  4. 🛠️ ADVANCED TOOLS (OSINT Framework)
  5. 🌍 GEOLOCATION TOOLS
  6. 📞 VOIP CREATOR (Simulated)
  7. 🛡️ OPSEC TOOLS (IP Checks)
  8. 💀 Exit
{Colors.RESET}
"""

# =============== DISCORD OSINT ADVANCED ===============
def discord_lookup():
    print(f"\n{Colors.FIRE}>>> DISCORD OSINT ADVANCED <<<{Colors.RESET}")
    discord_id = input(f"{Colors.GREEN}[?] Enter Discord ID: {Colors.RESET}").strip()
    
    if not discord_id.isdigit() or len(discord_id) < 17:
        print(f"{Colors.RED}[-] Invalid Discord ID format. Must be 17-18 digits.{Colors.RESET}")
        return
    
    # Calcolo data creazione precisa
    timestamp = ((int(discord_id) >> 22) + 1420070400000
    creation_date = datetime.fromtimestamp(timestamp/1000).strftime("%Y-%m-%d %H:%M:%S UTC")
    
    # Stima informazioni aggiuntive
    user_flags = int(discord_id) & 0xFFF
    is_bot = bool(user_flags & (1 << 0))
    is_system = bool(user_flags & (1 << 1))
    
    print(f"\n{Colors.GREEN}=== DISCORD OSINT RESULTS ===")
    print(f"{Colors.CYAN}User ID: {discord_id}")
    print(f"Creation Date: {creation_date}")
    print(f"Possible Bot: {'Yes' if is_bot else 'No'}")
    print(f"System Account: {'Yes' if is_system else 'No'}")
    
    # Ricerca username storico
    print(f"\n{Colors.YELLOW}[*] Checking username history...{Colors.RESET}")
    try:
        response = requests.get(
            f"{API_CONFIG['discord_lookup']}{discord_id}",
            headers={'User-Agent': 'Mozilla/5.0'},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print(f"{Colors.GREEN}Username History:")
            for username in data.get('usernames', [])[:3]:
                print(f"- {username}")
            if data.get('avatar_url'):
                print(f"Avatar URL: {data['avatar_url']}")
    except:
        print(f"{Colors.RED}[-] Could not fetch additional info{Colors.RESET}")
    
    # Ricerca nelle cache pubbliche
    print(f"\n{Colors.YELLOW}[*] Searching public caches...{Colors.RESET}")
    try:
        web_cache = requests.get(
            f"https://webcache.googleusercontent.com/search?q=cache:discord.com/users/{discord_id}",
            timeout=10
        )
        if "Discord" in web_cache.text:
            soup = BeautifulSoup(web_cache.text, 'html.parser')
            title = soup.find('title')
            if title:
                print(f"{Colors.CYAN}Possible Username: {title.text.split('|')[0].strip()}")
    except:
        pass
    
    # Ricerca su siti terzi
    print(f"\n{Colors.YELLOW}[*] Checking third-party sites...{Colors.RESET}")
    sites = [
        f"https://discord.id/?prefill={discord_id}",
        f"https://discordhub.com/user/{discord_id}",
        f"https://disboard.org/search/user/{discord_id}"
    ]
    for site in sites:
        try:
            r = requests.head(site, timeout=5, allow_redirects=True)
            if r.status_code == 200:
                print(f"{Colors.GREEN}Found on: {site}")
        except:
            continue
    
    print(f"\n{Colors.YELLOW}[!] Manual checks:")
    print(f"- Check https://discord.com/users/{discord_id}")
    print(f"- Search ID on Google: https://google.com/search?q={discord_id}")

# [Resto del codice rimane invariato...]
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

# [Resto delle funzioni rimane invariato...]

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
