SUICIDE TOOL
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import requests
from googlesearch import search
import socket
import dns.resolver
import argparse
from colorama import Fore, Style, init

init(autoreset=True)

# Banner artistico
def print_banner():
    banner = f"""
{Fore.RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
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
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠃⠁⠀⠀⠀⠀⠀⠀⠉⠛⠁  by:Ucciso
{Style.RESET_ALL}
"""
    print(banner)

# Funzioni di ricerca OSINT
def google_dorking(query, num_results=10):
    print(f"\n{Fore.YELLOW}[*] Eseguendo Google Dorking...{Style.RESET_ALL}")
    try:
        for result in search(query, num_results=num_results, stop=num_results, pause=2):
            print(f"{Fore.GREEN}[+] {result}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[-] Errore durante il Google Dorking: {e}{Style.RESET_ALL}")

def theharvester_search(domain):
    print(f"\n{Fore.YELLOW}[*] Eseguendo TheHarvester...{Style.RESET_ALL}")
    try:
        command = f"theHarvester -d {domain} -b all"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"{Fore.RED}[-] Errore durante l'esecuzione di TheHarvester: {e}{Style.RESET_ALL}")

def nmap_scan(target):
    print(f"\n{Fore.YELLOW}[*] Eseguendo Nmap scan...{Style.RESET_ALL}")
    try:
        command = f"nmap -sV -O -T4 {target}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"{Fore.RED}[-] Errore durante l'esecuzione di Nmap: {e}{Style.RESET_ALL}")

def shodan_search(query):
    print(f"\n{Fore.YELLOW}[*] Eseguendo Shodan search...{Style.RESET_ALL}")
    try:
        # Necessario avere l'API key di Shodan
        api_key = "YOUR_SHODAN_API_KEY"  # Sostituire con la propria API key
        if api_key == "YOUR_SHODAN_API_KEY":
            print(f"{Fore.RED}[-] Inserire la propria Shodan API key nello script{Style.RESET_ALL}")
            return
        
        url = f"https://api.shodan.io/shodan/host/search?key={api_key}&query={query}"
        response = requests.get(url)
        data = response.json()
        
        for result in data['matches']:
            print(f"\n{Fore.CYAN}IP: {result['ip_str']}")
            print(f"Porta: {result['port']}")
            print(f"Organizzazione: {result.get('org', 'N/A')}")
            print(f"Hostnames: {', '.join(result.get('hostnames', []))}")
            print(f"Dati: {result['data'][:100]}...{Style.RESET_ALL}")
            
    except Exception as e:
        print(f"{Fore.RED}[-] Errore durante la ricerca su Shodan: {e}{Style.RESET_ALL}")

def email_search(email):
    print(f"\n{Fore.YELLOW}[*] Ricercando informazioni sull'email...{Style.RESET_ALL}")
    try:
        # Verifica email su Have I Been Pwned
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
        headers = {"hibp-api-key": "YOUR_HIBP_API_KEY"}  # Sostituire con la propria API key
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            breaches = response.json()
            print(f"{Fore.RED}[!] Email trovata in {len(breaches)} violazioni:{Style.RESET_ALL}")
            for breach in breaches:
                print(f"- {breach['Name']} ({breach['BreachDate']})")
        else:
            print(f"{Fore.GREEN}[+] Email non trovata in violazioni conosciute{Style.RESET_ALL}")
            
        # Ricerca su Hunter.io (necessario API key)
        # hunter_api_key = "YOUR_HUNTER_API_KEY"
        # hunter_url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={hunter_api_key}"
        # hunter_response = requests.get(hunter_url)
        # hunter_data = hunter_response.json()
        # Analizzare i dati di hunter_data...
        
    except Exception as e:
        print(f"{Fore.RED}[-] Errore durante la ricerca dell'email: {e}{Style.RESET_ALL}")

def phone_lookup(phone_number):
    print(f"\n{Fore.YELLOW}[*] Ricercando informazioni sul numero di telefono...{Style.RESET_ALL}")
    try:
        # Utilizzo di NumVerify (necessario API key)
        # api_key = "YOUR_NUMVERIFY_API_KEY"
        # url = f"http://apilayer.net/api/validate?access_key={api_key}&number={phone_number}"
        # response = requests.get(url)
        # data = response.json()
        
        # Alternativa: ricerca su Truecaller (non ufficiale, potrebbe violare i ToS)
        print(f"{Fore.YELLOW}[!] Ricerca diretta del numero di telefono richiede servizi a pagamento{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}[-] Errore durante la ricerca del numero: {e}{Style.RESET_ALL}")

def discord_username_lookup(username):
    print(f"\n{Fore.YELLOW}[*] Ricercando informazioni sul nome utente Discord...{Style.RESET_ALL}")
    try:
        # Nota: Discord non fornisce un'API pubblica per la ricerca di utenti
        # Questa è una simulazione di ciò che si potrebbe fare con servizi esterni
        
        # Ricerca su social media e forum
        google_dorking(f'site:reddit.com "{username}"')
        google_dorking(f'site:twitter.com "{username}"')
        google_dorking(f'site:github.com "{username}"')
        
        # Ricerca su servizi di terze parti (esempio)
        print(f"{Fore.YELLOW}[!] Controllare manualmente servizi come Discord.id o altre utility{Style.RESET_ALL}")
        
    except Exception as e:
        print(f"{Fore.RED}[-] Errore durante la ricerca del nome utente Discord: {e}{Style.RESET_ALL}")

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(description="SUICIDE TOOL - Framework OSINT avanzato")
    parser.add_argument("-n", "--name", help="Nome completo (formato 'Nome Cognome')")
    parser.add_argument("-e", "--email", help="Indirizzo email da investigare")
    parser.add_argument("-p", "--phone", help="Numero di telefono da investigare")
    parser.add_argument("-d", "--domain", help="Dominio da investigare")
    parser.add_argument("-u", "--username", help="Nome utente Discord da investigare")
    parser.add_argument("-ip", "--ipaddress", help="Indirizzo IP da scannerizzare")
    
    args = parser.parse_args()
    
    if not any(vars(args).values()):
        parser.print_help()
        return
    
    if args.name:
        print(f"\n{Fore.BLUE}[*] Avvio ricerca per: {args.name}{Style.RESET_ALL}")
        google_dorking(f'"{args.name}"')
        google_dorking(f'"{args.name}" filetype:pdf')
        google_dorking(f'"{args.name}" site:linkedin.com')
        
    if args.email:
        print(f"\n{Fore.BLUE}[*] Avvio ricerca per email: {args.email}{Style.RESET_ALL}")
        email_search(args.email)
        google_dorking(args.email)
        
    if args.phone:
        print(f"\n{Fore.BLUE}[*] Avvio ricerca per telefono: {args.phone}{Style.RESET_ALL}")
        phone_lookup(args.phone)
        
    if args.domain:
        print(f"\n{Fore.BLUE}[*] Avvio ricerca per dominio: {args.domain}{Style.RESET_ALL}")
        theharvester_search(args.domain)
        shodan_search(f"hostname:{args.domain}")
        
    if args.username:
        print(f"\n{Fore.BLUE}[*] Avvio ricerca per nome utente Discord: {args.username}{Style.RESET_ALL}")
        discord_username_lookup(args.username)
        
    if args.ipaddress:
        print(f"\n{Fore.BLUE}[*] Avvio scansione IP: {args.ipaddress}{Style.RESET_ALL}")
        nmap_scan(args.ipaddress)
        shodan_search(f"net:{args.ipaddress}")

if __name__ == "__main__":
    main()
