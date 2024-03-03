# CLI Usage

`secator` is first and foremost a command-line interface (CLI). This page describes how to use it in-depth.

***

## Usage

```bash
secator --help

secator x --help      # Tasks
secator w --help      # Workflows
secator s --help      # Scans
secator u --help      # Utils
secator worker --help # Worker
secator test --help   # Tests
```

***

## Worker \[optional]

You can enable enable distributed runs by starting a `secator worker`.  All tasks / workflows / scans will be sent to the worker for execution.

{% hint style="info" %}
Learn more about [distributed-runs-with-celery.md](in-depth/distributed-runs-with-celery.md "mention").
{% endhint %}

***

## Tasks

You can run any of the supported tasks out-of-the box using the `secator x` (execute) subcommand:

{% tabs %}
{% tab title="subfinder" %}
Find subdomains of a domain using offline sources with `subfinder`:

```bash
secator x subfinder wikipedia.org
```
{% endtab %}

{% tab title="httpx" %}
Find information about an URL with `httpx`:

```bash
secator x httpx wikipedia.org
```
{% endtab %}

{% tab title="ffuf" %}
Fuzz URLs with `ffuf` with max 100 requests / second and matching select HTTP codes:

```bash
secator x ffuf http://testphp.vulnweb.com/FUZZ -rl 100 -mc 200,201,300,500
```
{% endtab %}

{% tab title="nmap" %}
Find open ports and associated vulnerabilities with `nmap` using proxychains as a proxy:

```bash
secator x nmap myhost.com -p 443,80,8080,8081,21 -proxy proxychains
```
{% endtab %}

{% tab title="maigret" %}
Find user accounts with `maigret`:

```bash
secator x maigret elonmusk
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
Use **`secator x --help`** to list all available tasks.

Use **`secator x <NAME> --help`** to list task options.
{% endhint %}

***

## Workflows

A workflow is a set of pre-defined tasks.

You can run some pre-written workflows using the `secator w` (workflow) subcommand:

{% tabs %}
{% tab title="Host recon" %}
To perform a basic host recon (open ports, network + HTTP vulnerabilities):

```bash
secator w host_recon 192.168.1.18
```
{% endtab %}

{% tab title="Subdomain recon" %}
To perform a basic subdomain discovery (subdomain + root URLs):

```bash
secator w subdomain_recon mydomain.com
```
{% endtab %}

{% tab title="URL crawl" %}
To perform URL crawling:

```bash
secator w url_crawl https://mydomain.com/start/crawling/from/here/
```
{% endtab %}

{% tab title="URL fuzz" %}
To perform URL fuzzing:

```bash
secator w url_fuzz https://mydomain.com/start/fuzzing/from/here/
```
{% endtab %}

{% tab title="Code scan" %}
To perform code vulnerability scan:

```bash
secator w code_scan /path/to/code/repo
```
{% endtab %}

{% tab title="User hunt" %}
To find user accounts for a username:

```bash
secator w user_hunt elonmusk
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
Use **`secator w --help`** to list all available workflows.

Use **`secator w <NAME> --help`** to list workflow options.
{% endhint %}

***

## Scans

A scan is a set of workflows that run one after the other.

You can run some pre-written scans using the `secator s` subcommand:

{% tabs %}
{% tab title="Domain scan" %}
```
secator s domain example.com
```
{% endtab %}

{% tab title="Subdomain scan" %}
```
secator s subdomain sub.example.com
```
{% endtab %}

{% tab title="Network scan" %}
```
secator s network 192.168.1.0/24
```
{% endtab %}

{% tab title="URL Scan" %}
```
secator s url http://testphp.vulnweb.com
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
Use **`secator s --help`** to list all available scans.

Use **`secator s <NAME> --help`** to list scan options.
{% endhint %}

***

## Utils

`secator` provides a number of utilities that can be useful when doing pentesting.

**Proxy**

You can get a random proxy:

```bash
secator utils get-proxy                  # print a random proxy
secator utils get-proxy -n 5 --timeout 1 # print 5 proxies with 1s max timeout
```

**Offline CVEs**

You can get download CVEs information locally to avoid remote CVE lookups:

```bash
secator utils download-cves
```

**Reverse shells**

You can spawn reverse shells in any language, and optional netcat listener:

```bash
secator utils revshells                                     # list all reverse shells
secator utils revshells bash                                # show a Bash reverse shell
secator utils revshells javascript -h <LHOST> -p <LPORT>    # show a Javascript reverse shell to connect to LHOST / LPORT
secator utils revshells javascript -h <LHOST> -p <LPORT> -l # ... also spawn a netcat listener
```

**Recording**

You can record pentesting sessions as a GIF:

```bash
secator utils record -i <RECORD_NAME>                # record an interactive session
secator utils record --script test.sh <RECORD_NAME>  # put your commands in a script and record the execution
```

***
