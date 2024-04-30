---
description: ... or what secator is all about.
---

# Introduction

`secator` is a task and workflow runner used for security assessments. It supports dozens of well-known security tools and is designed to improve productivity for pentesters and security researchers.

## Quick demo

<figure><img src=".gitbook/assets/demo.gif" alt=""><figcaption><p>Example of running secator tasks and workflows</p></figcaption></figure>

## Features

* [#curated-list-of-tools](in-depth/philosophy-and-design.md#curated-list-of-tools "mention")
* [#unified-input-options](in-depth/philosophy-and-design.md#unified-input-options "mention")
* [#unified-output-schema](in-depth/philosophy-and-design.md#unified-output-schema "mention")
* [#cli-and-library-usage](in-depth/philosophy-and-design.md#cli-and-library-usage "mention")
* [#distributed-options](in-depth/philosophy-and-design.md#distributed-options "mention")
* [#from-simple-tasks-to-complex-workflows](in-depth/philosophy-and-design.md#from-simple-tasks-to-complex-workflows "mention")
* [#customizable](in-depth/philosophy-and-design.md#customizable "mention")

## Supported tools

`secator` integrates the following tools:

| Name                                                          | Description                                                                            | Category       |
| ------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------- |
| [httpx](https://github.com/projectdiscovery/httpx)            | Fast HTTP prober.                                                                      | `http`         |
| [cariddi](https://github.com/edoardottt/cariddi)              | Fast crawler and endpoint secrets / api keys / tokens matcher.                         | `http/crawler` |
| [gau](https://github.com/lc/gau)                              | Offline URL crawler (Alien Vault, The Wayback Machine, Common Crawl, URLScan).         | `http/crawler` |
| [gospider](https://github.com/jaeles-project/gospider)        | Fast web spider written in Go.                                                         | `http/crawler` |
| [katana](https://github.com/projectdiscovery/katana)          | Next-generation crawling and spidering framework.                                      | `http/crawler` |
| [dirsearch](https://github.com/maurosoria/dirsearch)          | Web path discovery.                                                                    | `http/fuzzer`  |
| [feroxbuster](https://github.com/epi052/feroxbuster)          | Simple, fast, recursive content discovery tool written in Rust.                        | `http/fuzzer`  |
| [ffuf](https://github.com/ffuf/ffuf)                          | Fast web fuzzer written in Go.                                                         | `http/fuzzer`  |
| [h8mail](https://github.com/khast3x/h8mail)                   | Email OSINT and breach hunting tool.                                                   | `osint`        |
| [dnsx](https://github.com/projectdiscovery/dnsx)              | Fast and multi-purpose DNS toolkit designed for running DNS queries.                   | `recon/dns`    |
| [dnsxbrute](https://github.com/projectdiscovery/dnsx)         | Fast and multi-purpose DNS toolkit designed for running DNS queries (bruteforce mode). | `recon/dns`    |
| [subfinder](https://github.com/projectdiscovery/subfinder)    | Fast subdomain finder.                                                                 | `recon/dns`    |
| [fping](https://fping.org/)                                   | Find alive hosts on local networks.                                                    | `recon/ip`     |
| [mapcidr](https://github.com/projectdiscovery/mapcidr)        | Expand CIDR ranges into IPs.                                                           | `recon/ip`     |
| [naabu](https://github.com/projectdiscovery/naabu)            | Fast port discovery tool.                                                              | `recon/port`   |
| [maigret](https://github.com/soxoj/maigret)                   | Hunt for user accounts across many websites.                                           | `recon/user`   |
| [gf](https://github.com/tomnomnom/gf)                         | A wrapper around grep to avoid typing common patterns.                                 | `tagger`       |
| [grype](https://github.com/anchore/grype)                     | A vulnerability scanner for container images and filesystems.                          | `vuln/code`    |
| [dalfox](https://github.com/hahwul/dalfox)                    | Powerful XSS scanning tool and parameter analyzer.                                     | `vuln/http`    |
| [msfconsole](https://docs.rapid7.com/metasploit/msf-overview) | CLI to access and work with the Metasploit Framework.                                  | `vuln/http`    |
| [wpscan](https://github.com/wpscanteam/wpscan)                | WordPress Security Scanner                                                             | `vuln/multi`   |
| [nmap](https://github.com/nmap/nmap)                          | Vulnerability scanner using NSE scripts.                                               | `vuln/multi`   |
| [nuclei](https://github.com/projectdiscovery/nuclei)          | Fast and customisable vulnerability scanner based on simple YAML based DSL.            | `vuln/multi`   |

{% hint style="info" %}
Feel free to request new tools integrations by opening an issue on the repo, but please check that the tool complies with our selection criterias before doing so (read [#curated-list-of-tools](in-depth/philosophy-and-design.md#curated-list-of-tools "mention")). If it doesn't but you still want to integrate it into `secator`, you can plug it in (read [writing-tasks](for-developers/writing-tasks/ "mention")).
{% endhint %}
