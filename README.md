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

| Name                                                          | Description                                                                            | Category       |
| ------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------- |
| [httpx](https://github.com/projectdiscovery/httpx)            | Fast HTTP prober.                                                                      | `http`         |
| [wafw00f](https://github.com/EnableSecurity/wafw00f)          | Identify and fingerprint Web Application Firewalls (WAF) protecting a website.         | `http`         |
| [cariddi](https://github.com/edoardottt/cariddi)              | Fast crawler and endpoint secrets / api keys / tokens matcher.                         | `http/crawler` |
| [gau](https://github.com/lc/gau)                              | Offline URL crawler (Alien Vault, The Wayback Machine, Common Crawl, URLScan).         | `http/crawler` |
| [gospider](https://github.com/jaeles-project/gospider)        | Fast web spider written in Go.                                                         | `http/crawler` |
| [katana](https://github.com/projectdiscovery/katana)          | Next-generation crawling and spidering framework.                                      | `http/crawler` |
| [urlfinder](https://github.com/projectdiscovery/urlfinder)    | Passive URL discovery from online sources.                                             | `http/crawler` |
| [xurlfind3r](https://github.com/hueristiq/xurlfind3r)         | Passive URL discovery from multiple online sources.                                    | `http/crawler` |
| [arjun](https://github.com/s0md3v/Arjun)                      | HTTP parameter discovery suite.                                                        | `http/fuzzer`  |
| [bup](https://github.com/laluka/bypass-url-parser)            | Test many `40X` bypasses for a given URL (bypass-url-parser).                          | `http/fuzzer`  |
| [dirsearch](https://github.com/maurosoria/dirsearch)          | Web path discovery.                                                                    | `http/fuzzer`  |
| [feroxbuster](https://github.com/epi052/feroxbuster)          | Simple, fast, recursive content discovery tool written in Rust.                        | `http/fuzzer`  |
| [ffuf](https://github.com/ffuf/ffuf)                          | Fast web fuzzer written in Go.                                                         | `http/fuzzer`  |
| [x8](https://github.com/Sh1Yo/x8)                             | Hidden HTTP parameter discovery tool.                                                  | `http/fuzzer`  |
| [bbot](https://github.com/blacklanternsecurity/bbot)          | Recursive OSINT scanner and recon multitool.                                           | `osint`        |
| [h8mail](https://github.com/khast3x/h8mail)                   | Email OSINT and breach hunting tool.                                                   | `osint`        |
| [dnsx](https://github.com/projectdiscovery/dnsx)              | Fast and multi-purpose DNS toolkit (queries and bruteforce mode).                      | `recon/dns`    |
| [jswhois](https://github.com/freelabz/jswhois)                | Fast WHOIS lookup tool.                                                                | `recon/dns`    |
| [subfinder](https://github.com/projectdiscovery/subfinder)    | Fast subdomain finder.                                                                 | `recon/dns`    |
| [whois](https://github.com/likexian/whois)                    | WHOIS information lookup.                                                               | `recon/dns`    |
| [whoisdomain](https://github.com/mboot-github/WhoisDomain)    | Domain WHOIS parsing and lookup.                                                       | `recon/dns`    |
| [arpscan](https://github.com/royhills/arp-scan)               | Scan a CIDR range for alive hosts using ARP (arp-scan).                                | `recon/ip`     |
| [fping](https://fping.org/)                                   | Find alive hosts on local networks.                                                    | `recon/ip`     |
| [getasn](https://github.com/freelabz/getasn)                  | Get ASN information from an IP address.                                                | `recon/ip`     |
| [mapcidr](https://github.com/projectdiscovery/mapcidr)        | Expand CIDR ranges into IPs.                                                           | `recon/ip`     |
| [naabu](https://github.com/projectdiscovery/naabu)            | Fast port discovery tool.                                                              | `recon/port`   |
| [maigret](https://github.com/soxoj/maigret)                   | Hunt for user accounts across many websites.                                           | `recon/user`   |
| [gf](https://github.com/tomnomnom/gf)                         | A wrapper around grep to avoid typing common patterns.                                 | `tagger`       |
| [ph](https://github.com/freelabz/ph)                          | Pattern hunter / tagger for URLs and strings.                                          | `tagger`       |
| [gitleaks](https://github.com/gitleaks/gitleaks)              | Detect secrets and API keys in code and git repositories.                             | `vuln/code`    |
| [grype](https://github.com/anchore/grype)                     | A vulnerability scanner for container images and filesystems.                          | `vuln/code`    |
| [trivy](https://github.com/aquasecurity/trivy)                | Vulnerability and misconfiguration scanner for containers and filesystems.             | `vuln/code`    |
| [trufflehog](https://github.com/trufflesecurity/trufflehog)   | Find and verify leaked secrets and credentials.                                        | `vuln/code`    |
| [dalfox](https://github.com/hahwul/dalfox)                    | Powerful XSS scanning tool and parameter analyzer.                                     | `vuln/http`    |
| [msfconsole](https://docs.rapid7.com/metasploit/msf-overview) | CLI to access and work with the Metasploit Framework.                                  | `vuln/http`    |
| [nmap](https://github.com/nmap/nmap)                          | Vulnerability scanner using NSE scripts.                                               | `vuln/multi`   |
| [nuclei](https://github.com/projectdiscovery/nuclei)          | Fast and customisable vulnerability scanner based on simple YAML based DSL.            | `vuln/multi`   |
| [search_vulns](https://github.com/ra1nb0rn/search_vulns)      | Search for known vulnerabilities and exploits for a given product / CPE.               | `vuln/multi`   |
| [searchsploit](https://gitlab.com/exploit-database/exploitdb) | Search Exploit-DB for exploits and shellcodes.                                         | `vuln/multi`   |
| [sshaudit](https://github.com/jtesta/ssh-audit)               | SSH server / client configuration and known-vulnerability auditing.                    | `vuln/multi`   |
| [testssl](https://github.com/drwetter/testssl.sh)             | Test TLS/SSL configuration and known vulnerabilities.                                  | `vuln/multi`   |
| [wpprobe](https://github.com/Chocapikk/wpprobe)               | Fast WordPress plugin enumeration and vulnerability scanner.                           | `vuln/multi`   |
| [wpscan](https://github.com/wpscanteam/wpscan)                | WordPress Security Scanner.                                                            | `vuln/multi`   |

`secator` also ships a few **built-in tasks** written in Python that don't wrap an external tool:

| Name         | Description                                                            | Category    |
| ------------ | --------------------------------------------------------------------- | ----------- |
| `ai`         | AI-powered pentest assistant (attack or chat mode).                   | `ai`        |
| `arp`        | Display the system ARP cache.                                         | `recon/ip`  |
| `netdetect`  | Detect local network CIDR ranges.                                     | `recon/ip`  |
| `prompt`     | Prompt the user (interactive workflow step).                          | `util`      |
| `urlparser`  | Extract query-string parameters from URLs.                            | `http`      |

{% hint style="info" %}
Run **`secator x`** to list all available tasks on your installation.
{% endhint %}

{% hint style="info" %}
Feel free to request new tools integrations by [opening an issue](https://github.com/freelabz/secator/issues/new) on the repo, but please check that the tool complies with our selection criterias before doing so (read [#curated-list-of-tools](in-depth/philosophy-and-design.md#curated-list-of-tools "mention")). If it doesn't but you still want to integrate it into `secator`, you can plug it in (read [writing-tasks](for-developers/writing-tasks/ "mention")).
{% endhint %}

***
