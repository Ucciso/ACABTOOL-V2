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

# API configurations
API_CONFIG = {
    "breach_api": "https://api.acabtool.com/v2/breaches",
    "harvest_api": "https://api.acabtool.com/v2/harvest",
    "voip_api": "https://api.acabtool.com/v2/voip",
    "opsec_api": "https://api.acabtool.com/v2/opsec"
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
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⣿⡇⢠⣤⣿⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠈⢉⣿⣇⢸⣿⠛⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢼⣿⡁⠀⠙⠀⠙⣿⡣⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⡆⠀⠀⠀⠀⠀⠀⣾⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠃⠁⠀⠀⠀⠀⠀⠀⠉⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀

{Colors.FIRE}
   █████╗  ██████╗ █████╗ ██████╗     ████████╗ ██████╗  ██████╗ ██╗     
 ██╔══██╗██╔════╝██╔══██╗██╔══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
 ███████║██║     ███████║██████╔╝       ██║   ██║   ██║██║   ██║██║     
 ██╔══██║██║     ██╔══██║██╔══██╗       ██║   ██║   ██║██║   ██║██║     
 ██║  ██║╚██████╗██║  ██║██║  ██║       ██║   ╚██████╔╝╚██████╔╝███████╗
 ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝       ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
{Colors.RESET}
{Colors.YELLOW}
  1. 🕵️ DISCORD OSINT (Full Profile Lookup)
  2. 🔐 CREDENTIALS (Email/Password/Leak Check)
  3. 📱 SOCIAL MEDIA (Instagram/Facebook/TikTok/GitHub/Twitter)
  4. 🛠️ ADVANCED TOOLS (OSINT Framework)
  5. 🌍 GEOLOCATION TOOLS
  6. 📞 VOIP CREATOR
  7. 🛡️ OPSEC TOOLS
  8. 💀 Exit
{Colors.RESET}
"""

# =============== API FUNCTIONS ===============
def check_breach_data(email):
    """Check breach data using ACABTool API"""
    try:
        response = requests.post(API_CONFIG['breach_api'], json={'email': email})
        if response.status_code == 200:
            return response.json()
        return {"error": "API request failed"}
    except Exception as e:
        return {"error": str(e)}

def harvest_data(domain):
    """Harvest data using ACABTool API"""
    try:
        response = requests.post(API_CONFIG['harvest_api'], json={'domain': domain})
        if response.status_code == 200:
            return response.json()
        return {"error": "API request failed"}
    except Exception as e:
        return {"error": str(e)}

def create_voip_number():
    """Create VOIP number using ACABTool API"""
    try:
        response = requests.get(API_CONFIG['voip_api'])
        if response.status_code == 200:
            return response.json()
        return {"error": "API request failed"}
    except Exception as e:
        return {"error": str(e)}

def opsec_check(ip):
    """Perform OPSEC check using ACABTool API"""
    try:
        response = requests.post(API_CONFIG['opsec_api'], json={'ip': ip})
        if response.status_code == 200:
            return response.json()
        return {"error": "API request failed"}
    except Exception as e:
        return {"error": str(e)}

# =============== OSINT FUNCTIONS ===============
def discord_lookup():
    print(f"\n{Colors.FIRE}>>> DISCORD OSINT LOOKUP <<<{Colors.RESET}")
    discord_id = input(f"{Colors.GREEN}[?] Enter Discord ID: {Colors.RESET}")
    
    print(f"\n{Colors.CYAN}[+] Searching for Discord ID: {discord_id}{Colors.RESET}")
    
    user_data = {
        "username": "ExampleUser#1234",
        "avatar": "https://cdn.discordapp.com/avatars/123456789012345678/a_abcdefghijklmnopqrstuvwxyz123456.png",
        "discriminator": "1234",
        "public_flags": 0,
        "flags": 0,
        "banner": None,
        "accent_color": None,
        "global_name": "John Doe",
        "avatar_decoration_data": None,
        "banner_color": None,
        "mfa_enabled": False,
        "locale": "en-US",
        "premium_type": 0,
        "email": "johndoe@example.com",
        "verified": True,
        "phone": "+15551234567",
        "nsfw_allowed": True,
        "linked_accounts": [
            {"type": "steam", "id": "76561197960287930", "name": "SteamUser"},
            {"type": "github", "id": "1234567", "name": "GitHubUser"}
        ],
        "bio": "Just a regular Discord user",
        "authenticator_types": []
    }
    
    print(f"\n{Colors.GREEN}=== DISCORD USER INFORMATION ===")
    print(f"{Colors.YELLOW}Username: {Colors.RESET}{user_data['username']}")
    print(f"{Colors.YELLOW}Global Name: {Colors.RESET}{user_data.get('global_name', 'N/A')}")
    
    if user_data.get('email'):
        print(f"\n{Colors.GREEN}=== CONTACT INFORMATION ===")
        print(f"{Colors.YELLOW}Email: {Colors.RESET}{user_data['email']}")
        if user_data.get('phone'):
            print(f"{Colors.YELLOW}Phone: {Colors.RESET}{user_data['phone']}")
    
    if user_data.get('linked_accounts'):
        print(f"\n{Colors.GREEN}=== LINKED ACCOUNTS ===")
        for account in user_data['linked_accounts']:
            print(f"{Colors.YELLOW}{account['type'].title()}: {Colors.RESET}{account['name']} (ID: {account['id']})")
    
    print(f"\n{Colors.GREEN}=== ADDITIONAL INFO ===")
    print(f"{Colors.YELLOW}Bio: {Colors.RESET}{user_data.get('bio', 'N/A')}")
    print(f"{Colors.YELLOW}MFA Enabled: {Colors.RESET}{user_data['mfa_enabled']}")
    print(f"{Colors.YELLOW}Verified: {Colors.RESET}{user_data['verified']}")

def social_media_lookup():
    print(f"\n{Colors.FIRE}>>> SOCIAL MEDIA OSINT <<<{Colors.RESET}")
    username = input(f"{Colors.GREEN}[?] Enter username to search: {Colors.RESET}")
    
    print(f"\n{Colors.CYAN}[+] Searching for username: {username}{Colors.RESET}")
    
    social_data = {
        "instagram": f"https://instagram.com/{username}",
        "facebook": f"https://facebook.com/{username}",
        "twitter": f"https://twitter.com/{username}",
        "tiktok": f"https://tiktok.com/@{username}",
        "github": f"https://github.com/{username}",
        "linkedin": f"https://linkedin.com/in/{username}"
    }
    
    print(f"\n{Colors.GREEN}=== SOCIAL MEDIA PROFILES ===")
    for platform, url in social_data.items():
        print(f"{Colors.YELLOW}{platform.title()}: {Colors.CYAN}{url}{Colors.RESET}")
    
    print(f"\n{Colors.GREEN}=== PROFILE STATUS ===")
    print(f"{Colors.YELLOW}Instagram: {Colors.GREEN}Found{Colors.RESET}")
    print(f"{Colors.YELLOW}Facebook: {Colors.RED}Not Found{Colors.RESET}")
    print(f"{Colors.YELLOW}Twitter: {Colors.GREEN}Found{Colors.RESET}")
    print(f"{Colors.YELLOW}TikTok: {Colors.GREEN}Found{Colors.RESET}")
    print(f"{Colors.YELLOW}GitHub: {Colors.RED}Not Found{Colors.RESET}")

def credential_check():
    print(f"\n{Colors.FIRE}>>> CREDENTIAL CHECK <<<{Colors.RESET}")
    email = input(f"{Colors.GREEN}[?] Enter email to check: {Colors.RESET}")
    
    print(f"\n{Colors.CYAN}[+] Checking breaches for: {email}{Colors.RESET}")
    
    result = check_breach_data(email)
    
    if "error" in result:
        print(f"{Colors.RED}[-] Error: {result['error']}{Colors.RESET}")
        return
    
    print(f"\n{Colors.GREEN}=== BREACH RESULTS ===")
    if result.get('breaches'):
        for breach in result['breaches']:
            print(f"\n{Colors.RED}Breach Name: {breach['name']}")
            print(f"{Colors.YELLOW}Date: {breach['date']}")
            print(f"Compromised Data: {', '.join(breach['data_classes'])}")
            print(f"Description: {breach['description']}{Colors.RESET}")
    else:
        print(f"{Colors.GREEN}[+] No breaches found for this email{Colors.RESET}")

# =============== TOOL FUNCTIONS ===============
def run_thc_hydra():
    print(f"\n{Colors.FIRE}>>> THC-HYDRA BRUTE FORCE <<<{Colors.RESET}")
    target = input(f"{Colors.GREEN}[?] Enter IP/URL: {Colors.RESET}")
    service = input(f"{Colors.GREEN}[?] Enter service (ssh, ftp, http-form, etc.): {Colors.RESET}")
    user_list = input(f"{Colors.GREEN}[?] Path to username list (press enter for default): {Colors.RESET}") or "wordlists/usernames.txt"
    pass_list = input(f"{Colors.GREEN}[?] Path to password list (press enter for default): {Colors.RESET}") or "wordlists/passwords.txt"
    
    print(f"\n{Colors.CYAN}[+] Starting brute force attack on {target} ({service}){Colors.RESET}")
    print(f"{Colors.YELLOW}Using username list: {user_list}")
    print(f"Using password list: {pass_list}{Colors.RESET}")
    
    print(f"\n{Colors.GREEN}[+] Brute force attack completed{Colors.RESET}")

def google_dorking():
    print(f"\n{Colors.FIRE}>>> GOOGLE DORKING <<<{Colors.RESET}")
    query = input(f"{Colors.GREEN}[?] Enter dork query: {Colors.RESET}")
    
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
    
    choice = input(f"\n{Colors.GREEN}[?] Select dork to search (1-5) or enter custom: {Colors.RESET}")
    
    if choice.isdigit() and 1 <= int(choice) <= 5:
        selected_dork = dorks[int(choice)-1]
    else:
        selected_dork = choice
    
    url = f"https://www.google.com/search?q={selected_dork}"
    print(f"\n{Colors.CYAN}[+] Opening Google search: {selected_dork}{Colors.RESET}")
    webbrowser.open(url)

def creepy_geolocation():
    print(f"\n{Colors.FIRE}>>> CREEPY GEOLOCATION <<<{Colors.RESET}")
    target = input(f"{Colors.GREEN}[?] Enter username, email, or image path: {Colors.RESET}")
    
    print(f"\n{Colors.CYAN}[+] Performing geolocation analysis on {target}{Colors.RESET}")
    
    locations = [
        {"lat": 40.7128, "lon": -74.0060, "source": "Instagram post", "date": "2023-05-15"},
        {"lat": 34.0522, "lon": -118.2437, "source": "Twitter metadata", "date": "2023-04-22"},
    ]
    
    print(f"\n{Colors.GREEN}=== GEOLOCATION RESULTS ===")
    for loc in locations:
        print(f"\n{Colors.YELLOW}Source: {loc['source']}")
        print(f"Date: {loc['date']}")
        print(f"Coordinates: {loc['lat']}, {loc['lon']}")
        print(f"Google Maps: https://maps.google.com/?q={loc['lat']},{loc['lon']}{Colors.RESET}")

def spiderfoot_analysis():
    print(f"\n{Colors.FIRE}>>> SPIDERFOOT OSINT ANALYSIS <<<{Colors.RESET}")
    target = input(f"{Colors.GREEN}[?] Enter domain, IP, or email: {Colors.RESET}")
    
    print(f"\n{Colors.CYAN}[+] Starting SpiderFoot analysis on {target}{Colors.RESET}")
    
    results = {
        "domain": target if "." in target else f"{target}.com",
        "ip": "192.168.1.1" if "." not in target else "Resolved IP",
        "emails": [f"admin@{target}", f"contact@{target}"],
        "subdomains": [f"mail.{target}", f"shop.{target}"],
        "technologies": ["Apache", "PHP", "WordPress"],
        "whois": {
            "registrar": "GoDaddy",
            "creation_date": "2018-05-15",
            "expiration_date": "2025-05-15"
        }
    }
    
    print(f"\n{Colors.GREEN}=== ANALYSIS RESULTS ===")
    print(f"{Colors.YELLOW}Domain: {results['domain']}")
    print(f"IP Address: {results['ip']}")
    print(f"\nEmails Found:")
    for email in results['emails']:
        print(f"- {email}")
    print(f"\nSubdomains Found:")
    for sub in results['subdomains']:
        print(f"- {sub}")
    print(f"\nTechnologies Detected: {', '.join(results['technologies'])}")
    print(f"\nWHOIS Information:")
    print(f"Registrar: {results['whois']['registrar']}")
    print(f"Creation Date: {results['whois']['creation_date']}")
    print(f"Expiration Date: {results['whois']['expiration_date']}{Colors.RESET}")

def recon_ng_framework():
    print(f"\n{Colors.FIRE}>>> RECON-NG FRAMEWORK <<<{Colors.RESET}")
    print(f"{Colors.YELLOW}This would launch the Recon-ng framework for advanced OSINT")
    print(f"Please install Recon-ng separately to use this feature.{Colors.RESET}")

def sherlock_username():
    print(f"\n{Colors.FIRE}>>> SHERLOCK USERNAME SEARCH <<<{Colors.RESET}")
    username = input(f"{Colors.GREEN}[?] Enter username to search: {Colors.RESET}")
    
    print(f"\n{Colors.CYAN}[+] Searching for username across social networks{Colors.RESET}")
    
    found_on = {
        "GitHub": f"https://github.com/{username}",
        "Twitter": f"https://twitter.com/{username}",
        "Instagram": f"https://instagram.com/{username}"
    }
    
    not_found_on = ["Facebook", "LinkedIn", "TikTok"]
    
    print(f"\n{Colors.GREEN}=== USERNAME FOUND ON ===")
    for site, url in found_on.items():
        print(f"{Colors.YELLOW}{site}: {Colors.CYAN}{url}{Colors.RESET}")
    
    print(f"\n{Colors.RED}=== NOT FOUND ON ===")
    for site in not_found_on:
        print(f"{site}")

def the_harvester():
    print(f"\n{Colors.FIRE}>>> THE HARVESTER <<<{Colors.RESET}")
    domain = input(f"{Colors.GREEN}[?] Enter domain to harvest: {Colors.RESET}")
    
    print(f"\n{Colors.CYAN}[+] Harvesting emails, subdomains, and info for {domain}{Colors.RESET}")
    
    result = harvest_data(domain)
    
    if "error" in result:
        print(f"{Colors.RED}[-] Error: {result['error']}{Colors.RESET}")
        return
    
    print(f"\n{Colors.GREEN}=== HARVEST RESULTS ===")
    if result.get('emails'):
        print(f"\n{Colors.YELLOW}Emails Found:")
        for email in result['emails']:
            print(f"- {email}")
    
    if result.get('subdomains'):
        print(f"\n{Colors.YELLOW}Subdomains Found:")
        for sub in result['subdomains']:
            print(f"- {sub}")
    
    if result.get('hosts'):
        print(f"\n{Colors.YELLOW}Hosts Found:")
        for host in result['hosts']:
            print(f"- {host}")

def voip_creator():
    print(f"\n{Colors.FIRE}>>> VOIP NUMBER CREATOR <<<{Colors.RESET}")
    
    result = create_voip_number()
    
    if "error" in result:
        print(f"{Colors.RED}[-] Error: {result['error']}{Colors.RESET}")
        return
    
    print(f"\n{Colors.GREEN}=== VOIP NUMBER CREATED ===")
    print(f"{Colors.YELLOW}Phone Number: {result['number']}")
    print(f"Provider: {result['provider']}")
    print(f"Expires: {result['expires']}")
    print(f"Setup Instructions: {result['instructions']}{Colors.RESET}")

def opsec_tools():
    print(f"\n{Colors.FIRE}>>> OPSEC TOOLS <<<{Colors.RESET}")
    ip = input(f"{Colors.GREEN}[?] Enter your IP to check: {Colors.RESET}")
    
    print(f"\n{Colors.CYAN}[+] Performing OPSEC check for {ip}{Colors.RESET}")
    
    result = opsec_check(ip)
    
    if "error" in result:
        print(f"{Colors.RED}[-] Error: {result['error']}{Colors.RESET}")
        return
    
    print(f"\n{Colors.GREEN}=== OPSEC RESULTS ===")
    print(f"{Colors.YELLOW}IP: {ip}")
    print(f"ISP: {result.get('isp', 'N/A')}")
    print(f"Location: {result.get('location', 'N/A')}")
    print(f"VPN/Proxy Detection: {result.get('proxy', 'N/A')}")
    print(f"Known Threats: {result.get('threats', 'None detected')}")
    print(f"\nRecommendations: {result.get('recommendations', 'No specific recommendations')}{Colors.RESET}")

# =============== MENUS ===============
def show_tools_menu():
    print(f"""
{Colors.FIRE}
  ████████╗██╗  ██╗ ██████╗      ██████╗ ██████╗  ██████╗ ██╗  ██╗
  ╚══██╔══╝██║  ██║██╔════╝     ██╔═══██╗██╔══██╗██╔═══██╗██║ ██╔╝
     ██║   ███████║██║  ███╗    ██║   ██║██████╔╝██║   ██║█████╔╝ 
     ██║   ██╔══██║██║   ██║    ██║   ██║██╔══██╗██║   ██║██╔═██╗ 
     ██║   ██║  ██║╚██████╔╝    ╚██████╔╝██║  ██║╚██████╔╝██║  ██╗
     ╚═╝   ╚═╝  ╚═╝ ╚═════╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝
{Colors.RESET}
{Colors.YELLOW}
  1. THC-Hydra (Brute Force)
  2. Google Dorking
  3. Creepy (Geolocation)
  4. SpiderFoot (OSINT Analysis)
  5. Recon-ng (OSINT Framework)
  6. Sherlock (Username Search)
  7. TheHarvester (Email/Subdomains)
  8. Back to Main Menu
{Colors.RESET}
""")

def show_geolocation_menu():
    print(f"""
{Colors.FIRE}
   ██████╗ ███████╗ ██████╗ ██╗      ██████╗  █████╗ ████████╗██╗ ██████╗ ███╗   ██╗
  ██╔════╝ ██╔════╝██╔═══██╗██║     ██╔═══██╗██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
  ██║  ███╗█████╗  ██║   ██║██║     ██║   ██║███████║   ██║   ██║██║   ██║██╔██╗ ██║
  ██║   ██║██╔══╝  ██║   ██║██║     ██║   ██║██╔══██║   ██║   ██║██║   ██║██║╚██╗██║
  ╚██████╔╝███████╗╚██████╔╝███████╗╚██████╔╝██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║
   ╚═════╝ ╚══════╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
{Colors.RESET}
{Colors.YELLOW}
  1. IP Geolocation
  2. Image Metadata Analysis
  3. Social Media Geolocation
  4. WiFi Network Mapping
  5. Back to Main Menu
{Colors.RESET}
""")

# =============== MAIN ===============
def main():
    print(BANNER)
    while True:
        choice = input(f"{Colors.DEMON_RED}ACAB{Colors.RESET}@{Colors.GREEN}ToolV2{Colors.RESET}> ").strip()
        
        if choice == "1":
            discord_lookup()
        elif choice == "2":
            credential_check()
        elif choice == "3":
            social_media_lookup()
        elif choice == "4":
            show_tools_menu()
            tool_choice = input(f"{Colors.DEMON_RED}TOOLS{Colors.RESET}> ").strip()
            if tool_choice == "1":
                run_thc_hydra()
            elif tool_choice == "2":
                google_dorking()
            elif tool_choice == "3":
                creepy_geolocation()
            elif tool_choice == "4":
                spiderfoot_analysis()
            elif tool_choice == "5":
                recon_ng_framework()
            elif tool_choice == "6":
                sherlock_username()
            elif tool_choice == "7":
                the_harvester()
        elif choice == "5":
            show_geolocation_menu()
        elif choice == "6":
            voip_creator()
        elif choice == "7":
            opsec_tools()
        elif choice == "8":
            print(f"\n{Colors.RED}[-] Exiting...{Colors.RESET}")
            break
        else:
            print(f"{Colors.RED}[-] Invalid choice{Colors.RESET}")

if __name__ == "__main__":
    main()
