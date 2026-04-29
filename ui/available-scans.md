# Available scans

5 scans ship with the platform. Each one bundles several workflows to cover an entire engagement type. Pick one, point it at a target, and the matching combination of crawling, fuzzing, and vulnerability checks runs automatically.

Scans are picked from the **Run** form (Workspace → *Run* → *Scan* tab).

---

### `domain`

_Domain scan_

Comprehensive security assessment of a domain, combining multiple workflows for complete coverage.
Performs domain reconnaissance, subdomain discovery, host reconnaissance, URL crawling, and
vulnerability scanning. Provides a full picture of the domain's attack surface, infrastructure,
and potential security issues. Ideal for thorough domain-level security assessments.

**Input types:** `host`

**Tags:** `recon` `dns` `ssl` `network` `http` `crawl` `takeovers` `vuln` `secrets`

**Workflows it runs:**

- [`domain_recon`](./available-workflows.md#domain_recon)
- [`subdomain_recon`](./available-workflows.md#subdomain_recon)
- [`host_recon`](./available-workflows.md#host_recon)
- [`url_crawl`](./available-workflows.md#url_crawl)
- [`url_vuln`](./available-workflows.md#url_vuln)


---

### `host`

_Host scan_

In-depth security assessment of a specific host or IP address.
Combines host reconnaissance with URL crawling and vulnerability scanning to identify
open ports, running services, web applications, and potential security weaknesses.
Perfect for targeted host-level security testing and penetration testing.

**Input types:** `host` `ip`

**Tags:** `recon` `dns` `network` `http` `crawl` `ssl` `vuln` `secrets`

**Workflows it runs:**

- [`host_recon`](./available-workflows.md#host_recon)
- [`url_crawl`](./available-workflows.md#url_crawl)
- [`url_vuln`](./available-workflows.md#url_vuln)


---

### `network`

_Internal network scan_

Comprehensive security assessment of an internal network or CIDR range.
Discovers live hosts, scans for services and vulnerabilities, and performs URL-based
testing on discovered web applications. Combines CIDR reconnaissance with web application
security testing. Essential for internal network security assessments and lateral movement testing.

**Input types:** `cidr_range` `slug`

**Tags:** `recon` `cidr` `dns` `network` `internal` `http` `crawl` `ssl` `vuln` `secrets`

**Workflows it runs:**

- [`cidr_recon`](./available-workflows.md#cidr_recon)
- [`host_recon`](./available-workflows.md#host_recon)
- [`url_crawl`](./available-workflows.md#url_crawl)
- [`url_vuln`](./available-workflows.md#url_vuln)


---

### `subdomain`

_Subdomain scan_

Complete security assessment focused on subdomain discovery and testing.
Discovers all subdomains of a target domain, performs reconnaissance on discovered hosts,
crawls web applications, and scans for vulnerabilities. Identifies the full subdomain
attack surface and potential security issues. Crucial for comprehensive domain security testing.

**Input types:** `host`

**Tags:** `recon` `dns` `network` `http` `crawl` `ssl` `takeovers` `vuln` `secrets`

**Workflows it runs:**

- [`subdomain_recon`](./available-workflows.md#subdomain_recon)
- [`host_recon`](./available-workflows.md#host_recon)
- [`url_crawl`](./available-workflows.md#url_crawl)
- [`url_vuln`](./available-workflows.md#url_vuln)


---

### `url`

_URL scan_

Thorough security assessment of web applications and URLs.
Combines URL crawling, fuzzing, and vulnerability scanning to discover hidden content,
identify potential attack vectors, and find security vulnerabilities. Tests for common
web vulnerabilities including XSS, injection flaws, and misconfigurations. Essential for web application security testing.

**Input types:** `url`

**Tags:** `http` `crawl` `fuzz` `vuln` `secrets`

**Workflows it runs:**

- [`url_crawl`](./available-workflows.md#url_crawl)
- [`url_fuzz`](./available-workflows.md#url_fuzz)
- [`url_params_fuzz`](./available-workflows.md#url_params_fuzz)
- [`url_vuln`](./available-workflows.md#url_vuln)

