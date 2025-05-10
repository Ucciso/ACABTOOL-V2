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
  1. 🕵️ INFO DISCORD (OSINT Completo)
  2. 🔐 CREDENZIALI (Email/Password/Leak)
  3. 📱 SOCIAL MEDIA (Instagram/Facebook/TikTok/GitHub/Twitter)
  4. 🛠️ STRUMENTI AGGIUNTIVI (OSINT e Sicurezza)
  5. 📍 GEOLOCALIZZAZIONE (Creepy)
  6. 📞 VOIP CREATOR (Genera numeri VoIP)
  7. 🔒 OPSEC (Protezione Anonimato)
  8. 💾 DATABREACH (Ricerca in database leak)
  9. 💀 Esci
{Colors.RESET}
"""

# =============== FUNZIONI OSINT DISCORD ===============
def discord_osint():
    print(f"\n{Colors.FIRE}>>> RICERCA OSINT DISCORD <<<{Colors.RESET}")
    discord_id = input(f"{Colors.GREEN}[?] Inserisci ID Discord: {Colors.RESET}")
    
    # API Discord (limitata)
    try:
        print(f"{Colors.CYAN}[+] Interrogazione API Discord...{Colors.RESET}")
        r = requests.get(f'https://discordlookup.mesavirepl.xyz/user/{discord_id}')
        data = r.json()
        
        if 'username' in data:
            print(f"\n{Colors.GREEN}=== INFORMAZIONI TROVATE ==={Colors.RESET}")
            print(f"{Colors.YELLOW}Username: {Colors.RESET}{data['username']}#{data['discriminator']}")
            
            if 'global_name' in data:
                print(f"{Colors.YELLOW}Nome visualizzato: {Colors.RESET}{data['global_name']}")
            
            print(f"{Colors.YELLOW}ID: {Colors.RESET}{data['id']}")
            print(f"{Colors.YELLOW}Account creato: {Colors.RESET}{data['created_at']}")
            
            if 'avatar' in data:
                print(f"{Colors.YELLOW}Avatar URL: {Colors.RESET}https://cdn.discordapp.com/avatars/{data['id']}/{data['avatar']}.png")
            
            if 'banner' in data:
                print(f"{Colors.YELLOW}Banner URL: {Colors.RESET}https://cdn.discordapp.com/banners/{data['id']}/{data['banner']}.png")
        else:
            print(f"{Colors.RED}[-] Nessuna informazione pubblica trovata via API{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[-] Errore API Discord: {e}{Colors.RESET}")
    
    # Ricerca su social media correlati
    print(f"\n{Colors.CYAN}[+] Ricerca su social media correlati...{Colors.RESET}")
    try:
        # Sherlock per username
        print(f"{Colors.YELLOW}[*] Esecuzione Sherlock...{Colors.RESET}")
        os.system(f"sherlock {data['username']} --print-found")
    except:
        print(f"{Colors.RED}[-] Sherlock non installato o errore{Colors.RESET}")
    
    # TheHarvester per email
    print(f"\n{Colors.CYAN}[+] Ricerca email correlate...{Colors.RESET}")
    try:
        os.system(f"theharvester -d {data['username']} -b google")
    except:
        print(f"{Colors.RED}[-] TheHarvester non installato o errore{Colors.RESET}")

# =============== STRUMENTI AGGIUNTIVI ===============
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
  3. Creepy (Geolocalizzazione)
  4. SpiderFoot (Analisi OSINT)
  5. Recon-ng (Framework OSINT)
  6. Sherlock (Ricerca Username)
  7. TheHarvester (Email/Subdomains)
  8. Torna al menu principale
{Colors.RESET}
""")

def run_thc_hydra():
    print(f"\n{Colors.FIRE}>>> THC-HYDRA BRUTE FORCE <<<{Colors.RESET}")
    target = input(f"{Colors.GREEN}[?] Inserisci IP/URL: {Colors.RESET}")
    service = input(f"{Colors.GREEN}[?] Servizio (ssh,ftp,http-post-form): {Colors.RESET}")
    print(f"{Colors.CYAN}[+] Avvio attacco brute force su: {target}{Colors.RESET}")
    os.system(f"hydra -L users.txt -P passwords.txt {target} {service}")

def google_dorking():
    print(f"\n{Colors.FIRE}>>> GOOGLE DORKING <<<{Colors.RESET}")
    query = input(f"{Colors.GREEN}[?] Inserisci query: {Colors.RESET}")
    print(f"{Colors.CYAN}[+] Eseguo dorking per: {query}{Colors.RESET}")
    webbrowser.open(f"https://www.google.com/search?q={query}")

def creepy_geolocation():
    print(f"\n{Colors.FIRE}>>> CREEPY GEOLOCALIZZAZIONE <<<{Colors.RESET}")
    target = input(f"{Colors.GREEN}[?] Inserisci username/email: {Colors.RESET}")
    print(f"{Colors.CYAN}[+] Avvio Creepy per: {target}{Colors.RESET}")
    os.system(f"creepy -j -o {target}.kml {target}")

def spiderfoot_osint():
    print(f"\n{Colors.FIRE}>>> SPIDERFOOT OSINT <<<{Colors.RESET}")
    target = input(f"{Colors.GREEN}[?] Inserisci dominio/IP: {Colors.RESET}")
    print(f"{Colors.CYAN}[+] Avvio SpiderFoot per: {target}{Colors.RESET}")
    os.system(f"spiderfoot -l -q -s {target}")

def recon_ng():
    print(f"\n{Colors.FIRE}>>> RECON-NG FRAMEWORK <<<{Colors.RESET}")
    print(f"{Colors.CYAN}[+] Avvio Recon-ng...{Colors.RESET}")
    os.system("recon-ng")

def sherlock_username():
    print(f"\n{Colors.FIRE}>>> SHERLOCK USERNAME SEARCH <<<{Colors.RESET}")
    username = input(f"{Colors.GREEN}[?] Inserisci username: {Colors.RESET}")
    print(f"{Colors.CYAN}[+] Ricerca username su social media...{Colors.RESET}")
    os.system(f"sherlock {username}")

def theharvester():
    print(f"\n{Colors.FIRE}>>> THEHARVESTER EMAIL/DOMAIN <<<{Colors.RESET}")
    target = input(f"{Colors.GREEN}[?] Inserisci dominio/username: {Colors.RESET}")
    print(f"{Colors.CYAN}[+] Ricerca email e subdomini...{Colors.RESET}")
    os.system(f"theharvester -d {target} -b all")

# =============== GEOLOCALIZZAZIONE ===============
def creepy_menu():
    print(f"\n{Colors.FIRE}>>> CREEPY GEOLOCALIZZAZIONE <<<{Colors.RESET}")
    target = input(f"{Colors.GREEN}[?] Inserisci username/email: {Colors.RESET}")
    print(f"{Colors.CYAN}[+] Avvio Creepy per: {target}{Colors.RESET}")
    os.system(f"creepy -j -o {target}.kml {target}")

# =============== VOIP CREATOR ===============
def voip_creator():
    print(f"\n{Colors.FIRE}>>> GENERATORE NUMERI VOIP <<<{Colors.RESET}")
    print(f"{Colors.YELLOW}[*] Generazione numero VoIP casuale...{Colors.RESET}")
    # Questo è un esempio, nella realtà servirebbe un servizio VoIP vero
    import random
    voip_num = f"+1{random.randint(200, 999)}{random.randint(100, 999)}{random.randint(1000, 9999)}"
    print(f"{Colors.GREEN}[+] Numero VoIP generato: {voip_num}{Colors.RESET}")
    print(f"{Colors.YELLOW}[*] Nota: Questo è un esempio. Per numeri reali servono servizi VoIP veri{Colors.RESET}")

# =============== OPSEC ===============
def opsec_tools():
    print(f"""
{Colors.FIRE}
  ██████╗ ██████╗ ███████╗███████╗ ██████╗
 ██╔═══██╗██╔══██╗██╔════╝██╔════╝██╔════╝
 ██║   ██║██████╔╝█████╗  █████╗  ██║     
 ██║   ██║██╔═══╝ ██╔══╝  ██╔══╝  ██║     
 ╚██████╔╝██║     ███████╗███████╗╚██████╗
  ╚═════╝ ╚═╝     ╚══════╝╚══════╝ ╚═════╝
{Colors.RESET}
{Colors.YELLOW}
  1. Verifica indirizzo IP
  2. Analisi tracce digitali
  3. Pulizia metadati
  4. Torna al menu principale
{Colors.RESET}
""")
    choice = input(f"{Colors.DEMON_RED}OPSEC{Colors.RESET}> ").strip()
    if choice == "1":
        os.system("curl ifconfig.me")
    elif choice == "2":
        os.system("bleachbit --list | grep -i metadata")
    elif choice == "3":
        os.system("mat2 --inplace *")

# =============== DATABREACH ===============
def databreach_search():
    print(f"\n{Colors.FIRE}>>> RICERCA DATABREACH <<<{Colors.RESET}")
    email = input(f"{Colors.GREEN}[?] Inserisci email/username: {Colors.RESET}")
    print(f"{Colors.CYAN}[+] Ricerca in database leakati...{Colors.RESET}")
    
    # Integrazione con Have I Been Pwned (API pubblica)
    try:
        r = requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}", 
                        headers={"hibp-api-key": "YOUR_API_KEY"})
        if r.status_code == 200:
            breaches = r.json()
            print(f"\n{Colors.RED}=== ACCOUNT COMPROMESSO IN {len(breaches)} BREACHES ==={Colors.RESET}")
            for breach in breaches:
                print(f"\n{Colors.YELLOW}Nome: {Colors.RESET}{breach['Name']}")
                print(f"{Colors.YELLOW}Data: {Colors.RESET}{breach['BreachDate']}")
                print(f"{Colors.YELLOW}Dati esposti: {Colors.RESET}{', '.join(breach['DataClasses'])}")
        else:
            print(f"{Colors.GREEN}[+] Nessuna violazione trovata per {email}{Colors.RESET}")
    except Exception as e:
        print(f"{Colors.RED}[-] Errore API: {e}{Colors.RESET}")
    
    # Ricerca locale con ripwned
    try:
        os.system(f"ripwned --email {email}")
    except:
        print(f"{Colors.RED}[-] ripwned non installato{Colors.RESET}")

# =============== MAIN ===============
def main():
    print(BANNER)
    while True:
        choice = input(f"{Colors.DEMON_RED}ACAB{Colors.RESET}@{Colors.GREEN}ToolV2{Colors.RESET}> ").strip()
        
        if choice == "1":
            discord_osint()
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
                spiderfoot_osint()
            elif tool_choice == "5":
                recon_ng()
            elif tool_choice == "6":
                sherlock_username()
            elif tool_choice == "7":
                theharvester()
        elif choice == "5":
            creepy_menu()
        elif choice == "6":
            voip_creator()
        elif choice == "7":
            opsec_tools()
        elif choice == "8":
            databreach_search()
        elif choice == "9":
            print(f"\n{Colors.RED}[-] Uscita...{Colors.RESET}")
            break

if __name__ == "__main__":
    main()
