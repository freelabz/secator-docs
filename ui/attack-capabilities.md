# Attack capabilities

The platform's offensive and defensive capabilities are organised here by **intrusion layer** — from zero-touch passive intelligence (Layer 1) to live exploitation (Layer 5). This is the same way a serious engagement scope is written: *"OK for layers 1-3, written authorization required beyond"*.

When you discuss scope with a client, refer to a layer rather than naming individual tools — every layer maps to a curated set of profiles, workflows and tasks below.

> [!note]
> Higher layers always include the capabilities of the layers beneath them when they need to (e.g. a Layer 4 vuln scan first runs Layer 2 probes to discover the surface). The layer boundaries are about **what new traffic the platform sends to the target**, not about which tools "could" run.

### Layer 1 — Passive intelligence

Zero requests sent to the target. All data comes from third-party datasets (Wayback, Common Crawl, certificate transparency, breach corpora, public source code, social platforms).

Safe to run during scoping, on out-of-scope assets, or when stealth is mandatory. Use the `passive` profile to lock the platform into this layer.

| Capability | Tools |
|---|---|
| Subdomain enumeration | `subfinder`, `xurlfind3r` |
| URL harvesting | `gau`, `xurlfind3r`, `urlfinder` |
| WHOIS / domain info | `jswhois`, `whois` |
| ASN / IP intelligence | `getasn` |
| Known-CVE lookup | `searchsploit`, `search_vulns` |
| Email breach lookup | `h8mail` |
| Username correlation | `maigret` |
| Public secret hunting | `gitleaks` (on public git repos) |

### Layer 2 — Active probing

Sends TCP / HTTP / DNS / ICMP probes to the target but **no offensive payload**. Just enough traffic to map the surface and fingerprint services.

Equivalent to standard pre-engagement recon. Most clients accept this as soon as the IP / domain is in scope.

| Capability | Tools |
|---|---|
| DNS resolution | `dnsx` |
| Port scanning | `nmap`, `naabu` |
| HTTP probing | `httpx` |
| Network discovery (LAN) | `arpscan`, `arp`, `fping`, `mapcidr`, `netdetect` |
| TLS posture | `testssl` |
| SSH hardening | `sshaudit` |
| WAF fingerprinting | `wafw00f` |

### Layer 3 — Crawling & content discovery

Walks the application like a user or a search-engine spider, plus directory / parameter brute-force on the discovered surface. Consumes target bandwidth but does not yet send injection payloads.

Use when the scope is *web app testing* without explicit authorization for vuln scanning.

| Capability | Tools |
|---|---|
| Active crawling | `katana`, `gospider`, `cariddi` |
| Directory / file brute-force | `feroxbuster`, `dirsearch`, `ffuf` |
| HTTP parameter discovery | `arjun`, `x8` |
| In-response secret hunting | `trufflehog` |
| Pattern matching for vuln candidates | `gf` (SQLi / SSRF / LFI / RCE / IDOR / debug paths) |

### Layer 4 — Vulnerability scanning

Sends template- or signature-based payloads to verify whether known issues exist. Findings carry CVE / CVSS / severity data and may include reproducible request/response evidence (records).

Requires written authorization. Choose `aggressive` for speed, `polite` for production targets.

| Capability | Tools |
|---|---|
| Generic vulnerability scanner | `nuclei` (10 000+ templates: CVEs, misconfigs, exposed panels) |
| Multipurpose recon-to-vuln pipeline | `bbot` |
| Container / filesystem CVE scanning | `trivy`, `grype` |
| WordPress audit | `wpscan`, `wpprobe` |
| Reflected / stored / DOM XSS | `dalfox` |
| Subdomain-takeover detection | `subdomain_recon` workflow (chains `subfinder → dnsx → httpx → nuclei` takeover templates) |

### Layer 5 — Exploitation

Live exploit attempts against confirmed vulnerabilities. **Do not run** unless you have explicit authorization in writing and a controlled rollback plan.

| Capability | Tools |
|---|---|
| 40x bypass attempts | `bup` (30+ techniques: header injection, path tricks, method override) |
| Known-CVE exploitation modules | `msfconsole` (Metasploit) |

> [!caution]
> Layer 5 produces real changes on the target — application state, audit logs, sometimes data. Always run inside a lab/staging environment before pointing at production. Verify the workspace's [scope](glossary.md#g-scope) before launching.

The full content of each scan and each workflow follows directly below.



---

See the full content of every scan and workflow in:

- [Available scans](available-scans.md)
- [Available workflows](available-workflows.md)

