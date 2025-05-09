#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import subprocess
import webbrowser
import json
from datetime import datetime

# =============== CONFIGURAZIONE COLORI WINDOWS ===============
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

# =============== BANNER PULITO ===============
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
  1. 🕵️ INFO DISCORD (ID Lookup)
  2. 🔐 CREDENZIALI (Email/Password/Leak)
  3. 📱 SOCIAL MEDIA (Instagram/Facebook/TikTok/GitHub/Twitter)
  4. 🛠️ STRUMENTI AGGIUNTIVI (THC-Hydra, Google Dorking, etc.)
  5. 💀 Esci
{Colors.RESET}
"""

# =============== FUNZIONI PRINCIPALI ===============
def discord_lookup():
    print(f"\n{Colors.FIRE}>>> RICERCA ID DISCORD <<<{Colors.RESET}")
    discord_id = input(f"{Colors.GREEN}[?] Inserisci ID Discord: {Colors.RESET}")
    print(f"{Colors.CYAN}[+] Ricerca in corso per ID: {discord_id}{Colors.RESET}")

def run_thc_hydra():
    print(f"\n{Colors.FIRE}>>> THC-HYDRA BRUTE FORCE <<<{Colors.RESET}")
    target = input(f"{Colors.GREEN}[?] Inserisci IP/URL: {Colors.RESET}")
    print(f"{Colors.CYAN}[+] Avvio attacco brute force su: {target}{Colors.RESET}")

def google_dorking():
    print(f"\n{Colors.FIRE}>>> GOOGLE DORKING <<<{Colors.RESET}")
    query = input(f"{Colors.GREEN}[?] Inserisci query: {Colors.RESET}")
    print(f"{Colors.CYAN}[+] Eseguo dorking per: {query}{Colors.RESET}")

# =============== MENU STRUMENTI ===============
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
  3. Torna al menu principale
{Colors.RESET}
""")

# =============== MAIN ===============
def main():
    print(BANNER)
    while True:
        choice = input(f"{Colors.DEMON_RED}ACAB{Colors.RESET}@{Colors.GREEN}ToolV2{Colors.RESET}> ").strip()
        
        if choice == "1":
            discord_lookup()
        elif choice == "4":
            show_tools_menu()
            tool_choice = input(f"{Colors.DEMON_RED}TOOLS{Colors.RESET}> ").strip()
            if tool_choice == "1":
                run_thc_hydra()
            elif tool_choice == "2":
                google_dorking()
        elif choice == "5":
            print(f"\n{Colors.RED}[-] Uscita...{Colors.RESET}")
            break

if __name__ == "__main__":
    main()