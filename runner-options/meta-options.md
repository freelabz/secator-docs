---
description: >-
  ... or options that are mutualized among task categories for efficiency,
  speed, and user-friendliness.
---

# Meta options

**Meta options** apply to **tasks**, **workflows**, or **scans**. When passed to **workflows** or **scans**, they will be passed to each task contained in the runner.

{% hint style="warning" %}
Some tasks, workflows, or scans do not support some of the options mentioned below. Ru&#x6E;**`secator x/w/s <name> --help`** to get the complete list of supported options.
{% endhint %}

***

## Execution Options

### Threads (`-threads`)

Number of threads to use. Applies to all tasks supporting threads (or concurrency).

<details>

<summary>Example: set 50 threads</summary>

```bash
secator w host_recon mydomain.com -threads 50
```

</details>

***

## Requests Options

The following options will apply to tasks making network requests (if they implement it), no matter the protocol used (HTTP, TCP, UDP, DNS, FTP, ...).

### Proxy (`-proxy`)

Proxy (HTTP, Socks5, ...) to use when communicating with the targets.

<details>

<summary>Example: set proxies in config and <code>-proxy</code> to <code>auto</code></summary>

```bash
secator config set http.http_proxy http://localhost:8080
secator config set http.socks5_proxy socks5://localhost:9050
secator w host_recon mydomain.com -proxy auto  # auto choose the right proxy
```

</details>

{% hint style="info" %}
Learn more about [proxies.md](../in-depth/concepts/proxies.md "mention").
{% endhint %}

***

### Rate limit (`-rl`)

Rate limit is an upper limit on the number of requests per second.

<details>

<summary>Example: set a rate limit of <code>50</code> requests/second</summary>

```bash
secator w host_recon mydomain.com -rl 50
```

</details>

***

### Timeout (`-timeout`)

Timeout is the time to wait (in seconds) before giving up on the request.

<details>

<summary>Example: set a request timeout of <code>10</code> seconds</summary>

```bash
secator w host_recon mydomain.com -timeout 10
```

</details>

***

### Retries (`-retries`)

Number of retries for failed requests.

<details>

<summary>Example: set <code>5</code> retries for all requests</summary>

```bash
secator w host_recon mydomain.com -retries 5
```

</details>

***

### Delay (`-d`)

Delay to add between each request (in seconds).

<details>

<summary>Example: add a <code>0.5</code> second delay between requests</summary>

```bash
secator w host_recon mydomain.com -d 0.5
```

</details>

***

## HTTP Options

The following options will apply to tasks making HTTP requests (if they implement it).

### Header (`-H`)

Custom header to add to each request in the form "KEY1:VALUE1;; KEY2:VALUE2".

<details>

<summary>Example: set an <code>Authorization</code> and an <code>Accept</code> header</summary>

```bash
secator x cariddi mydomain.com -H "Authorization: Basic <TOKEN>;; Accept: application/json"
```

</details>

***

### Method (`-X`)

HTTP method to use for request GET, POST, PUT, DELETE, etc...

<details>

<summary>Example: use <code>POST</code> method for fuzzing</summary>

```bash
secator x ffuf mydomain.com -X POST
```

</details>

***

### Data (`-data`)

Data to send in the request body.

<details>

<summary>Example: send JSON data in POST request</summary>

```bash
secator x ffuf mydomain.com/api -X POST -data '{"key":"value"}'
```

</details>

***

### User-agent (`-ua`)

Custom user-agent to use for request.

<details>

<summary>Example: use <code>secator</code> as a user agent value</summary>

```bash
secator x dalfox mydomain.com -ua secator
```

</details>

***

### **Match regex (`-mr)`**

Keep responses which body content match the input.

<details>

<summary>Example: keep responses which match the regex<code>MySQLError.*</code></summary>

```bash
secator x ffuf mydomain.com -mr MySQLError.*
```

</details>

***

### Match size (`-ms`)

Keep responses which body size (in bytes) match the input.

<details>

<summary>Example: keep responses with <code>1025</code> bytes</summary>

```bash
secator x katana mydomain.com -ms 1026  # bytes
```

</details>

***

### Match-words (`-mw)`

Keep responses which body word count match the input.

<details>

<summary>Example: keep responses with <code>10</code> words</summary>

```bash
secator x katana mydomain.com -mw 10
```

</details>

***

### Match code (`-mc`)

Keep responses which HTTP status codes match the input.

<details>

<summary>Example: keep responses matching HTTP statuses <code>200</code>,<code>400</code>,<code>501</code></summary>

```bash
secator x katana mydomain.com -mc 200,400,501
```

</details>

***

### Filter regex (`-fr`)

Filter out responses which body content match the input.

<details>

<summary>Example: filter out responses containing the string <code>LoginPage</code></summary>

```bash
secator x ffuf mydomain.com -fr LoginPage.*
```

</details>

***

### Filter codes (`-fc`)

Filter out responses which HTTP status codes match the input.

<details>

<summary>Example: filter out responses matching HTTP status <code>500</code></summary>

```bash
secator x ffuf mydomain.com -fc 500
```

</details>

***

### Filter size (`-fs)`

Filter out responses which body size (in bytes) match the input.

<details>

<summary>Example: filter out responses with <code>1025</code> bytes</summary>

```bash
secator x ffuf mydomain.com -fs 1025
```

</details>

***

### Filter words (`-fw`)

Filter out responses which body word count match the input.

<details>

<summary>Example: filter out responses with <code>10</code> words</summary>

```bash
secator x ffuf mydomain.com -fw 10
```

</details>

***

### Follow redirect (`-frd`)

Follow all http redirects.

<details>

<summary>Example: follow HTTP redirects</summary>

```bash
secator x katana mydomain.com -frd
```

</details>

***

### Depth (`-depth`)

Scan depth for crawling tasks.

<details>

<summary>Example: set crawl depth to <code>3</code></summary>

```bash
secator x gospider mydomain.com -depth 3
```

</details>

***

### Replay proxy (`-P`)

Proxy to use for replay requests (useful for fuzzing tasks).

<details>

<summary>Example: use a proxy for replay requests</summary>

```bash
secator x ffuf mydomain.com/FUZZ -P http://localhost:8080
```

</details>

***

### Wordlist (`-w`)

Custom wordlist to use.

<details>

<summary>Example: use fuzz-Bo0oM wordlist</summary>

```bash
secator x ffuf mydomain.com/FFUF/ -w /usr/share/seclists/Fuzzing/fuzz-Bo0oM.txt
```

</details>

***

## Port Scanning Options

The following options apply to port scanning tasks (e.g., `naabu`, `nmap`).

### Ports (`-p`)

Only scan specific ports. Accepts a comma-separated list of ports, or `-` for all ports.

<details>

<summary>Example: scan ports <code>80</code>, <code>443</code>, and <code>8080</code></summary>

```bash
secator x naabu mydomain.com -p 80,443,8080
```

</details>

***

### Top ports (`-tp`)

Scan the N most common ports.

<details>

<summary>Example: scan top <code>100</code> most common ports</summary>

```bash
secator x naabu mydomain.com -tp 100
```

</details>

***
