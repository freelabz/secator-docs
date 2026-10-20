---
description: ... or what secator is all about.
---

# Introduction

`secator` is a task and workflow runner used for security assessments. It supports dozens of well-known security tools and is designed to improve productivity for pentesters and security researchers.

***

## Quick demo

<figure><img src=".gitbook/assets/demo.gif" alt=""><figcaption><p>Example of running secator tasks and workflows</p></figcaption></figure>

***

## Features

* [#curated-list-of-tools](in-depth/philosophy-and-design.md#curated-list-of-tools "mention")
* [#unified-input-options](in-depth/philosophy-and-design.md#unified-input-options "mention")
* [#unified-output-schema](in-depth/philosophy-and-design.md#unified-output-schema "mention")
* [#cli-and-library-usage](in-depth/philosophy-and-design.md#cli-and-library-usage "mention")
* [#distributed-options](in-depth/philosophy-and-design.md#distributed-options "mention")
* [#from-simple-tasks-to-complex-workflows](in-depth/philosophy-and-design.md#from-simple-tasks-to-complex-workflows "mention")
* [#customizable](in-depth/philosophy-and-design.md#customizable "mention")

***

## Supported tools

`secator` integrates the following tools:

| Name | Description | Category |
| ---- | ----------- | -------- |
| [`ai`](in-depth/ai-task.md) | AI-powered penetration testing assistant (scan, chat or exploit mode). | `ai/analysis/pentest` |
| [arjun](https://github.com/s0md3v/Arjun) | HTTP Parameter Discovery Suite. | `url/fuzz/params` |
| `arp` | Display the system ARP cache. | `ip/recon` |
| [arpscan](https://github.com/royhills/arp-scan) | Scan a CIDR range for alive hosts using ARP. | `ip/recon` |
| [bbot](https://github.com/blacklanternsecurity/bbot) | Multipurpose scanner. | `vuln/scan` |
| [bup](https://github.com/laluka/bypass-url-parser) | 40X bypasser. | `url/bypass` |
| [cariddi](https://github.com/edoardottt/cariddi) | Crawl endpoints, secrets, api keys, extensions, tokens... | `url/crawl` |
| `command` | Run an arbitrary shell command verbatim. | `misc` |
| [dalfox](https://github.com/hahwul/dalfox) | Powerful open source XSS scanning tool. | `url/fuzz` |
| [dnsx](https://github.com/projectdiscovery/dnsx) | dnsx is a fast and multi-purpose DNS toolkit designed for running various retryabledns library. | `dns/fuzz` |
| [feroxbuster](https://github.com/epi052/feroxbuster) | Simple, fast, recursive content discovery tool written in Rust | `url/fuzz` |
| [ffuf](https://github.com/ffuf/ffuf) | Fast web fuzzer written in Go. | `url/fuzz` |
| [fping](https://github.com/schweikert/fping) | Send ICMP echo probes to network hosts, similar to ping, but much better. | `ip/recon` |
| [gau](https://github.com/lc/gau) | Fetch known URLs from AlienVault's Open Threat Exchange, the Wayback Machine, Common Crawl, and URLScan. | `url/crawl/passive` |
| [getasn](https://github.com/freelabz/getasn) | Get ASN information from IP address. | `ip/probe` |
| [gf](https://github.com/tomnomnom/gf) | Wrapper around grep, to help you grep for things. | `pattern/scan` |
| [gitleaks](https://github.com/gitleaks/gitleaks) | Tool for detecting secrets like passwords, API keys, and tokens in git repos, files, and stdin. | `secret/scan` |
| [gospider](https://github.com/jaeles-project/gospider) | Fast web spider written in Go. | `url/crawl` |
| [grype](https://github.com/anchore/grype) | Vulnerability scanner for container images and filesystems. | `vuln/scan` |
| [h8mail](https://github.com/khast3x/h8mail) | Email information and password lookup tool. | `user/recon/email` |
| [httpx](https://github.com/projectdiscovery/httpx) | Fast and multi-purpose HTTP toolkit. | `url/probe` |
| [jswhois](https://github.com/freelabz/jswhois) | WHOIS in JSON format | `domain/info` |
| [katana](https://github.com/projectdiscovery/katana) | Next-generation crawling and spidering framework. | `url/crawl` |
| [maigret](https://github.com/soxoj/maigret) | Collect a dossier on a person by username. | `user/recon/username` |
| [mapcidr](https://github.com/projectdiscovery/mapcidr) | Utility program to perform multiple operations for a given subnet/cidr ranges. | `ip/recon` |
| [msfconsole](https://docs.rapid7.com/metasploit/msf-overview/) | CLI to access and work with the Metasploit Framework. | `exploit/attack` |
| [naabu](https://github.com/projectdiscovery/naabu) | Port scanning tool written in Go. | `port/scan` |
| `netdetect` | Detect local network CIDR ranges. | `network/recon` |
| [nmap](https://github.com/nmap/nmap) | Network Mapper is a free and open source utility for network discovery and security auditing. | `port/scan` |
| [nuclei](https://github.com/projectdiscovery/nuclei) | Fast and customisable vulnerability scanner based on simple YAML based DSL. | `vuln/scan` |
| [ph](https://github.com/freelabz/ph) | Pattern matcher that tags interesting patterns found in URLs or text. | `pattern/scan` |
| `prompt` | Prompt the user. | `network/recon` |
| [search_vulns](https://github.com/ra1nb0rn/search_vulns) | Search for known vulnerabilities in software by product name or CPE. | `vuln/recon` |
| [searchsploit](https://gitlab.com/exploit-database/exploitdb) | Exploit searcher based on ExploitDB. | `exploit/recon` |
| [sshaudit](https://github.com/jtesta/ssh-audit) | SSH server & client security auditing (banner, key exchange, encryption, mac, compression, etc). | `ssh/audit/security` |
| [subfinder](https://github.com/projectdiscovery/subfinder) | Fast passive subdomain enumeration tool. | `dns/recon/passive` |
| [testssl](https://github.com/testssl/testssl.sh) | SSL/TLS security scanner, including ciphers, protocols and cryptographic flaws. | `dns/recon/tls` |
| [trivy](https://github.com/aquasecurity/trivy) | Comprehensive and versatile security scanner. | `vuln/scan` |
| [trufflehog](https://github.com/trufflesecurity/trufflehog) | Tool for finding secrets in git repositories and filesystems using TruffleHog. | `secret/scan` |
| [urlfinder](https://github.com/projectdiscovery/urlfinder) | Find URLs in text. | `url/crawl/passive` |
| `urlparser` | Extract query string parameters from URLs | `url/params` |
| [wafw00f](https://github.com/EnableSecurity/wafw00f) | Web Application Firewall Fingerprinting tool. | `waf/scan` |
| [whois](https://github.com/likexian/whois) | The whois tool from likexian retrieves domain registration information in JSON format. | `misc` |
| [whoisdomain](https://github.com/mboot-github/WhoisDomain) | The whois tool retrieves registration information about domain names and IP addresses. | `misc` |
| [wpprobe](https://github.com/Chocapikk/wpprobe) | Fast wordpress plugin enumeration tool. | `vuln/scan/wordpress` |
| [wpscan](https://github.com/wpscanteam/wpscan) | Wordpress security scanner. | `vuln/scan/wordpress` |
| [x8](https://github.com/freelabz/x8) | Hidden parameters discovery suite written in Rust. | `url/fuzz/params` |
| [xurlfind3r](https://github.com/hueristiq/xurlfind3r) | Discover URLs for a given domain in a simple, passive and efficient way | `url/crawl/passive` |

{% hint style="info" %}
`ai`, `arp`, `command`, `netdetect`, `prompt` and `urlparser` are built-in tasks that do not wrap an external tool.
{% endhint %}

{% hint style="info" %}
Feel free to request new tools integrations by [opening an issue](https://github.com/freelabz/secator/issues/new) on the repo, but please check that the tool complies with our selection criterias before doing so (read [#curated-list-of-tools](in-depth/philosophy-and-design.md#curated-list-of-tools "mention")). If it doesn't but you still want to integrate it into `secator`, you can plug it in (read [writing-tasks](for-developers/writing-tasks/ "mention")).
{% endhint %}

***
