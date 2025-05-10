import os
import subprocess

def run(cmd):
    print(f"[+] Running: {cmd}")
    subprocess.run(cmd, shell=True, executable="/bin/bash")

def make_dirs(base):
    paths = {
        "subdomains": f"{base}/1_subdomains",
        "perms": f"{base}/2_permutations",
        "alive": f"{base}/3_alive",
        "spider": f"{base}/4_spidering",
        "gf": f"{base}/5_gf_analysis",
        "js": f"{base}/6_js_analysis"
    }
    for path in paths.values():
        os.makedirs(path, exist_ok=True)
    return paths

def recon(domain):
    base = f"recon/{domain}"
    paths = make_dirs(base)

    # Step 1: Subdomain Enumeration
    sub_output = f"{paths['subdomains']}/all_subs.txt"
    run(f"subfinder -d {domain} -silent > {sub_output}")
    run(f"assetfinder --subs-only {domain} >> {sub_output}")
    run(f"findomain --quiet -t {domain} >> {sub_output}")
    run(f"chaos -d {domain} >> {sub_output}")
    run(f"github-subdomains -d {domain} >> {sub_output}")
    run(f"gitlab-subdomains -d {domain} >> {sub_output}")
    run(f"sort -u {sub_output} -o {sub_output}")

    # Step 2: Subdomain Permutation and Bruteforce
    dnsgen_out = f"{paths['perms']}/dnsgen.txt"
    puredns_out = f"{paths['perms']}/bruteforced.txt"
    run(f"dnsgen {sub_output} > {dnsgen_out}")
    run(f"puredns bruteforce {dnsgen_out} -r resolvers.txt -w wordlist.txt --write {puredns_out}")

    # Step 3: Identify Live Subdomains
    alive_output = f"{paths['alive']}/alive.txt"
    run(f"cat {sub_output} {puredns_out} | sort -u | httpx -silent > {alive_output}")

    # Step 5: Content Discovery (Spidering)
    gospider_out = f"{paths['spider']}/gospider.txt"
    katana_out = f"{paths['spider']}/katana.txt"
    gau_out = f"{paths['spider']}/gau.txt"
    run(f"gospider -S {alive_output} -o {gospider_out} -c 10 --no-redirect --quiet")
    run(f"cat {alive_output} | katana -silent > {katana_out}")
    run(f"cat {alive_output} | gau > {gau_out}")

    # Step 6: Analyze Spidering Output for Vulnerabilities (GF)
    all_spider_data = f"{paths['spider']}/combined_urls.txt"
    run(f"cat {gospider_out} {katana_out} {gau_out} | sort -u > {all_spider_data}")
    gf_patterns = ['xss', 'sqli', 'lfi', 'ssrf', 'redirect', 'rce']
    for pattern in gf_patterns:
        out_file = f"{paths['gf']}/{pattern}.txt"
        run(f"cat {all_spider_data} | gf {pattern} > {out_file}")

    # Step 7: JavaScript Analysis for Secrets
    js_dir = paths['js']
    run(f"getJS --input {alive_output} --complete --output {js_dir}/js_links.txt")
    run(f"cat {js_dir}/js_links.txt | cariddi -o {js_dir}/cariddi_output.txt")

    print(f"\n[✓] Recon automation complete! Results saved in recon/{domain}/")

if __name__ == "__main__":
    target = input("Enter the target domain: ").strip()
    recon(target)
