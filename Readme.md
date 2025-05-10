<h1><b>Bug Bounty Recon Automation Tool<b></h1>
This tool automates bug bounty reconnaissance workflow using the best open-source tools for each phase. It performs deep subdomain enumeration, live host detection, spidering, GF pattern detection, and JavaScript secret analysis.

Directory Structure
After running the script, you’ll get output in:
recon/
└── example.com/
    ├── 1_subdomains/       # All subdomains from all sources
    ├── 2_permutations/     # Dnsgen + Puredns brute-forced subdomains
    ├── 3_alive/            # Alive hosts (httpx)
    ├── 4_spidering/        # GoSpider, Katana, GAU URLs
    ├── 5_gf_analysis/      # GF pattern matched URLs (xss, sqli, etc.)
    └── 6_js_analysis/      # getJS & Cariddi output


Tools Required
Ensure these are installed and in $PATH:

subfinder, assetfinder, findomain, chaos, github-subdomains, gitlab-subdomains

dnsgen, puredns

httpx, gospider, katana, gau, gf

getJS, cariddi

Also include:

resolvers.txt → list of DNS resolvers

wordlist.txt → subdomain brute-force wordlist



USAGE : 

git clone https://github.com/yourusername/recon-automation
cd recon-automation

python3 recon.py

INSTALLATION STEPS : 

sudo apt install golang git python3 -y
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install github.com/tomnomnom/assetfinder@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
go install github.com/projectdiscovery/chaos-client/cmd/chaos@latest
go install github.com/tomnomnom/gf@latest
go install github.com/ffuf/dnsgen@latest
# And install gospider, katana, getJS, cariddi from their GitHub repos
