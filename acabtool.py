ACABTOOL V2
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

# =============== LA TUA TEXT ART ===============
BANNER = r"""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
[ ... INSERISCI TUTTA LA TUA TEXT ART ... ]
""" + f"""
{Colors.FIRE}
   █████╗  ██████╗ █████╗ ██████╗     ████████╗ ██████╗  ██████╗ ██╗     
 ██╔══██╗██╔════╝██╔══██╗██╔══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
 ███████║██║     ███████║██████╔╝       ██║   ██║   ██║██║   ██║██║     
 ██╔══██║██║     ██╔══██║██╔══██╗       ██║   ██║   ██║██║   ██║██║     
 ██║  ██║╚██████╗██║  ██║██║  ██║       ██║   ╚██████╔╝╚██████╔╝███████╗
 ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝       ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝
{Colors.RESET}
{Colors.YELLOW}
  1.
bro questa vabene devi solo spiegarmi come installarlo su windows
Ecco la **guida completa per installare e far funzionare il tool su

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import requests
import subprocess
import webbrowser
import json
from datetime import datetime

# =============== COLORI ORIGINALI ===============
class Colors:
    DEMON_RED = "\033[38;2;255;36;0m"
    BLOOD = "\033[38;2;200;0;0m"
    FIRE = "\033[38;2;255;69;0m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    RESET = "\033[0m"

# =============== LA TUA TEXT ART ORIGINALE ===============
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

# =============== TUTTI GLI STRUMENTI INTEGRATI ===============
def discord_lookup():
    print(f"\n{Colors.FIRE}>>> RICERCA ID DISCORD <<<{Colors.RESET}")
    discord_id = input(f"{Colors.GREEN}[?] Inserisci ID Discord: {Colors.RESET}")
    # Implementazione completa qui...

def run_thc_hydra():
    print(f"\n{Colors.FIRE}>>> THC-HYDRA BRUTE FORCE <<<{Colors.RESET}")
    # Implementazione completa qui...

def google_dorking():
    print(f"\n{Colors.FIRE}>>> GOOGLE DORKING <<<{Colors.RESET}")
    # Implementazione completa qui...

def run_theharvester():
    print(f"\n{Colors.FIRE}>>> THEHARVESTER OSINT <<<{Colors.RESET}")
    # Implementazione completa qui...

def run_creepy():
    print(f"\n{Colors.FIRE}>>> CREEPY GEOLOCALIZZAZIONE <<<{Colors.RESET}")
    # Implementazione completa qui...

def run_spiderfoot():
    print(f"\n{Colors.FIRE}>>> SPIDERFOOT ANALISI <<<{Colors.RESET}")
    # Implementazione completa qui...

def run_reconng():
    print(f"\n{Colors.FIRE}>>> RECON-NG FRAMEWORK <<<{Colors.RESET}")
    # Implementazione completa qui...

def run_sherlock():
    print(f"\n{Colors.FIRE}>>> SHERLOCK USERNAME <<<{Colors.RESET}")
    # Implementazione completa qui...

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
  3. TheHarvester (Email/Subdomains)
  4. Creepy (Geolocalizzazione)
  5. SpiderFoot (Analisi OSINT)
  6. Recon-ng (Framework OSINT)
  7. Sherlock (Ricerca Username)
  8. Torna al menu principale
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
            elif tool_choice == "3":
                run_theharvester()
            elif tool_choice == "4":
                run_creepy()
            elif tool_choice == "5":
                run_spiderfoot()
            elif tool_choice == "6":
                run_reconng()
            elif tool_choice == "7":
                run_sherlock()
        elif choice == "5":
            print(f"\n{Colors.RED}[-] Uscita...{Colors.RESET}")
            break

if __name__ == "__main__":
    main()