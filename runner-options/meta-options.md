---
description: >-
  ... or options that are mutualized among task categories for efficiency,
  speed, and user-friendliness.
---

# Meta options

**Meta options** apply to **tasks**, **workflows**, or **scans**. When passed to **workflows** or **scans**, they will be passed to each task contained in the runner.

{% hint style="warning" %}
Some tasks, workflows, or scans do not support some of the options mentioned below. Run **`secator x/w/s <name> --help`** to get the complete list of supported options.
{% endhint %}

{% hint style="info" %}
Each option is documented with:
- **CLI**: Command-line flags (`--long-form` / `-short`)
- **Library**: Internal name for Python usage (e.g., `rate_limit=100`)
{% endhint %}

***

## Execution Options

### Threads

Number of threads to use. Applies to all tasks supporting threads (or concurrency).

| Form | Usage |
|------|-------|
| **CLI** | `--threads` / `-threads` |
| **Library** | `threads` |
| **Type** | `int` |

**Example:** set 50 threads

{% tabs %}
{% tab title="CLI" %}
```bash
secator w host_recon mydomain.com -threads 50
```
{% endtab %}

{% tab title="Library" %}
```python
from secator.workflows import host_recon
results = host_recon('mydomain.com', threads=50).run()
```
{% endtab %}
{% endtabs %}

***

## Requests Options

The following options will apply to tasks making network requests (if they implement it), no matter the protocol used (HTTP, TCP, UDP, DNS, FTP, ...).

### Proxy

Proxy (HTTP, Socks5, ...) to use when communicating with the targets.

| Form | Usage |
|------|-------|
| **CLI** | `--proxy` / `-proxy` |
| **Library** | `proxy` |
| **Type** | `str` |

**Example:** set proxies in config and use auto proxy selection

{% tabs %}
{% tab title="CLI" %}
```bash
secator config set http.http_proxy http://localhost:8080
secator config set http.socks5_proxy socks5://localhost:9050
secator w host_recon mydomain.com -proxy auto  # auto choose the right proxy
```
{% endtab %}

{% tab title="Library" %}
```python
from secator.workflows import host_recon
results = host_recon('mydomain.com', proxy='http://localhost:8080').run()
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
Learn more about [proxies.md](../in-depth/concepts/proxies.md "mention").
{% endhint %}

***

### Rate limit

Rate limit is an upper limit on the number of requests per second.

| Form | Usage |
|------|-------|
| **CLI** | `--rate-limit` / `-rl` |
| **Library** | `rate_limit` |
| **Type** | `int` |

**Example:** set a rate limit of 50 requests/second

{% tabs %}
{% tab title="CLI" %}
```bash
secator w host_recon mydomain.com -rl 50
```
{% endtab %}

{% tab title="Library" %}
```python
from secator.workflows import host_recon
results = host_recon('mydomain.com', rate_limit=50).run()
```
{% endtab %}
{% endtabs %}

***

### Timeout

Timeout is the time to wait (in seconds) before giving up on the request.

| Form | Usage |
|------|-------|
| **CLI** | `--timeout` / `-to` |
| **Library** | `timeout` |
| **Type** | `int` |

**Example:** set a request timeout of 10 seconds

{% tabs %}
{% tab title="CLI" %}
```bash
secator w host_recon mydomain.com -timeout 10
```
{% endtab %}

{% tab title="Library" %}
```python
from secator.workflows import host_recon
results = host_recon('mydomain.com', timeout=10).run()
```
{% endtab %}
{% endtabs %}

***

### Retries

Number of retries for failed requests.

| Form | Usage |
|------|-------|
| **CLI** | `--retries` / `-retries` |
| **Library** | `retries` |
| **Type** | `int` |

**Example:** set 5 retries for all requests

{% tabs %}
{% tab title="CLI" %}
```bash
secator w host_recon mydomain.com -retries 5
```
{% endtab %}

{% tab title="Library" %}
```python
from secator.workflows import host_recon
results = host_recon('mydomain.com', retries=5).run()
```
{% endtab %}
{% endtabs %}

***

### Delay

Delay to add between each request (in seconds).

| Form | Usage |
|------|-------|
| **CLI** | `--delay` / `-d` |
| **Library** | `delay` |
| **Type** | `float` |

**Example:** add a 0.5 second delay between requests

{% tabs %}
{% tab title="CLI" %}
```bash
secator w host_recon mydomain.com -d 0.5
```
{% endtab %}

{% tab title="Library" %}
```python
from secator.workflows import host_recon
results = host_recon('mydomain.com', delay=0.5).run()
```
{% endtab %}
{% endtabs %}

***

## HTTP Options

The following options will apply to tasks making HTTP requests (if they implement it).

### Header

Custom header to add to each request in the form "KEY1:VALUE1;; KEY2:VALUE2".

| Form | Usage |
|------|-------|
| **CLI** | `--header` / `-H` |
| **Library** | `header` |
| **Type** | `str` |

**Example:** set an Authorization and an Accept header

{% tabs %}
{% tab title="CLI" %}
```bash
secator x cariddi mydomain.com -H "Authorization: Basic <TOKEN>;; Accept: application/json"
```
{% endtab %}

{% tab title="Library" %}
```python
from secator.tasks import cariddi
results = cariddi('mydomain.com', header='Authorization: Basic <TOKEN>;; Accept: application/json').run()
```
{% endtab %}
{% endtabs %}

***

### Method

HTTP method to use for request GET, POST, PUT, DELETE, etc...

| Form | Usage |
|------|-------|
| **CLI** | `--method` / `-X` |
| **Library** | `method` |
| **Type** | `str` |

**Example:** use POST method for fuzzing

{% tabs %}
{% tab title="CLI" %}
```bash
secator x ffuf mydomain.com -X POST
```
{% endtab %}

{% tab title="Library" %}
```python
from secator.tasks import ffuf
results = ffuf('mydomain.com', method='POST').run()
```
{% endtab %}
{% endtabs %}

***

### Data

Data to send in the request body.

| Form | Usage |
|------|-------|
| **CLI** | `--data` / `-data` |
| **Library** | `data` |
| **Type** | `str` |

<details>

<summary>Example: send JSON data in POST request</summary>

{% tabs %}
{% tab title="CLI" %}
```bash
secator x ffuf mydomain.com/api -X POST -data '{"key":"value"}'
```
{% endtab %}

{% tab title="Library" %}
```python
from secator.tasks import ffuf
results = ffuf('mydomain.com/api', method='POST', data='{"key":"value"}').run()
```
{% endtab %}
{% endtabs %}

</details>

***

### User-agent

Custom user-agent to use for request.

| Form | Usage |
|------|-------|
| **CLI** | `--user-agent` / `-ua` |
| **Library** | `user_agent` |
| **Type** | `str` |

<details>

<summary>Example: use a custom user agent value</summary>

{% tabs %}
{% tab title="CLI" %}
```bash
secator x dalfox mydomain.com -ua "secator/1.0"
```
{% endtab %}

{% tab title="Library" %}
```python
from secator.tasks import dalfox
results = dalfox('mydomain.com', user_agent='secator/1.0').run()
```
{% endtab %}
{% endtabs %}

</details>

***

### Match regex

Keep responses which body content match the input.

| Form | Usage |
|------|-------|
| **CLI** | `--match-regex` / `-mr` |
| **Library** | `match_regex` |
| **Type** | `str` |

<details>

<summary>Example: keep responses which match the regex MySQLError.*</summary>

{% tabs %}
{% tab title="CLI" %}
```bash
secator x ffuf mydomain.com -mr "MySQLError.*"
```
{% endtab %}

{% tab title="Library" %}
```python
from secator.tasks import ffuf
results = ffuf('mydomain.com', match_regex='MySQLError.*').run()
```
{% endtab %}
{% endtabs %}

</details>

***

### Match size

Keep responses which body size (in bytes) match the input.

| Form | Usage |
|------|-------|
| **CLI** | `--match-size` / `-ms` |
| **Library** | `match_size` |
| **Type** | `int` |

<details>

<summary>Example: keep responses with 1025 bytes</summary>

{% tabs %}
{% tab title="CLI" %}
```bash
secator x katana mydomain.com -ms 1025
```
{% endtab %}

{% tab title="Library" %}
```python
from secator.tasks import katana
results = katana('mydomain.com', match_size=1025).run()
```
{% endtab %}
{% endtabs %}

</details>

***

### Match words

Keep responses which body word count match the input.

| Form | Usage |
|------|-------|
| **CLI** | `--match-words` / `-mw` |
| **Library** | `match_words` |
| **Type** | `int` |

<details>

<summary>Example: keep responses with 10 words</summary>

{% tabs %}
{% tab title="CLI" %}
```bash
secator x katana mydomain.com -mw 10
```
{% endtab %}

{% tab title="Library" %}
```python
from secator.tasks import katana
results = katana('mydomain.com', match_words=10).run()
```
{% endtab %}
{% endtabs %}

</details>

***

### Match codes

Keep responses which HTTP status codes match the input.

| Form | Usage |
|------|-------|
| **CLI** | `--match-codes` / `-mc` |
| **Library** | `match_codes` |
| **Type** | `str` |

<details>

<summary>Example: keep responses matching HTTP statuses 200, 400, 501</summary>

{% tabs %}
{% tab title="CLI" %}
```bash
secator x katana mydomain.com -mc 200,400,501
```
{% endtab %}

{% tab title="Library" %}
```python
from secator.tasks import katana
results = katana('mydomain.com', match_codes='200,400,501').run()
```
{% endtab %}
{% endtabs %}

</details>

***

### Filter regex

Filter out responses which body content match the input.

| Form | Usage |
|------|-------|
| **CLI** | `--filter-regex` / `-fr` |
| **Library** | `filter_regex` |
| **Type** | `str` |

<details>

<summary>Example: filter out responses containing the string LoginPage</summary>

{% tabs %}
{% tab title="CLI" %}
```bash
secator x ffuf mydomain.com -fr "LoginPage.*"
```
{% endtab %}

{% tab title="Library" %}
```python
from secator.tasks import ffuf
results = ffuf('mydomain.com', filter_regex='LoginPage.*').run()
```
{% endtab %}
{% endtabs %}

</details>

***

### Filter codes

Filter out responses which HTTP status codes match the input.

| Form | Usage |
|------|-------|
| **CLI** | `--filter-codes` / `-fc` |
| **Library** | `filter_codes` |
| **Type** | `str` |

<details>

<summary>Example: filter out responses matching HTTP status 500</summary>

{% tabs %}
{% tab title="CLI" %}
```bash
secator x ffuf mydomain.com -fc 500
```
{% endtab %}

{% tab title="Library" %}
```python
from secator.tasks import ffuf
results = ffuf('mydomain.com', filter_codes='500').run()
```
{% endtab %}
{% endtabs %}

</details>

***

### Filter size

Filter out responses which body size (in bytes) match the input.

| Form | Usage |
|------|-------|
| **CLI** | `--filter-size` / `-fs` |
| **Library** | `filter_size` |
| **Type** | `int` |

<details>

<summary>Example: filter out responses with 1025 bytes</summary>

{% tabs %}
{% tab title="CLI" %}
```bash
secator x ffuf mydomain.com -fs 1025
```
{% endtab %}

{% tab title="Library" %}
```python
from secator.tasks import ffuf
results = ffuf('mydomain.com', filter_size=1025).run()
```
{% endtab %}
{% endtabs %}

</details>

***

### Filter words

Filter out responses which body word count match the input.

| Form | Usage |
|------|-------|
| **CLI** | `--filter-words` / `-fw` |
| **Library** | `filter_words` |
| **Type** | `int` |

<details>

<summary>Example: filter out responses with 10 words</summary>

{% tabs %}
{% tab title="CLI" %}
```bash
secator x ffuf mydomain.com -fw 10
```
{% endtab %}

{% tab title="Library" %}
```python
from secator.tasks import ffuf
results = ffuf('mydomain.com', filter_words=10).run()
```
{% endtab %}
{% endtabs %}

</details>

***

### Follow redirect

Follow all HTTP redirects.

| Form | Usage |
|------|-------|
| **CLI** | `--follow-redirect` / `-frd` |
| **Library** | `follow_redirect` |
| **Type** | `flag` (boolean) |

<details>

<summary>Example: follow HTTP redirects</summary>

{% tabs %}
{% tab title="CLI" %}
```bash
secator x katana mydomain.com -frd
```
{% endtab %}

{% tab title="Library" %}
```python
from secator.tasks import katana
results = katana('mydomain.com', follow_redirect=True).run()
```
{% endtab %}
{% endtabs %}

</details>

***

### Depth

Scan depth for crawling tasks.

| Form | Usage |
|------|-------|
| **CLI** | `--depth` / `-depth` |
| **Library** | `depth` |
| **Type** | `int` |

<details>

<summary>Example: set crawl depth to 3</summary>

{% tabs %}
{% tab title="CLI" %}
```bash
secator x gospider mydomain.com -depth 3
```
{% endtab %}

{% tab title="Library" %}
```python
from secator.tasks import gospider
results = gospider('mydomain.com', depth=3).run()
```
{% endtab %}
{% endtabs %}

</details>

***

### Replay proxy

Proxy to use for replay requests (useful for fuzzing tasks).

| Form | Usage |
|------|-------|
| **CLI** | `--replay-proxy` / `-P` |
| **Library** | `replay_proxy` |
| **Type** | `str` |

<details>

<summary>Example: use a proxy for replay requests</summary>

{% tabs %}
{% tab title="CLI" %}
```bash
secator x ffuf mydomain.com/FUZZ -P http://localhost:8080
```
{% endtab %}

{% tab title="Library" %}
```python
from secator.tasks import ffuf
results = ffuf('mydomain.com/FUZZ', replay_proxy='http://localhost:8080').run()
```
{% endtab %}
{% endtabs %}

</details>

***

### Wordlist

Custom wordlist to use.

| Form | Usage |
|------|-------|
| **CLI** | `--wordlist` / `-w` |
| **Library** | `wordlist` |
| **Type** | `str` |

<details>

<summary>Example: use fuzz-Bo0oM wordlist</summary>

{% tabs %}
{% tab title="CLI" %}
```bash
secator x ffuf mydomain.com/FUZZ -w /usr/share/seclists/Fuzzing/fuzz-Bo0oM.txt
```
{% endtab %}

{% tab title="Library" %}
```python
from secator.tasks import ffuf
results = ffuf('mydomain.com/FUZZ', wordlist='/usr/share/seclists/Fuzzing/fuzz-Bo0oM.txt').run()
```
{% endtab %}
{% endtabs %}

</details>

***

## Port Scanning Options

The following options apply to port scanning tasks (e.g., `naabu`, `nmap`).

### Ports

Only scan specific ports. Accepts a comma-separated list of ports, or `-` for all ports.

| Form | Usage |
|------|-------|
| **CLI** | `--ports` / `-p` |
| **Library** | `ports` |
| **Type** | `str` |

<details>

<summary>Example: scan ports 80, 443, and 8080</summary>

{% tabs %}
{% tab title="CLI" %}
```bash
secator x naabu mydomain.com -p 80,443,8080
```
{% endtab %}

{% tab title="Library" %}
```python
from secator.tasks import naabu
results = naabu('mydomain.com', ports='80,443,8080').run()
```
{% endtab %}
{% endtabs %}

</details>

***

### Top ports

Scan the N most common ports.

| Form | Usage |
|------|-------|
| **CLI** | `--top-ports` / `-tp` |
| **Library** | `top_ports` |
| **Type** | `int` |

<details>

<summary>Example: scan top 100 most common ports</summary>

{% tabs %}
{% tab title="CLI" %}
```bash
secator x naabu mydomain.com -tp 100
```
{% endtab %}

{% tab title="Library" %}
```python
from secator.tasks import naabu
results = naabu('mydomain.com', top_ports=100).run()
```
{% endtab %}
{% endtabs %}

</details>

***

## Quick Reference Table

| Option | CLI Long | CLI Short | Library | Type |
|--------|----------|-----------|---------|------|
| Threads | `--threads` | `-threads` | `threads` | int |
| Proxy | `--proxy` | `-proxy` | `proxy` | str |
| Rate limit | `--rate-limit` | `-rl` | `rate_limit` | int |
| Timeout | `--timeout` | `-to` | `timeout` | int |
| Retries | `--retries` | `-retries` | `retries` | int |
| Delay | `--delay` | `-d` | `delay` | float |
| Header | `--header` | `-H` | `header` | str |
| Method | `--method` | `-X` | `method` | str |
| Data | `--data` | `-data` | `data` | str |
| User-agent | `--user-agent` | `-ua` | `user_agent` | str |
| Match regex | `--match-regex` | `-mr` | `match_regex` | str |
| Match size | `--match-size` | `-ms` | `match_size` | int |
| Match words | `--match-words` | `-mw` | `match_words` | int |
| Match codes | `--match-codes` | `-mc` | `match_codes` | str |
| Filter regex | `--filter-regex` | `-fr` | `filter_regex` | str |
| Filter codes | `--filter-codes` | `-fc` | `filter_codes` | str |
| Filter size | `--filter-size` | `-fs` | `filter_size` | int |
| Filter words | `--filter-words` | `-fw` | `filter_words` | int |
| Follow redirect | `--follow-redirect` | `-frd` | `follow_redirect` | flag |
| Depth | `--depth` | `-depth` | `depth` | int |
| Replay proxy | `--replay-proxy` | `-P` | `replay_proxy` | str |
| Wordlist | `--wordlist` | `-w` | `wordlist` | str |
| Ports | `--ports` | `-p` | `ports` | str |
| Top ports | `--top-ports` | `-tp` | `top_ports` | int |

***
