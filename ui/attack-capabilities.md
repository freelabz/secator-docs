# Attack capabilities

This is the high-level map of the offensive and defensive capabilities you can launch from the *Run* form. Each line points to the actual tools chained together for that capability.

### Reconnaissance & asset discovery

- **DNS recon** — `subfinder`, `dnsx`, `jswhois` for passive subdomain enumeration, DNS resolution, WHOIS data.
- **Network discovery** — `arpscan`, `mapcidr`, `fping` to walk a CIDR range and probe live hosts via ARP/ICMP.
- **Port scanning** — `nmap` (full TCP/UDP, service detection, scripting) and `naabu` (fast SYN scan).
- **HTTP probing** — `httpx` to fingerprint live web servers (status, tech stack, TLS, redirects).
- **Internet-wide URL recon** — `gau`, `xurlfind3r`, `urlfinder` to harvest URLs from passive sources (Wayback, Common Crawl, AlienVault OTX, URLScan).
- **ASN / IP intelligence** — `getasn` for ASN/owner lookup.
- **Certificate inspection** — `testssl` for full TLS posture and `sshaudit` for SSH server hardening.

### Web crawling & content discovery

- **Active crawlers** — `katana`, `gospider`, `cariddi` to spider modern JS-heavy applications and extract endpoints, parameters, JS secrets, and juicy extensions.
- **Path brute-force** — `feroxbuster`, `dirsearch`, `ffuf` for recursive directory/file fuzzing with custom wordlists and matchers.
- **Sitemap reconstruction** — Combined output rendered as a clickable URL tree in the Findings page.

### Vulnerability scanning

- **Generic vulnerability scanner** — `nuclei` (10,000+ community templates: CVEs, misconfigurations, exposed panels, default credentials).
- **Multipurpose scanner** — `bbot` for chained recon-to-vuln pipelines.
- **Container & filesystem CVE scanning** — `trivy`, `grype` for SBOM-style image/filesystem checks.
- **WordPress audit** — `wpscan`, `wpprobe` for plugin enumeration and known-vulnerability detection.
- **CVE search** — `search_vulns`, `searchsploit` to map detected products/CPEs to known exploits.
- **WAF fingerprinting** — `wafw00f` to identify protective layers before further testing.

### Web vulnerability fuzzing & exploitation

- **XSS** — `dalfox` (DOM, reflected, stored), with severity scoring and PoC URL.
- **HTTP parameter discovery** — `arjun`, `x8` to find hidden GET/POST parameters not visible in the UI.
- **403/40x bypass** — `bup` to test 30+ techniques (header injection, path tricks, method override) against forbidden endpoints.
- **Pattern hunting** — `gf` patterns over crawled URLs to surface likely SQLi, SSRF, LFI, open redirect candidates.
- **Exploit attempts** — `msfconsole` modules for known CVEs (used carefully via `exploit/attack` category).

### Secrets & credential hunting

- **Source-code & filesystem secrets** — `gitleaks`, `trufflehog` over git history, repos, response bodies.
- **Email/password breach lookup** — `h8mail` to check if discovered emails appear in breach corpora.
- **Username dossier** — `maigret` to correlate a username across hundreds of social/web platforms.

### Subdomain takeovers

- The `subdomain_recon` workflow chains `subfinder` → `dnsx` → `httpx` → takeover-detection templates inside `nuclei`, surfacing dangling DNS records pointing at unclaimed cloud assets.

The full content of each scan and each workflow follows directly below.



---

See the full content of every scan and workflow in:

- [Available scans](available-scans.md)
- [Available workflows](available-workflows.md)

