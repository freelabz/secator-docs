# Available workflows

15 workflows ship with the platform. Each one chains tasks (security tools) into a coherent recon or assessment flow. The task tree below each workflow is the live view you see when monitoring a run; conditions (`if …`) reflect the option flags that gate each task.

Workflows are picked from the **Run** form (Workspace → *Run* → *Workflow* tab).

---

### `cidr_recon` <a id="cidr_recon"></a>

_Local network reconnaissance_

Discovers and analyzes hosts within a CIDR range or local network through ARP / ICMP scanning.
Maps IP addresses and identifies live hosts.
Useful for local network security assessments and penetration testing.

**Input types:** `cidr_range` `ip` `slug`

**Tags:** `recon` `cidr` `network` `vuln` `internal`

**Task tree:**

- 📂 ***discover*** *(parallel group)*
  - 🔧 `netdetect` — Discover local network CIDR ranges — *if `targets`*
  - 🔧 `arp` — Discover neighbors with ARP requests — *if `targets`*
- 🔧 `prompt` — Select a CIDR range manually
- 📂 ***probe*** *(parallel group)*
  - 🔧 `arpscan` — Discover hosts with ARP requests
  - 🔧 `fping` — Discover hosts with ICMP requests
  - 🔧 `nmap` — Discover live hosts with ping scan


---

### `code_scan` <a id="code_scan"></a>

_Code vulnerability scan and secret hunt_

Analyzes source code repositories and filesystems for security vulnerabilities and exposed secrets.
Scans dependencies for known CVEs, detects hardcoded credentials, API keys, and sensitive data
in code. Supports multiple input types including local paths, Git repositories, and cloud storage.
Essential for DevSecOps and identifying security issues before deployment.

**Input types:** `path` `url` `gcs_url` `string`

**Tags:** `vuln` `secret` `code`

**Task tree:**

- 🔧 `_group`


---

### `domain_recon` <a id="domain_recon"></a>

_Domain reconnaissance_

Performs comprehensive reconnaissance on a domain to gather essential information.
Collects WHOIS data, probes HTTP services, detects technologies, analyzes SSL/TLS security,
resolves DNS records, retrieves ASN information, and identifies any Web Application Firewalls (WAF).
Ideal for understanding a domain's infrastructure and security posture before deeper testing.

**Input types:** `host`

**Tags:** `recon` `dns` `ssl` `http`

**Task tree:**

- 🔧 `_group`
- 🔧 `wafw00f` — Check WAF — *if `!passive`*


---

### `host_recon` <a id="host_recon"></a>

_Host reconnaissance_

Performs comprehensive reconnaissance on a host or IP address to identify open ports and services.
Combines multiple port scanning techniques, detects service versions, searches for known vulnerabilities,
audits SSH configurations, and probes HTTP services. Optionally runs nuclei scans for network and
SSL vulnerabilities. Essential for understanding a host's security posture and attack surface.

**Input types:** `ip` `host` `cidr_range`

**Tags:** `recon` `network` `http`

**Task tree:**

- 🔧 `_group`
- 🔧 `nmap` — Detect services and versions — *if `!passive`*
- 🔧 `sshaudit` — Audit SSH port — *if `!passive`*
- 🔧 `httpx` — Probe HTTP services on open ports — *if `!passive`*
- 📂 ***nuclei*** *(parallel group)*
  - 🔧 `nuclei/network` — Scan network and SSL vulnerabilities — *if `nuclei`*
  - 🔧 `nuclei/url` — Search for vulnerabilities on alive HTTP services — *if `nuclei`*
- 📂 ***vuln*** *(parallel group)*
  - 🔧 `searchsploit` — Search for related exploits — *if `exploiters`*
  - 🔧 `search_vulns` — Search for related vulns and exploits — *if `exploiters`*


---

### `js_secrets_params_hunt` <a id="js_secrets_params_hunt"></a>

_JS secrets and params recon_

Crawls the target with multiple engines, hunts for JavaScript variables and secret patterns
using gf, scans HTTP responses with TruffleHog, discovers hidden parameters with Arjun, and
optionally scans tagged URLs with nuclei for vulnerabilities.

**Input types:** `url`

**Tags:** `http` `crawl` `secrets` `params` `vuln`

**Task tree:**

- 📂 ***crawl*** *(parallel group)*
  - 🔧 `gospider` — Crawl target with an alternative engine
  - 🔧 `katana` — Crawl target to discover endpoints
  - 🔧 `cariddi` — Hunt URL patterns and juicy endpoints
- 🔧 `httpx` — Probe discovered URLs and store responses
- 📂 ***pattern_analysis*** *(parallel group)*
  - 🔧 `gf/interestingparams` — Hunt interesting parameters and potential injection points
  - 🔧 `gf/idor` — Hunt IDOR-like parameters
- 📂 ***secrets_hunt*** *(parallel group)*
  - 🔧 `trufflehog` — Find secrets in HTTP responses — *if `hunt_secrets`*
- 📂 ***extract_params*** *(parallel group)*
  - 🔧 `arjun` — Extract parameters from GF-tagged URLs
- 🔧 `nuclei` — Scan GF/Arjun URLs for vulnerabilities — *if `nuclei`*


---

### `subdomain_recon` <a id="subdomain_recon"></a>

_Subdomain reconnaissance_

Discovers subdomains associated with a target domain using multiple passive and active techniques.
Combines passive sources, DNS queries, TLS certificate analysis, and optional brute-force methods.
Verifies discovered subdomains, checks for subdomain takeover vulnerabilities, and can optionally
test SSL/TLS security or hunt for secrets in HTTP responses. Perfect for mapping attack surface.

**Input types:** `host`

**Tags:** `recon` `dns` `http` `ssl` `secrets` `takeovers`

**Task tree:**

- 🔧 `httpx/tls` — Find subdomains through TLS certificates — *if `!passive`*
- 📂 ***hunt*** *(parallel group)*
  - 🔧 `subfinder` — List subdomains (passive) — *if `!active`*
  - 🔧 `gau` — List subdomains (passive) — *if `!active`*
  - 🔧 `dnsx/brute` — Bruteforce subdomains (DNS) — *if `brute_dns`*
  - 🔧 `ffuf/url` — Bruteforce subdomains (URL) — *if `brute_http`*
  - 🔧 `ffuf/host` — Bruteforce subdomains (Host header) — *if `brute_http`*
- 📂 ***probe*** *(parallel group)*
  - 🔧 `dnsx/probe` — Verify subdomains by probing DNS records
  - 🔧 `httpx/probe` — Run HTTP probes on subdomains — *if `!passive`*
- 📂 ***vuln*** *(parallel group)*
  - 🔧 `testssl` — Test SSL/TLS security on subdomains — *if `test_ssl`*
  - 🔧 `nuclei` — Check for subdomain takeovers — *if `!passive`*
  - 🔧 `trufflehog` — Find secrets in HTTP responses — *if `hunt_secrets`*
- 🔧 `search_vulns` — Search for related vulns and exploits


---

### `url_bypass` <a id="url_bypass"></a>

_4xx URL bypass techniques_

Attempts to bypass access restrictions on URLs that return 4xx status codes (forbidden, not found, etc.).
Uses various HTTP header manipulation and path traversal techniques to potentially gain access
to protected resources. Useful for finding misconfigured access controls and authorization bypasses.

**Input types:** `url`

**Tags:** `http` `bypass`

**Task tree:**

- 🔧 `bup` — Bypass 4xx


---

### `url_crawl` <a id="url_crawl"></a>

_URL crawl_

Rapidly crawls and discovers URLs from a target website using multiple crawling engines.
Supports both passive sources (collecting from external databases) and active crawlers
(spidering the website directly). Identifies interesting patterns, endpoints, and parameters.
Can optionally hunt for secrets in HTTP responses and probe URLs for additional information.

**Input types:** `url`

**Tags:** `http` `crawl` `secrets`

**Task tree:**

- 📂 ***crawl*** *(parallel group)*
  - 🔧 `xurlfind3r` — Crawl URLs from passive sources — *if `crawlers`*
  - 🔧 `urlfinder` — Crawl URLs from passive sources — *if `crawlers`*
  - 🔧 `gau` — Crawl URLs from passive sources — *if `crawlers`*
  - 🔧 `katana` — Crawl URLs — *if `crawlers`*
  - 🔧 `gospider` — Crawl URLs — *if `crawlers`*
  - 🔧 `cariddi` — Hunt URLs patterns — *if `crawlers`*
- 🔧 `httpx` — Run HTTP probes on unverified URLs — *if `!passive`*
- 📂 ***data_hunt*** *(parallel group)*
  - 🔧 `trufflehog` — Find secrets in HTTP responses — *if `hunt_secrets`*
  - 🔧 `maigret` — Hunt email addresses found — *if `hunt_secrets`*


---

### `url_dirsearch` <a id="url_dirsearch"></a>

_URL directory search_

Searches for hidden directories and files on web servers using content discovery techniques.
Probes URLs for directory listings, optionally bruteforces directories and crawls discovered
directory contents. Can hunt for sensitive files and secrets in HTTP responses.
Helpful for finding hidden admin panels, backup files, and exposed directories.

**Input types:** `url` `host` `host:port` `ip`

**Tags:** `http` `dir` `secrets`

**Task tree:**

- 🔧 `httpx` — Run HTTP probes on URLs
- 🔧 `ffuf` — Search for HTTP directories — *if `hunt_dirs`*
- 🔧 `katana` — Crawl files from HTTP directories — *if `hunt_files`*
- 🔧 `trufflehog` — Find secrets in HTTP responses — *if `hunt_files`*


---

### `url_fuzz` <a id="url_fuzz"></a>

_URL fuzz (slow)_

Performs comprehensive fuzzing of URLs to discover hidden content and directories.
Uses multiple fuzzing engines (dirsearch, feroxbuster, ffuf) with intelligent calibration
to filter false positives. Probes discovered URLs, captures screenshots when configured,
and optionally hunts for secrets in HTTP responses. Thorough but time-intensive.

**Input types:** `url`

**Tags:** `http` `fuzz` `secrets`

**Task tree:**

- 📂 ***fuzz*** *(parallel group)*
  - 🔧 `feroxbuster` — Fuzz URLs — *if `fuzzers`*
  - 🔧 `ffuf` — Fuzz URLs — *if `fuzzers`*
- 🔧 `httpx` — Run HTTP probes on fuzzed URLs
- 🔧 `trufflehog` — Find secrets in HTTP responses — *if `hunt_secrets`*


---

### `url_params_fuzz` <a id="url_params_fuzz"></a>

_URL parameter fuzzing_

Identifies and tests URL parameters for vulnerabilities through intelligent fuzzing.
Extracts parameters from URLs using multiple techniques, then fuzzes them with various payloads
to discover potential security issues. Probes fuzzed URLs to verify results and optionally
hunts for secrets in responses. Effective for finding hidden parameters and testing input validation.

**Input types:** `url`

**Tags:** `http` `fuzz` `secrets`

**Task tree:**

- 🔧 `httpx` — Probe URLs and eliminate unresponsive ones — *if `probe`*
- 🔧 `urlparser` — Extract base URLs
- 📂 ***extract_params*** *(parallel group)*
  - 🔧 `arjun` — Extract parameters from URLs — *if `fuzzers`*
  - 🔧 `x8` — Bruteforce URL params — *if `fuzzers`*
- 🔧 `ffuf` — Fuzz URL params — *if `fuzz_values`*
- 🔧 `trufflehog` — Find secrets in HTTP responses — *if `hunt_secrets`*


---

### `url_secrets_hunt` <a id="url_secrets_hunt"></a>

_URL secrets hunt_

Searches for exposed secrets, credentials, and sensitive information in web content.
Probes URLs and analyzes HTTP responses for API keys, passwords, tokens, private keys,
and other confidential data. Uses TruffleHog to detect various secret patterns.
Critical for identifying accidental credential exposure and sensitive data leaks.

**Input types:** `url`

**Tags:** `http` `fuzz` `secrets`

**Task tree:**

- 🔧 `httpx` — Run HTTP probes on URLs
- 🔧 `trufflehog` — Find secrets in HTTP responses


---

### `url_vuln` <a id="url_vuln"></a>

_URL vulnerability scan (gf, dalfox)_

Scans URLs for common web vulnerabilities using pattern matching and automated testing tools.
Identifies potential XSS, LFI, SSRF, RCE, IDOR, and other vulnerability indicators in URL parameters.
Tests discovered vulnerable patterns with specialized tools like Dalfox for XSS exploitation.
Optionally runs comprehensive nuclei scans for additional HTTP vulnerability detection.

**Input types:** `url`

**Tags:** `http` `vuln`

**Task tree:**

- 📂 ***pattern_analysis*** *(parallel group)*
  - 🔧 `gf/xss` — Hunt XSS params
  - 🔧 `gf/lfi` — Hunt LFI params
  - 🔧 `gf/ssrf` — Hunt SSRF params
  - 🔧 `gf/rce` — Hunt RCE params
  - 🔧 `gf/interestingparams` — Hunt interest params
  - 🔧 `gf/idor` — Hunt Idor params
  - 🔧 `gf/debug_logic` — Hunt debug params
- 📂 ***vuln_scan*** *(parallel group)*
  - 🔧 `dalfox` — Attack XSS vulnerabilities — *if `!passive`*
  - 🔧 `nuclei` — Search for HTTP vulns — *if `nuclei`*


---

### `user_hunt` <a id="user_hunt"></a>

_User account search_

Searches for user accounts and associated information across various online platforms and services.
Takes usernames, email addresses, or other identifiers and queries multiple sources to find
associated accounts, password leaks, and online profiles. Useful for OSINT investigations,
credential stuffing prevention checks, and understanding a user's digital footprint.

**Input types:** `slug` `string` `email`

**Tags:** `user_account` `leak`

**Task tree:**

- 📂 ***hunt_users*** *(parallel group)*
  - 🔧 `maigret` — Hunt user accounts
  - 🔧 `h8mail` — Find password leaks


---

### `wordpress` <a id="wordpress"></a>

_Wordpress vulnerability scan_

Specialized security assessment for WordPress websites and installations.
Identifies WordPress version, installed themes and plugins, known vulnerabilities,
misconfigurations, and weak configurations. Uses multiple WordPress-specific tools
to provide comprehensive coverage. Critical for WordPress site security audits.

**Input types:** `url` `ip` `host` `host:port`

**Tags:** `http` `wordpress` `vuln`

**Task tree:**

- 🔧 `httpx` — URL probe
- 📂 ***hunt_wordpress*** *(parallel group)*
  - 🔧 `wpscan` — WPScan
  - 🔧 `wpprobe` — WPProbe
  - 🔧 `nuclei` — Nuclei Wordpress scan

