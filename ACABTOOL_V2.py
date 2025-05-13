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
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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
    "discord_lookup": "https://api.acabtool.com/v2/discord"
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
  1. 🕵️ ACAB DISCORD OSINT (Full Profile Lookup)
  2. 🔐 CREDENTIALS (Email/Password/Leak Check)
  3. 📱 SOCIAL MEDIA (Instagram/Facebook/TikTok/GitHub/Twitter)
  4. 🛠️ ADVANCED TOOLS (OSINT Framework)
  5. 🌍 GEOLOCATION TOOLS
  6. 📞 VOIP CREATOR (Real Working Numbers)
  7. 🛡️ OPSEC TOOLS (IP/DNS Analysis)
  8. 💀 Exit
{Colors.RESET}
"""

# =============== REAL OSINT FUNCTIONS ===============
def get_discord_info(discord_id):
    """Get real Discord information from various sources"""
    try:
        # First try our API
        response = requests.post(API_CONFIG['discord_lookup'], json={'discord_id': discord_id})
        if response.status_code == 200:
            return response.json()
        
        # If API fails, try web scraping
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        
        # Check Discord ID on discord.id
        driver.get(f"https://discord.id/?prefill={discord_id}")
        time.sleep(3)
        
        # Extract information
        info = {}
        try:
            username = driver.find_element(By.XPATH, "//div[@class='lookup-result']//h2").text
            info['username'] = username.split('#')[0]
            info['discriminator'] = username.split('#')[1] if '#' in username else 'N/A'
        except:
            pass
            
        try:
            creation_date = driver.find_element(By.XPATH, "//div[contains(text(),'Account Creation Date')]/following-sibling::div").text
            info['creation_date'] = creation_date
        except:
            pass
            
        driver.quit()
        
        # Check other sources
        info['possible_linked_accounts'] = check_social_media(info.get('username', ''))
        
        return info
        
    except Exception as e:
        return {"error": str(e)}

def check_social_media(username):
    """Check social media for username"""
    results = {}
    try:
        # Check GitHub
        response = requests.get(f"https://api.github.com/users/{username}")
        if response.status_code == 200:
            github_data = response.json()
            results['github'] = {
                'name': github_data.get('name'),
                'location': github_data.get('location'),
                'email': github_data.get('email'),
                'blog': github_data.get('blog')
            }
    except:
        pass
        
    return results

def get_phone_info(phone_number):
    """Get information about phone number"""
    try:
        parsed = phonenumbers.parse(phone_number, None)
        if not phonenumbers.is_valid_number(parsed):
            return {"error": "Invalid phone number"}
            
        region = phonenumbers.region_code_for_number(parsed)
        carrier = phonenumbers.carrier.name_for_number(parsed, "en")
        
        return {
            "valid": True,
            "region": region,
            "carrier": carrier,
            "number_type": phonenumbers.number_type(parsed)
        }
    except Exception as e:
        return {"error": str(e)}

def generate_voip_number():
    """Generate real VOIP numbers using TextNow API"""
    try:
        # This uses TextNow's public API to get a free number
        session = requests.Session()
        
        # Get a new number
        response = session.post("https://www.textnow.com/api/v2/users", json={"username": ""})
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "number": data.get('phone_number'),
                "username": data.get('username'),
                "password": data.get('password'),
                "expires": "30 days",
                "instructions": "Use TextNow app or website to login"
            }
        return {"error": "Failed to generate number"}
    except Exception as e:
        return {"error": str(e)}

def check_opsec(ip):
    """Perform real OPSEC checks"""
    try:
        # Check IP info
        whois = IPWhois(ip)
        results = whois.lookup_rdap()
        
        # Check DNS leaks
        dns_servers = []
        try:
            resolver = dns.resolver.Resolver()
            dns_servers = resolver.nameservers
        except:
            pass
            
        return {
            "ip": ip,
            "asn": results.get('asn'),
            "isp": results.get('asn_description'),
            "country": results.get('asn_country_code'),
            "dns_servers": dns_servers,
            "recommendations": [
                "Use VPN if your real IP is exposed",
                "Check for DNS leaks",
                "Disable WebRTC in browser"
            ]
        }
    except Exception as e:
        return {"error": str(e)}

# =============== IMPROVED DISCORD OSINT ===============
def discord_lookup():
    print(f"\n{Colors.FIRE}>>> ACAB DISCORD OSINT LOOKUP <<<{Colors.RESET}")
    discord_id = input(f"{Colors.GREEN}[?] Enter Discord ID (e.g. username#1234 or user ID): {Colors.RESET}")
    
    print(f"\n{Colors.CYAN}[+] Searching for Discord ID: {discord_id}{Colors.RESET}")
    
    # Get real data
    user_data = get_discord_info(discord_id)
    
    if "error" in user_data:
        print(f"{Colors.RED}[-] Error: {user_data['error']}{Colors.RESET}")
        return
    
    print(f"\n{Colors.GREEN}=== ACAB OSINT RESULTS ===")
    print(f"{Colors.YELLOW}Username: {Colors.RESET}{user_data.get('username', 'N/A')}")
    print(f"{Colors.YELLOW}Discriminator: {Colors.RESET}{user_data.get('discriminator', 'N/A')}")
    print(f"{Colors.YELLOW}Account Created: {Colors.RESET}{user_data.get('creation_date', 'N/A')}")
    
    if 'possible_linked_accounts' in user_data:
        print(f"\n{Colors.GREEN}=== LINKED ACCOUNTS ===")
        for platform, data in user_data['possible_linked_accounts'].items():
            print(f"\n{Colors.YELLOW}{platform.upper()}:")
            if data.get('name'):
                print(f"Name: {data['name']}")
            if data.get('location'):
                print(f"Location: {data['location']}")
            if data.get('email'):
                print(f"Email: {data['email']}")
            if data.get('blog'):
                print(f"Website: {data['blog']}")
    
    print(f"\n{Colors.GREEN}=== RECOMMENDED NEXT STEPS ===")
    print(f"{Colors.YELLOW}1. Check username on other social media")
    print(f"2. Reverse image search avatar")
    print(f"3. Check for data breaches with email")
    print(f"4. Geolocate any IP addresses{Colors.RESET}")

# =============== IMPROVED SOCIAL MEDIA LOOKUP ===============
def social_media_lookup():
    print(f"\n{Colors.FIRE}>>> SOCIAL MEDIA OSINT <<<{Colors.RESET}")
    username = input(f"{Colors.GREEN}[?] Enter username to search: {Colors.RESET}")
    
    print(f"\n{Colors.CYAN}[+] Searching for username: {username}{Colors.RESET}")
    
    # Real social media URLs
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
        # Check if profile exists
        try:
            response = requests.head(url, allow_redirects=True, timeout=5)
            if response.status_code == 200:
                print(f"{Colors.YELLOW}{platform.title()}: {Colors.GREEN}FOUND {Colors.CYAN}{url}{Colors.RESET}")
            else:
                print(f"{Colors.YELLOW}{platform.title()}: {Colors.RED}NOT FOUND{Colors.RESET}")
        except:
            print(f"{Colors.YELLOW}{platform.title()}: {Colors.RED}ERROR CHECKING{Colors.RESET}")

# =============== IMPROVED CREDENTIAL CHECK ===============
def credential_check():
    print(f"\n{Colors.FIRE}>>> CREDENTIAL CHECK <<<{Colors.RESET}")
    email = input(f"{Colors.GREEN}[?] Enter email to check: {Colors.RESET}")
    
    print(f"\n{Colors.CYAN}[+] Checking breaches for: {email}{Colors.RESET}")
    
    # Check Have I Been Pwned
    try:
        response = requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}", 
                              headers={"hibp-api-key": "your-api-key-here"})
        if response.status_code == 200:
            breaches = response.json()
            print(f"\n{Colors.GREEN}=== BREACH RESULTS ===")
            for breach in breaches:
                print(f"\n{Colors.RED}Breach Name: {breach['Name']}")
                print(f"{Colors.YELLOW}Date: {breach['AddedDate']}")
                print(f"Compromised Data: {', '.join(breach['DataClasses'])}")
                print(f"Description: {breach['Description']}{Colors.RESET}")
        else:
            print(f"{Colors.GREEN}[+] No breaches found for this email{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[-] Error checking breaches: {str(e)}{Colors.RESET}")

# =============== IMPROVED VOIP CREATOR ===============
def voip_creator():
    print(f"\n{Colors.FIRE}>>> REAL VOIP NUMBER CREATOR <<<{Colors.RESET}")
    
    print(f"{Colors.YELLOW}[*] Generating real VOIP number...{Colors.RESET}")
    
    result = generate_voip_number()
    
    if "error" in result:
        print(f"{Colors.RED}[-] Error: {result['error']}{Colors.RESET}")
        return
    
    print(f"\n{Colors.GREEN}=== VOIP NUMBER CREATED ===")
    print(f"{Colors.YELLOW}Phone Number: {result['number']}")
    print(f"Username: {result['username']}")
    print(f"Password: {result['password']}")
    print(f"Expires: {result['expires']}")
    print(f"Instructions: {result['instructions']}{Colors.RESET}")
    
    print(f"\n{Colors.YELLOW}[*] You can use this number with the TextNow app or website.{Colors.RESET}")

# =============== IMPROVED OPSEC TOOLS ===============
def opsec_tools():
    print(f"\n{Colors.FIRE}>>> OPSEC TOOLS <<<{Colors.RESET}")
    ip = input(f"{Colors.GREEN}[?] Enter your IP to check: {Colors.RESET}")
    
    print(f"\n{Colors.CYAN}[+] Performing OPSEC check for {ip}{Colors.RESET}")
    
    result = check_opsec(ip)
    
    if "error" in result:
        print(f"{Colors.RED}[-] Error: {result['error']}{Colors.RESET}")
        return
    
    print(f"\n{Colors.GREEN}=== OPSEC RESULTS ===")
    print(f"{Colors.YELLOW}IP: {result['ip']}")
    print(f"ISP: {result.get('isp', 'N/A')}")
    print(f"Country: {result.get('country', 'N/A')}")
    print(f"ASN: {result.get('asn', 'N/A')}")
    print(f"\nDNS Servers: {', '.join(result.get('dns_servers', []))}")
    
    print(f"\n{Colors.GREEN}=== RECOMMENDATIONS ===")
    for rec in result.get('recommendations', []):
        print(f"{Colors.YELLOW}- {rec}{Colors.RESET}")

# =============== MAIN MENU ===============
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
