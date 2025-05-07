# AUTO_SUBDOM_ENUM
## INTRODUCTION
This automated subdomain enumeration script is a powerful Python-based tool that discovers subdomains of a target domain, checks which ones are active, and provides a color-coded terminal output for better readability.
## FEATURES
passive and active subdomain enumeration using:
1) amass
2) subfinder
3) crt.sh (optional certificate-based lookup)
4) Verifies which discovered subdomains are active
5) Automatically installs missing tools(amass, subfinder) using apt
6) Colorful terminal output for readability
## REQUIREMENTS
1) python3
2) requests module(pip install requests)
3) amass(installed automatically if not available)
4) subfinder(installed automatically if not available)
## INSTALLATION
Clone the repository:
```bash
git clone https://github.com/yourusername/subdomain-enum-script.git
```
Change the directory:
```bash
cd subdomain-enum-script
```
## USAGE
```bash
python3 enum_script.py -d example.com --crtsh
```
## ARGUMENTS
-d: (Required) domain scan.

--crtsh:  (Optional) Use crt.sh to find more subdomains



