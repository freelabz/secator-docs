---
description: ... or how to manage different runner option sets effectively.
---

# Profiles

`secator` profiles are a way to mutualize sets of options to be quickly re-used in tasks, workflows, and scans. Profiles allow you to apply predefined option configurations with a single flag, making it easy to switch between different scanning strategies.

***

## Using profiles

You can use profiles with any task, workflow, or scan by using the `-pf` or `--profiles` flag:

{% tabs %}
{% tab title="Task" %}
```bash
secator x httpx example.com -pf aggressive,full
```
{% endtab %}

{% tab title="Workflow" %}
```bash
secator w host_recon example.com -pf aggressive,full
```
{% endtab %}

{% tab title="Scan" %}
```bash
secator s host example.com -pf aggressive,full
```
{% endtab %}
{% endtabs %}

You can combine multiple profiles by separating them with commas. Options from profiles are merged, with later profiles taking precedence over earlier ones.

***

## Listing available profiles

To see all available profiles and their options:

```bash
secator p list
```

***

## Built-in profiles

`secator` comes with several built-in profiles organized by category:

### Speed profiles

These profiles control the aggressiveness and speed of scans by adjusting rate limits, delays, timeouts, and retries.

#### Aggressive (`aggressive`)

Optimized for internal networks or time-sensitive scans with no rate limiting.

```yaml
rate_limit: 10000
delay: 0
timeout: 1
retries: 1
```

**Use case**: Fast scanning on trusted internal networks where you need results quickly.

#### Insane (`insane`)

Maximum speed for local LAN scanning or stress testing.

```yaml
rate_limit: 100000
delay: 0
timeout: 1
retries: 0
```

**Use case**: Local network scanning or stress testing where network impact is not a concern.

#### Paranoid (`paranoid`)

Maximum stealth with very conservative settings.

```yaml
rate_limit: 5
delay: 5
timeout: 15
retries: 5
```

**Use case**: Scanning sensitive networks where stealth is critical and you can afford to wait.

#### Polite (`polite`)

Balanced settings to avoid overloading the network.

```yaml
rate_limit: 100
delay: 0
timeout: 10
retries: 5
```

**Use case**: General-purpose scanning where you want to be respectful of network resources.

***

### Evasion profiles

These profiles help evade detection systems and maintain anonymity.

#### Sneaky (`sneaky`)

IDS/IPS evasion for sensitive networks using packet fragmentation.

```yaml
fragment: true
nmap_light_fragment: true
```

**Use case**: Scanning networks with active IDS/IPS systems that you want to evade.

#### Stealth (`stealth`)

Stealth scan using TCP SYN scanning.

```yaml
tcp_syn_stealth: true
nmap_light_tcp_syn_stealth: true
scan_type: s
```

**Use case**: Port scanning where you want to minimize detection by using stealth techniques.

#### Tor (`tor`)

Anonymous scanning using the Tor network.

```yaml
proxy: auto
```

**Use case**: Scanning where you need anonymity and want to route traffic through Tor.

{% hint style="info" %}
Make sure you have Tor configured and running, and set up your proxy settings in the config (see [proxies.md](proxies.md "mention")).
{% endhint %}

***

### General profiles

These profiles control the overall scanning approach and feature activation.

#### Active (`active`)

Active scanning only - no passive sources are used. This profile enforces active-only mode.

```yaml
active: true
domain_recon_active: true
subdomain_recon_active: true
host_recon_active: true
url_crawl_active: true
url_vuln_active: true
```

**Use case**: When you want to ensure all scanning is done actively (making requests to targets) and avoid passive data sources.

#### Passive (`passive`)

Passive scanning only - no requests are made to targets. This profile enforces passive-only mode.

```yaml
passive: true
domain_recon_passive: true
subdomain_recon_passive: true
host_recon_passive: true
url_crawl_passive: true
url_vuln_passive: true
```

**Use case**: When you want to gather information without making any requests to the target (e.g., using only OSINT sources).

#### Full (`full`)

Activates all optional features for comprehensive scanning.

```yaml
# Task options
headless: true
system_chrome: true
no_sandbox: true
screenshot: true
juicy_extensions: 3
server_defaults: false

# Workflow options
ports: "-"
nuclei: true
brute_dns: true
brute_http: true
hunt_secrets: true
test_ssl: true

# Scan options
host_recon_nuclei: true
host_recon_nmap_ports: "-"
domain_recon_testssl_server_defaults: null
subdomain_recon_hunt_secrets: true
subdomain_recon_test_ssl: true
subdomain_recon_testssl_server_defaults: null
url_crawl_hunt_secrets: true
url_vuln_nuclei: true
url_crawl_cariddi_juicy_extensions: 3
```

**Use case**: Comprehensive security assessments where you want to enable all available features including headless browsing, screenshots, vulnerability scanning, secret hunting, and SSL testing.

***

### Network profiles

These profiles configure network-specific scanning options.

#### All Ports (`all_ports`)

Scans all ports instead of just common ones.

```yaml
ports: "-"
host_recon_nmap_ports: "-"
```

**Use case**: When you need a complete port scan of all 65535 ports (warning: this can be very slow).

#### HTTP Headless (`http_headless`)

Enables headless browser mode for HTTP tasks.

```yaml
headless: true
system_chrome: true
no_sandbox: true
```

**Use case**: When you need to render JavaScript or interact with modern web applications that require a browser.

#### HTTP Record (`http_record`)

Records HTTP requests/responses and takes screenshots.

```yaml
screenshot: true
store_responses: true
system_chrome: true
no_sandbox: true
```

**Use case**: When you need to capture full HTTP interactions and visual evidence of web pages.

***

## Profile enforcement

Some profiles have the `enforce: true` setting, which means they override any conflicting options you might pass directly. Profiles with enforcement are:

- `active`
- `passive`
- `full`
- `all_ports`

When using enforced profiles, the profile options take precedence over command-line options.

***

## Combining profiles

You can combine multiple profiles to create a custom configuration:

```bash
# Combine speed and evasion profiles
secator w host_recon example.com -pf aggressive,stealth

# Combine feature activation with speed
secator s host example.com -pf full,polite

# Combine network and evasion
secator x naabu example.com -pf all_ports,tor
```

When combining profiles, options are merged with later profiles taking precedence over earlier ones.

***

## Setting default profiles

You can set default profiles in your configuration that will be applied automatically:

```bash
secator config set profiles.defaults aggressive,polite
```

Default profiles are automatically applied to all runs unless you explicitly override them with the `-pf` flag.

***

## Creating custom profiles

To create your own profile, create a YAML file in `~/.secator/templates/profiles/`:

```yaml
type: profile
name: my_custom_profile
category: general
description: "My custom profile description"
opts:
    rate_limit: 500
    delay: 0.5
    timeout: 5
    retries: 3
```

After creating the profile file, it will be automatically available for use with the `-pf` flag.

***
