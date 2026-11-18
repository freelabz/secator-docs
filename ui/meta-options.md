# Meta options

Meta options are *transverse* flags that apply across most tasks, regardless of the underlying tool. They appear in the **Options** panel of the *Run* form, in the runner's option summary card, and in the dynamic forms generated for each task.

> [!note]
> Each task can override or hide an option that does not apply to it (e.g. *Match codes* does not show up on tasks that do not produce HTTP responses). The list below is the **superset** — what you can find across the platform.

### Performance

| Option | Default | What it does | When to tune it |
|---|---|---|---|
| **Rate limit** | tool-specific | Upper limit on requests **per second**. | Production targets, WAF-protected sites. The `polite` profile sets it to 100; `aggressive` to 10 000; `paranoid` to 5. |
| **Threads** | `50` | Number of concurrent workers inside a single tool. | Lower for fragile targets, raise for cooperative ones. |
| **Delay** | `0` | Seconds to wait **between** successive requests. | Combined with a low rate-limit, useful for stealth or shared infrastructure. |
| **Timeout** | tool-specific | Per-request timeout in seconds. | Slow / unstable targets; cap to protect your [run hours](glossary.md#g-run-hours). |
| **Retries** | `0` to `2` | Re-send a failed request before giving up. | Lossy networks, rate-limited APIs (combine with *Delay*). |
| **Proxy** | none | Route the tool's traffic through HTTP / SOCKS5 / `proxychains`. | Egress through Burp Suite, route via VPN, or pick the `tor` profile. |

> [!tip]
> Most of these are bundled into [profiles](runners.md#available-profiles). When in doubt pick `polite`, `paranoid`, `aggressive`, `insane` or `tor` instead of editing each option by hand.

### HTTP requests

Apply to every web-facing task (`httpx`, `katana`, `gospider`, `cariddi`, `dirsearch`, `feroxbuster`, `ffuf`, `nuclei`, `dalfox`, …).

| Option | What it does | When to use |
|---|---|---|
| **Method** | HTTP verb (`GET`, `POST`, `PUT`, `DELETE`, …). | Probing CRUD endpoints. |
| **Headers** | Custom request headers, repeatable. | `Authorization` for authenticated scans, `Host` for virtual-host probing, custom CSRF tokens. |
| **Data** | Request body content (form-encoded, JSON, raw). | POST-based fuzzing, GraphQL endpoints, JSON APIs. |
| **User agent** | Custom `User-Agent` header. | Bypass UA-based filtering; identify yourself in the client's logs. |
| **Follow redirect** | Follow `30x` redirects automatically. | Login redirects, virtual hosts that redirect to canonical domains. |
| **Depth** | Maximum recursion depth for crawlers. | Bound a passive crawl that would otherwise spider an entire SaaS. |
| **Replay proxy** | Replay every request through a separate proxy *after* execution (typically Burp). | Hand off to manual review without slowing the live run. |
| **Wordlist** | Custom wordlist for fuzzing tasks. | Targeted dictionaries (CMS-specific, language-specific, client-supplied). |

### Response filtering

When a task produces many HTTP responses, these options pick which become findings.

The `match-*` family is **inclusive** — only responses matching at least one criterion are kept. The `filter-*` family is **exclusive** — responses matching are dropped.

| Option | What it matches |
|---|---|
| **Match codes** | HTTP status codes to keep (e.g. `200,301,401`). |
| **Match regex** | Response body matches this regex. |
| **Match size** / **Match words** | Body byte size / word count to keep. |
| **Filter codes** | HTTP status codes to drop (e.g. `404,403`). |
| **Filter regex** | Drop responses whose body matches this regex. |
| **Filter size** / **Filter words** | Drop by body size / word count — useful to hide a fixed-length error page. |

> [!tip]
> A common URL-fuzz preset is *Match codes* `200,204,301,302,401,403,405,500` plus *Filter size* on the boilerplate length of the target's 404 page. The `url_crawl` workflow already ships with the match-codes preset.

### Port scanning

Apply to the network-scanning tasks (`nmap`, `naabu`).

| Option | What it does | When to use |
|---|---|---|
| **Ports** | Specific TCP ports (comma-list) **or** `-` for all 65 535. | Tailored scans (`80,443,8080,8443` for web-only) or full surface mapping. |
| **Top ports** | Scan the *top N* most common ports per nmap's frequency database. | Faster than scanning all 65 535 while still covering the realistic surface. |
| **Skip host discovery** | Tell nmap to assume the host is up and skip the ICMP / ARP probe. | When the target blocks ICMP — without this nmap may report *"host down"* and abort. |
| **Fragment** *(profile-only)* | Split SYN packets into IP fragments for IDS/IPS evasion. | Picked via the `sneaky` profile. |
| **TCP SYN stealth** *(profile-only)* | SYN scan (`-sS`) without completing the TCP handshake. | Lower footprint in target logs. Picked via the `stealth` profile. |

> [!warning]
> The default `nmap` task sweeps *top-1000 TCP ports* and uses ICMP host discovery. On hosts where outbound ICMP is blocked, this returns *"host down"* and the deeper scan never runs. Either pick the `all_ports` profile, set explicit *Ports*, or enable **Skip host discovery**.

### Workspace & output

| Option | What it does |
|---|---|
| **Workspace** | Saves all reports under a workspace-named scope. In the UI this is the workspace selector at the top of the Run form. |
| **Output** | Built-in export formats (`txt`, `csv`, `json`, `gdrive`). In the UI this is exposed via [Reports](reports.md). |
| **Drivers** | Stream live results to an external destination during execution (MongoDB, GCS). Configured at the worker level, not from the UI. |
