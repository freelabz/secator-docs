---
description: ... or how you can use secator as your pentesting swiss-knife.
---

# CLI Usage

`secator` is first and foremost a command-line interface (CLI). This page describes how to use it in-depth.

***

## Usage

```bash
secator --help # General help
secator x      # List available tasks
secator w      # List available workflows
secator s      # List available scans
secator u      # List available utilities
```

***

## Running tasks

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
Use **`secator x <NAME> --help`** to list options for a specific task.
{% endhint %}

***

## Running workflows

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
Use **`secator w <NAME> --help`** to list options for a specific workflow.
{% endhint %}

***

## Running scans

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
Use **`secator s <NAME> --help`** to list a options for a specific scan.
{% endhint %}

***

## Running utils

`secator` provides a number of utilities that can be useful when doing pentesting.

### **Proxy**

You can get a random proxy:

```bash
secator u proxy                  # print a random proxy
secator u proxy -n 5 --timeout 1 # print 5 proxies with 1s max timeout
```

### **Reverse shells**

You can spawn reverse shells in any language, and optional netcat listener:

```bash
secator u revshell                                     # list all reverse shells
secator u revshell bash                                # show a Bash reverse shell
secator u revshell javascript -h <LHOST> -p <LPORT>    # show a Javascript reverse shell to connect to LHOST / LPORT
secator u revshell javascript -h <LHOST> -p <LPORT> -l # ... also spawn a netcat listener
```

### Serve

You can run an HTTP server to serve payloads:

```sh
secator u serve
```

### **Recording**

You can record pentesting sessions as a GIF:

```bash
secator u record -i <RECORD_NAME>                # record an interactive session
secator u record --script test.sh <RECORD_NAME>  # put your commands in a script and record the execution
```

***

## Configuring secator

To configure `secator`, use the following commands:

```bash
secator c get                                     # get full config (with defaults)
secator c get --user                              # get user config
secator c get wordlists.defaults.http             # get default wordlist path
secator c set wordlists.defaults.http rockyou.txt # set default wordlist 
secator c edit                                    # edit user config yaml
secator c default                                 # get default config
```

To see the full available configuration options,  get the default configuration using `secator c default`.

***

## Running a worker \[optional]

You can enable enable distributed runs by starting `secator` workers.  All tasks / workflows / scans will be sent to the workers for execution.

You can run a worker using the file system as a broker and result backend:

```bash
secator install addons worker
secator worker
```

{% hint style="info" %}
Learn more about [distributed-runs-with-celery.md](../in-depth/distributed-runs-with-celery.md "mention")
{% endhint %}

***
