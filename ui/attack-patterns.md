# Attack patterns

This is the *cookbook* of the platform — concrete, intent-driven recipes. Each pattern says *what you want to do*, *what to click*, and *where to look at the result*. Pick the closest pattern to your engagement, then tune the options to your scope.

### Bug bounty — out-of-scope guard

**Goal:** confirm a candidate asset is in scope before any active probe.

1. Workspace settings → *Scope* tab → enter the program's allowlist patterns (and denylist for explicit out-of-scope domains).
2. Run **`subdomain_recon`** workflow with profile **`passive`** on the program's apex domain.
3. Open the *Findings → Subdomain* tab. Subdomains that fall outside the allowlist are tagged `scope-mismatch` and shown in red.
4. Resolve / drop the out-of-scope ones before adding them as targets.

> [!tip]
> Combine with the *Suggestions* tab: the platform proposes adding only allowlist-compatible subdomains as new targets.

### Authenticated web app scan

**Goal:** scan an app behind a login.

1. Get a valid session token / API key from the app.
2. Open the *Run* form for the **`url_crawl`** workflow on your target URL.
3. In *Options*, set **Headers** to: `Authorization: Bearer <token>`. For cookie-based auth use `Cookie: session=...`.
4. Optionally set **Method** + **Data** if the app expects POST navigation (rare).
5. Chain with **`url_vuln`** in the same workspace — both will reuse the workspace targets and you'll get `nuclei` + `dalfox` running with the same auth context.

> [!warning]
> Pick the **`polite`** profile for production apps to avoid filling the audit log with rate-limited 429s.

### WordPress CVE audit

**Goal:** find known CVEs on a WordPress install.

1. Run the **`wordpress`** workflow with profile **`aggressive`** if scope allows, otherwise **`polite`**.
2. Open *Findings → Vulnerability*. Filter by **Severity** ≥ High.
3. Each vulnerability with an `id` (CVE) shows a **Source** badge (`wpscan`, `wpprobe`, `nuclei`).
4. The **Exploit** tab right next to it lists `searchsploit` matches: ready-to-use PoCs for the same CVE.

### Find leaked secrets in a target's JS

**Goal:** identify hardcoded API keys / tokens shipped in front-end JS.

1. Run **`url_crawl`** with the **`hunt_secrets`** profile on the target.
2. Wait for the run to complete. Switch to *Findings → Tag*.
3. Filter by tag value: `aws_key`, `api_key`, `jwt`, `private_key`, `slack_webhook`, `gcp_credentials`.
4. Click any finding → the *Record* link shows the exact JS file and line where the secret was found.

### Internal CIDR mapping

**Goal:** map a /24 internal network during an on-site engagement.

1. Add the CIDR (e.g. `10.0.0.0/24`) as a target in the workspace.
2. Run **`cidr_recon`** workflow with profile **`active`**.
3. Open the workspace's *Overview* tab → **Infrastructure Graph** to see the live host topology.
4. Switch to *Findings → Port* to see the open services per host, then chain `nmap` (deep) tasks on interesting hosts.

> [!note]
> Layer 2 traffic (ARP, ICMP) requires the worker to be on the same network — typically a worker deployed inside the client's environment.

### 40x bypass on a forbidden endpoint

**Goal:** see if a `403 Forbidden` page can be reached through bypass techniques.

1. From *Tasks → Run a task*, pick **`bup`**.
2. Set the target URL to the forbidden endpoint (e.g. `https://target/admin`).
3. Leave the default 30+ techniques enabled.
4. The runner shows a per-technique table: bypass technique → response status → response size. Anything other than the original 403 is worth investigating manually.

### Unknown-tech triage

**Goal:** you have a black-box target and don't know yet which workflow fits.

1. Add the target.
2. Run the **`url`** scan with profile **`passive`** + **`http_headless`**.
3. Open *Findings → URL* and look at the **Tech** column. The detected stack (PHP, Drupal, Spring, …) tells you which dedicated workflow to run next: `wordpress` for WP, `url_vuln` + `dalfox` for generic webapp, `code_scan` if a public repo was discovered, etc.

> [!tip]
> The *Suggestions* tab usually proposes the right next workflow automatically based on the detected technologies. Save these clicks by enabling AI suggestions in workspace settings.
