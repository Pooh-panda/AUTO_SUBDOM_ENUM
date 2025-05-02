import argparse
import subprocess
import requests

# Text colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"

# Style
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
RESET = "\033[0m"  # Resets color back to default


def query_crtsh(domain):
    print(f"""\n{CYAN}===========({RESET} {MAGENTA}Querying crt.sh for subdomains{RESET} {CYAN})==========={RESET}""")
    try:
        url = f"https://crt.sh/"
        params = {'q': domain, 'output': 'json'}
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Te': 'trailers',
        }
        response = requests.get(url=url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            subdomains = set()
            for entry in data:
                name_value = entry.get('name_value')
                if name_value:
                    subdomains.update(name_value.split('\n'))
            return list(subdomains)
        else:
            print(f"crt.sh QUERY FAILED WITH STATUS CODE: {response.status_code}")
            return []
    except Exception as e:
        print(f"ERROR QUERYING crt.sh: {e}")
        return []

def verify_subdomains(domain, subdomains):
    """Verify which subdomains are active."""
    print(f"\n{GREEN}VERIFYING DISCOVERED SUBDOMAINS...{RESET}")
    active_subdomains = []
    for subdomain in subdomains:
        url = f"http://{subdomain}"
        try:
            response = requests.get(url, timeout=3)
            if response.status_code < 400:
                print(f"[+] {BOLD}ACTIVE:{RESET} {YELLOW}{url}{RESET}")
                active_subdomains.append(subdomain)
        except requests.RequestException:
            pass
    return active_subdomains

def enum_with_amass(domain: str):
    try:
        print(f'\n{CYAN}==========({RESET} {MAGENTA}enumerating domain with amass{RESET} {CYAN})==========={RESET}')
        command = ['amass', 'enum', '-d', domain]
        result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in result.stdout:
            print(line, end='')
        result.wait()
    except Exception as e:
        print(f'ERROR: {e}')

def enum_with_subfinder(domain: str):
    print(f'\n{CYAN}==========({RESET} {MAGENTA}enumerating domain with subfinder{RESET} {CYAN})==========={RESET}')
    try:
        command = ['subfinder', '-d', domain]
        result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in result.stdout:
            print(line, end='')
        result.wait()
    except Exception as e:
        print(f'ERROR: {e}')

def install_tool(tool: str):
    print(f'Installing {tool} using apt...')
    try:
        subprocess.run(['sudo', 'apt', 'update'], check=True)
        subprocess.run(['sudo', 'apt', 'install', tool], check=True)
        print(f'{tool} installed successfully')
        return True
    except subprocess.CalledProcessError as e:
        print(f"Could not install {tool}. Try using 'sudo apt install {tool}'")
        return False

def main():
    parser = argparse.ArgumentParser(description="Automated Subdomain Enumeration Script")
    parser.add_argument('-d', '--domain', type=str, required=True, help="Target domain for subdomain enumeration")
    parser.add_argument('-c', '--crtsh', action='store_true', help="Include crt.sh in enumeration")
    args = parser.parse_args()

    domain = args.domain

    if not subprocess.run(['which', 'subfinder'], capture_output=True).stdout.strip():
        print(f'subfinder not installed, installing...')
        if not install_tool(tool='subfinder'):
            return

    if not subprocess.run(['which', 'amass'], capture_output=True).stdout.strip():
        print(f'amass not installed, installing...')
        if not install_tool(tool='amass'):
            return

    if args.crtsh:
        subdomains = query_crtsh(domain)
        print(f"{GREEN}Found {len(subdomains)} subdomains from crt.sh.{RESET}")
        for sub in subdomains:
        	print(sub)
        active = verify_subdomains(domain, subdomains)
        print(f"\n{GREEN}{len(active)} ACTIVE subdomains discovered from crt.sh.{RESET}")
        for sub in active:
        	print(sub)
    #enum_with_subfinder(domain)
    enum_with_amass(domain)

if __name__ == '__main__':
    main()
