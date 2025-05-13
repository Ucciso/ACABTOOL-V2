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
    "opsec_api": "https://api.acabtool.com/v2/opsec",
    "discord_api": "https://api.acabtool.com/v2/discord"
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
  1. 🕵️ ACAB DISCORD OSINT (Full Profile Lookup)
  2. 🔐 CREDENTIALS (Email/Password/Leak Check)
  3. 📱 SOCIAL MEDIA (Instagram/Facebook/TikTok/GitHub/Twitter)
  4. 🛠️ ADVANCED TOOLS (OSINT Framework)
  5. 🌍 GEOLOCATION TOOLS
  6. 📞 VOIP CREATOR (Functional)
  7. 🛡️ OPSEC TOOLS (Real Checks)
  8. 💀 Exit
{Colors.RESET}
"""

# =============== API FUNCTIONS ===============
def check_breach_data(email):
    """Check breach data using ACABTool API"""
    try:
        headers = {'User-Agent': UserAgent().random}
        response = requests.post(API_CONFIG['breach_api'], json={'email': email}, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        return {"error": "API request failed with status code: " + str(response.status_code)}
    except Exception as e:
        return {"error": str(e)}

def harvest_data(domain):
    """Harvest data using ACABTool API"""
    try:
        headers = {'User-Agent': UserAgent().random}
        response = requests.post(API_CONFIG['harvest_api'], json={'domain': domain}, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        return {"error": "API request failed"}
    except Exception as e:
        return {"error": str(e)}

def create_voip_number():
    """Create VOIP number using ACABTool API"""
    try:
        headers = {'User-Agent': UserAgent().random}
        response = requests.get(API_CONFIG['voip_api'], headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        return {"error": "API request failed"}
    except Exception as e:
        return {"error": str(e)}

def opsec_check(ip):
    """Perform OPSEC check using ACABTool API"""
    try:
        headers = {'User-Agent': UserAgent().random}
        response = requests.post(API_CONFIG['opsec_api'], json={'ip': ip}, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        return {"error": "API request failed"}
    except Exception as e:
        return {"error": str(e)}

def get_discord_info(user_id):
    """Get real Discord information using ACAB API"""
    try:
        headers = {'User-Agent': UserAgent().random}
        response = requests.post(API_CONFIG['discord_api'], json={'user_id': user_id}, headers=headers, timeout=15)
        if response.status_code == 200:
            return response.json()
        return {"error": "Failed to fetch Discord info"}
    except Exception as e:
        return {"error": str(e)}

# =============== REAL OSINT FUNCTIONS ===============
def discord_lookup():
    print(f"\n{Colors.FIRE}>>> ACAB DISCORD OSINT LOOKUP <<<{Colors.RESET}")
    discord_id = input(f"{Colors.GREEN}[?] Enter Discord ID: {Colors.RESET}").strip()
    
    if not discord_id.isdigit() or len(discord_id) < 17:
        print(f"{Colors.RED}[-] Invalid Discord ID format. Must be 17-18 digits.{Colors.RESET}")
        return
    
    print(f"\n{Colors.CYAN}[+] Searching for Discord ID: {discord_id}{Colors.RESET}")
    
    result = get_discord_info(discord_id)
    
    if "error" in result:
        print(f"{Colors.RED}[-] Error: {result['error']}{Colors.RESET}")
        return
    
    print(f"\n{Colors.GREEN}=== ACAB DISCORD OSINT RESULTS ===")
    if result.get('found'):
        print(f"\n{Colors.YELLOW}Basic Information:")
        print(f"{Colors.CYAN}Username: {result.get('username', 'N/A')}")
        print(f"Global Name: {result.get('global_name', 'N/A')}")
        print(f"Discriminator: {result.get('discriminator', 'N/A')}")
        print(f"Account Created: {result.get('creation_date', 'N/A')}")
        
        print(f"\n{Colors.YELLOW}Personal Information:")
        print(f"{Colors.CYAN}Full Name: {result.get('full_name', 'N/A')}")
        print(f"Birth Date: {result.get('birth_date', 'N/A')}")
        print(f"Phone Number: {result.get('phone', 'N/A')}")
        print(f"Address: {result.get('address', 'N/A')}")
        print(f"Mother's Name: {result.get('mother_name', 'N/A')}")
        print(f"Father's Name: {result.get('father_name', 'N/A')}")
        
        print(f"\n{Colors.YELLOW}Digital Footprint:")
        print(f"{Colors.CYAN}Email: {result.get('email', 'N/A')}")
        print(f"IP Address: {result.get('ip', 'N/A')}")
        print(f"Devices: {', '.join(result.get('devices', ['N/A']))}")
        
        print(f"\n{Colors.YELLOW}Social Connections:")
        for platform, data in result.get('social_media', {}).items():
            print(f"{platform.title()}: {data.get('username', 'N/A')} ({data.get('url', 'N/A')})")
    else:
        print(f"{Colors.RED}[-] No information found for this Discord ID{Colors.RESET}")

def social_media_lookup():
    print(f"\n{Colors.FIRE}>>> SOCIAL MEDIA OSINT <<<{Colors.RESET}")
    username = input(f"{Colors.GREEN}[?] Enter username to search: {Colors.RESET}").strip()
    
    if not username:
        print(f"{Colors.RED}[-] Please enter a valid username{Colors.RESET}")
        return
    
    print(f"\n{Colors.CYAN}[+] Searching for username: {username}{Colors.RESET}")
    
    # Real API calls would go here - this is a placeholder structure
    platforms = {
        'Instagram': f'https://www.instagram.com/{username}',
        'Facebook': f'https://www.facebook.com/{username}',
        'Twitter': f'https://twitter.com/{username}',
        'TikTok': f'https://www.tiktok.com/@{username}',
        'GitHub': f'https://github.com/{username}',
        'LinkedIn': f'https://www.linkedin.com/in/{username}'
    }
    
    print(f"\n{Colors.GREEN}=== SOCIAL MEDIA RESULTS ===")
    for platform, url in platforms.items():
        try:
            headers = {'User-Agent': UserAgent().random}
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=False)
            
            if response.status_code == 200:
                print(f"{Colors.GREEN}[+] {platform}: {Colors.CYAN}{url} {Colors.GREEN}(Found){Colors.RESET}")
            elif response.status_code == 404:
                print(f"{Colors.RED}[-] {platform}: {Colors.CYAN}{url} {Colors.RED}(Not Found){Colors.RESET}")
            else:
                print(f"{Colors.YELLOW}[?] {platform}: {Colors.CYAN}{url} {Colors.YELLOW}(Status: {response.status_code}){Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[-] {platform}: Error checking - {str(e)}{Colors.RESET}")

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
        for breach in result['breaches']:
            print(f"\n{Colors.RED}Breach Name: {breach['name']}")
            print(f"{Colors.YELLOW}Date: {breach['date']}")
            print(f"Compromised Data: {', '.join(breach['data_classes'])}")
            print(f"Description: {breach['description']}{Colors.RESET}")
        print(f"\n{Colors.RED}Total breaches found: {len(result['breaches'])}{Colors.RESET}")
    else:
        print(f"{Colors.GREEN}[+] No breaches found for this email{Colors.RESET}")

# =============== TOOL FUNCTIONS ===============
def run_thc_hydra():
    print(f"\n{Colors.FIRE}>>> THC-HYDRA BRUTE FORCE <<<{Colors.RESET}")
    target = input(f"{Colors.GREEN}[?] Enter IP/URL: {Colors.RESET}").strip()
    service = input(f"{Colors.GREEN}[?] Enter service (ssh, ftp, http-form, etc.): {Colors.RESET}").strip().lower()
    
    if not target or not service:
        print(f"{Colors.RED}[-] Target and service are required{Colors.RESET}")
        return
    
    print(f"\n{Colors.CYAN}[+] Starting brute force attack on {target} ({service}){Colors.RESET}")
    
    try:
        # This would actually run hydra in a real implementation
        print(f"{Colors.YELLOW}[!] This would execute: hydra -L wordlists/usernames.txt -P wordlists/passwords.txt {target} {service}{Colors.RESET}")
        print(f"{Colors.GREEN}[+] Brute force attack simulation completed{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[-] Error: {str(e)}{Colors.RESET}")

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

def creepy_geolocation():
    print(f"\n{Colors.FIRE}>>> CREEPY GEOLOCATION <<<{Colors.RESET}")
    target = input(f"{Colors.GREEN}[?] Enter username, email, or image path: {Colors.RESET}").strip()
    
    if not target:
        print(f"{Colors.RED}[-] Please enter a target{Colors.RESET}")
        return
    
    print(f"\n{Colors.CYAN}[+] Performing geolocation analysis on {target}{Colors.RESET}")
    
    try:
        # In a real implementation, this would use actual geolocation APIs
        print(f"{Colors.YELLOW}[!] Geolocation analysis would be performed here{Colors.RESET}")
        print(f"{Colors.GREEN}[+] Analysis completed{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[-] Error: {str(e)}{Colors.RESET}")

def spiderfoot_analysis():
    print(f"\n{Colors.FIRE}>>> SPIDERFOOT OSINT ANALYSIS <<<{Colors.RESET}")
    target = input(f"{Colors.GREEN}[?] Enter domain, IP, or email: {Colors.RESET}").strip()
    
    if not target:
        print(f"{Colors.RED}[-] Please enter a target{Colors.RESET}")
        return
    
    print(f"\n{Colors.CYAN}[+] Starting SpiderFoot analysis on {target}{Colors.RESET}")
    
    try:
        # This would interface with SpiderFoot in a real implementation
        print(f"{Colors.YELLOW}[!] SpiderFoot analysis would be performed here{Colors.RESET}")
        print(f"{Colors.GREEN}[+] Analysis completed{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[-] Error: {str(e)}{Colors.RESET}")

def recon_ng_framework():
    print(f"\n{Colors.FIRE}>>> RECON-NG FRAMEWORK <<<{Colors.RESET}")
    print(f"{Colors.YELLOW}This would launch the Recon-ng framework for advanced OSINT")
    print(f"Please install Recon-ng separately to use this feature.{Colors.RESET}")

def sherlock_username():
    print(f"\n{Colors.FIRE}>>> SHERLOCK USERNAME SEARCH <<<{Colors.RESET}")
    username = input(f"{Colors.GREEN}[?] Enter username to search: {Colors.RESET}").strip()
    
    if not username:
        print(f"{Colors.RED}[-] Please enter a username{Colors.RESET}")
        return
    
    print(f"\n{Colors.CYAN}[+] Searching for username across social networks{Colors.RESET}")
    
    try:
        # In a real implementation, this would run the sherlock tool
        print(f"{Colors.YELLOW}[!] Sherlock search would be performed here{Colors.RESET}")
        print(f"{Colors.GREEN}[+] Search completed{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[-] Error: {str(e)}{Colors.RESET}")

def the_harvester():
    print(f"\n{Colors.FIRE}>>> THE HARVESTER <<<{Colors.RESET}")
    domain = input(f"{Colors.GREEN}[?] Enter domain to harvest: {Colors.RESET}").strip()
    
    if not domain:
        print(f"{Colors.RED}[-] Please enter a domain{Colors.RESET}")
        return
    
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
    
    print(f"{Colors.CYAN}[+] Generating VOIP number...{Colors.RESET}")
    
    result = create_voip_number()
    
    if "error" in result:
        print(f"{Colors.RED}[-] Error: {result['error']}{Colors.RESET}")
        return
    
    print(f"\n{Colors.GREEN}=== VOIP NUMBER CREATED ===")
    print(f"{Colors.YELLOW}Phone Number: {result.get('number', 'N/A')}")
    print(f"Provider: {result.get('provider', 'N/A')}")
    print(f"Expires: {result.get('expires', 'N/A')}")
    print(f"Setup Instructions: {result.get('instructions', 'N/A')}{Colors.RESET}")

def opsec_tools():
    print(f"\n{Colors.FIRE}>>> OPSEC TOOLS <<<{Colors.RESET}")
    ip = input(f"{Colors.GREEN}[?] Enter your IP to check: {Colors.RESET}").strip()
    
    if not ip or not re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", ip):
        print(f"{Colors.RED}[-] Invalid IP address format{Colors.RESET}")
        return
    
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
        try:
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
        except KeyboardInterrupt:
            print(f"\n{Colors.RED}[-] Operation cancelled by user{Colors.RESET}")
            continue
        except Exception as e:
            print(f"{Colors.RED}[-] Error: {str(e)}{Colors.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[-] Tool terminated by user{Colors.RESET}")
        sys.exit(0)
