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
import time
from colorama import init, Fore, Back, Style

# Initialize colorama
init()

# =============== CONFIGURATION ===============
class Colors:
    DEMON_RED = Fore.RED + Style.BRIGHT
    BLOOD = Fore.RED
    FIRE = Fore.YELLOW + Style.BRIGHT
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    CYAN = Fore.CYAN
    RESET = Style.RESET_ALL

# API configurations
API_CONFIG = {
    "discord_lookup": "https://discordlookup.mesavirep.xyz/v1/user/",
    "breach_api": "https://haveibeenpwned.com/api/v3/breachedaccount/",
    "phone_lookup": "https://api.numlookupapi.com/v1/",
    "voip_api": "https://api.voip.ms/api/v1/rest.php",
    "ip_api": "http://ip-api.com/json/"
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
  6. 📞 VOIP CREATOR
  7. 🛡️ OPSEC TOOLS
  8. 💀 Exit
{Colors.RESET}
"""

# =============== API FUNCTIONS ===============
def get_discord_user(user_id):
    """Get Discord user information from API"""
    try:
        response = requests.get(f"{API_CONFIG['discord_lookup']}{user_id}")
        if response.status_code == 200:
            return response.json()
        return {"error": "User not found or API error"}
    except Exception as e:
        return {"error": str(e)}

def check_breaches(email):
    """Check email breaches using HaveIBeenPwned API"""
    try:
        headers = {"hibp-api-key": "your-api-key-here"}  # You need to get your own API key
        response = requests.get(f"{API_CONFIG['breach_api']}{email}", headers=headers)
        if response.status_code == 200:
            return response.json()
        return {"error": "No breaches found or API error"}
    except Exception as e:
        return {"error": str(e)}

def lookup_phone_number(phone):
    """Lookup phone number information"""
    try:
        response = requests.get(f"{API_CONFIG['phone_lookup']}{phone}?apikey=your-api-key")
        if response.status_code == 200:
            return response.json()
        return {"error": "Phone lookup failed"}
    except Exception as e:
        return {"error": str(e)}

def create_voip_number():
    """Create VOIP number using VoIP.ms API"""
    try:
        params = {
            'api_username': 'your_username',
            'api_password': 'your_password',
            'method': 'getDIDCountries'
        }
        response = requests.get(API_CONFIG['voip_api'], params=params)
        if response.status_code == 200:
            return response.json()
        return {"error": "VOIP API request failed"}
    except Exception as e:
        return {"error": str(e)}

def ip_lookup(ip):
    """Perform IP lookup"""
    try:
        response = requests.get(f"{API_CONFIG['ip_api']}{ip}")
        if response.status_code == 200:
            return response.json()
        return {"error": "IP lookup failed"}
    except Exception as e:
        return {"error": str(e)}

# =============== OSINT FUNCTIONS ===============
def discord_lookup():
    print(f"\n{Colors.FIRE}>>> ACAB DISCORD OSINT LOOKUP <<<{Colors.RESET}")
    discord_id = input(f"{Colors.GREEN}[?] Enter Discord ID: {Colors.RESET}").strip()
    
    if not discord_id.isdigit():
        print(f"{Colors.RED}[-] Invalid Discord ID format{Colors.RESET}")
        return
    
    print(f"\n{Colors.CYAN}[+] Searching for Discord ID: {discord_id}{Colors.RESET}")
    
    user_data = get_discord_user(discord_id)
    
    if "error" in user_data:
        print(f"{Colors.RED}[-] Error: {user_data['error']}{Colors.RESET}")
        return
    
    # Enhanced data gathering from public sources
    print(f"\n{Colors.GREEN}=== ACAB DISCORD USER INFORMATION ===")
    print(f"{Colors.YELLOW}Username: {Colors.RESET}{user_data.get('username', 'N/A')}#{user_data.get('discriminator', '0000')}")
    print(f"{Colors.YELLOW}Global Name: {Colors.RESET}{user_data.get('global_name', 'N/A')}")
    print(f"{Colors.YELLOW}Avatar URL: {Colors.RESET}{user_data.get('avatar_url', 'N/A')}")
    
    # Try to find additional public information
    try:
        # This would be replaced with actual OSINT techniques in a real tool
        additional_info = find_public_info(user_data.get('username'))
        
        print(f"\n{Colors.GREEN}=== PUBLIC RECORDS FOUND ===")
        if additional_info.get('full_name'):
            print(f"{Colors.YELLOW}Full Name: {Colors.RESET}{additional_info['full_name']}")
        if additional_info.get('birth_date'):
            print(f"{Colors.YELLOW}Birth Date: {Colors.RESET}{additional_info['birth_date']}")
        if additional_info.get('location'):
            print(f"{Colors.YELLOW}Location: {Colors.RESET}{additional_info['location']}")
        if additional_info.get('phone'):
            print(f"{Colors.YELLOW}Phone Number: {Colors.RESET}{additional_info['phone']}")
            phone_info = lookup_phone_number(additional_info['phone'])
            if not phone_info.get('error'):
                print(f"{Colors.YELLOW}Carrier: {Colors.RESET}{phone_info.get('carrier', 'N/A')}")
                print(f"{Colors.YELLOW}Country: {Colors.RESET}{phone_info.get('country_name', 'N/A')}")
        if additional_info.get('relatives'):
            print(f"\n{Colors.GREEN}=== FAMILY INFORMATION ===")
            for rel in additional_info['relatives']:
                print(f"{Colors.YELLOW}{rel['relation']}: {Colors.RESET}{rel['name']}")
    except Exception as e:
        print(f"{Colors.RED}[-] Could not retrieve additional public records: {str(e)}{Colors.RESET}")

def find_public_info(username):
    """Simulate finding public information about a user"""
    # In a real tool, this would use actual OSINT techniques to find public records
    # This is just a simulation of what might be found
    
    # Simulate finding info based on username patterns
    if "john" in username.lower():
        return {
            "full_name": "John Doe",
            "birth_date": "1990-05-15",
            "location": "New York, USA",
            "phone": "+15551234567",
            "relatives": [
                {"relation": "Mother", "name": "Jane Doe"},
                {"relation": "Father", "name": "Robert Doe"}
            ]
        }
    elif "jane" in username.lower():
        return {
            "full_name": "Jane Smith",
            "birth_date": "1985-08-22",
            "location": "Los Angeles, USA",
            "phone": "+15559876543",
            "relatives": [
                {"relation": "Mother", "name": "Mary Smith"},
                {"relation": "Father", "name": "John Smith"}
            ]
        }
    else:
        return {
            "full_name": "Unknown",
            "birth_date": "Unknown",
            "location": "Unknown",
            "phone": "Unknown",
            "relatives": []
        }

def credential_check():
    print(f"\n{Colors.FIRE}>>> CREDENTIAL CHECK <<<{Colors.RESET}")
    email = input(f"{Colors.GREEN}[?] Enter email to check: {Colors.RESET}").strip()
    
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        print(f"{Colors.RED}[-] Invalid email format{Colors.RESET}")
        return
    
    print(f"\n{Colors.CYAN}[+] Checking breaches for: {email}{Colors.RESET}")
    
    result = check_breaches(email)
    
    if "error" in result:
        print(f"{Colors.RED}[-] Error: {result['error']}{Colors.RESET}")
        return
    
    print(f"\n{Colors.GREEN}=== BREACH RESULTS ===")
    if isinstance(result, list) and len(result) > 0:
        for breach in result:
            print(f"\n{Colors.RED}Breach Name: {breach['Name']}")
            print(f"{Colors.YELLOW}Date: {breach['BreachDate']}")
            print(f"Compromised Data: {', '.join(breach['DataClasses'])}")
            print(f"Description: {breach['Description']}{Colors.RESET}")
    else:
        print(f"{Colors.GREEN}[+] No breaches found for this email{Colors.RESET}")

def social_media_lookup():
    print(f"\n{Colors.FIRE}>>> SOCIAL MEDIA OSINT <<<{Colors.RESET}")
    username = input(f"{Colors.GREEN}[?] Enter username to search: {Colors.RESET}").strip()
    
    print(f"\n{Colors.CYAN}[+] Searching for username: {username}{Colors.RESET}")
    
    # Check if username exists on various platforms
    platforms = {
        "Instagram": f"https://instagram.com/{username}",
        "Facebook": f"https://facebook.com/{username}",
        "Twitter": f"https://twitter.com/{username}",
        "TikTok": f"https://tiktok.com/@{username}",
        "GitHub": f"https://github.com/{username}",
        "LinkedIn": f"https://linkedin.com/in/{username}"
    }
    
    print(f"\n{Colors.GREEN}=== SOCIAL MEDIA CHECK ===")
    for platform, url in platforms.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"{Colors.YELLOW}{platform}: {Colors.GREEN}Found {Colors.CYAN}({url}){Colors.RESET}")
            else:
                print(f"{Colors.YELLOW}{platform}: {Colors.RED}Not Found{Colors.RESET}")
        except:
            print(f"{Colors.YELLOW}{platform}: {Colors.RED}Error checking{Colors.RESET}")

def voip_creator():
    print(f"\n{Colors.FIRE}>>> VOIP NUMBER CREATOR <<<{Colors.RESET}")
    
    print(f"{Colors.YELLOW}[!] This requires a VoIP.ms account with API access{Colors.RESET}")
    print(f"{Colors.YELLOW}[!] Please configure your API credentials in the code{Colors.RESET}")
    
    result = create_voip_number()
    
    if "error" in result:
        print(f"{Colors.RED}[-] Error: {result['error']}{Colors.RESET}")
        return
    
    print(f"\n{Colors.GREEN}=== VOIP NUMBER CREATED ===")
    if result.get('countries'):
        print(f"{Colors.YELLOW}Available Countries:")
        for country in result['countries']:
            print(f"- {country['country']} ({country['country_code']})")
    else:
        print(f"{Colors.YELLOW}No countries available. Check your API credentials.{Colors.RESET}")

def opsec_tools():
    print(f"\n{Colors.FIRE}>>> OPSEC TOOLS <<<{Colors.RESET}")
    ip = input(f"{Colors.GREEN}[?] Enter IP to check (leave blank for your IP): {Colors.RESET}").strip() or None
    
    if ip is None:
        try:
            ip = requests.get('https://api.ipify.org').text
        except:
            print(f"{Colors.RED}[-] Could not determine your IP address{Colors.RESET}")
            return
    
    print(f"\n{Colors.CYAN}[+] Performing OPSEC check for {ip}{Colors.RESET}")
    
    result = ip_lookup(ip)
    
    if "error" in result:
        print(f"{Colors.RED}[-] Error: {result['error']}{Colors.RESET}")
        return
    
    print(f"\n{Colors.GREEN}=== OPSEC RESULTS ===")
    print(f"{Colors.YELLOW}IP: {ip}")
    print(f"ISP: {result.get('isp', 'N/A')}")
    print(f"Organization: {result.get('org', 'N/A')}")
    print(f"Location: {result.get('city', 'N/A')}, {result.get('country', 'N/A')}")
    print(f"AS Number: {result.get('as', 'N/A')}")
    print(f"Proxy/VPN: {'Yes' if result.get('proxy', False) else 'No'}")
    
    print(f"\n{Colors.GREEN}=== RECOMMENDATIONS ===")
    if result.get('proxy', False):
        print(f"{Colors.GREEN}[+] You appear to be using a proxy/VPN - good practice{Colors.RESET}")
    else:
        print(f"{Colors.RED}[-] You are not using a proxy/VPN - consider using one{Colors.RESET}")

# =============== MAIN MENU ===============
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
                print(f"\n{Colors.YELLOW}[!] Advanced tools would be implemented here{Colors.RESET}")
            elif choice == "5":
                print(f"\n{Colors.YELLOW}[!] Geolocation tools would be implemented here{Colors.RESET}")
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
            print(f"\n{Colors.RED}[-] Exiting...{Colors.RESET}")
            break
        except Exception as e:
            print(f"{Colors.RED}[-] Error: {str(e)}{Colors.RESET}")

if __name__ == "__main__":
    main()
