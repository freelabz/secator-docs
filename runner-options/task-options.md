---
description: ... or options that you can use in any context.
---

# Global options

**Global options** apply to all runners (task, workflow, scan)  and allow to control the overrall behaviour of the run.

***

### Workspace (`-ws`)

You can pass a workspace name to use for the runner, which will save all reports to a subfolder named after the workspace.

<details>

<summary><strong>Example: Save results to <code>mydomain</code> workspace</strong></summary>

```bash
secator x httpx mydomain.com -ws mydomain
secator w host_recon mydomain.com -ws mydomain
secator s domain mydomain.com -ws mydomain
```

</details>

***

### Output (`-o`)

You can export reports in various formats using built-in exporters.

<details>

<summary><strong>Example:</strong> export reports as <code>table</code>, <code>csv</code>, and <code>json</code>formats</summary>

```bash
secator x httpx mydomain.com -o table,csv,json
secator w host_recon mydomain.com -o table,csv,json
secator s domain mydomain.com -o table,csv,json
```

</details>

{% hint style="info" %}
Learn more about [exporters.md](../in-depth/concepts/exporters.md "mention").
{% endhint %}

***

### Drivers (`-driver`)

You can export live results to different targets using drivers.&#x20;

To use drivers, make sure you install the corresponding addon using `secator install addons <NAME>`.

<details>

<summary><strong>Example -</strong> export live results to MongoDB</summary>

First, install the `mongodb` addon using `secator install addons mongodb`

Then, use the `-driver` flag route your results:

```bash
secator x httpx mydomain.com -driver mongodb
secator w host_recon mydomain.com -driver mongodb
secator s domain mydomain.com -driver mongodb
```

</details>

{% hint style="info" %}
Learn more about [drivers.md](../in-depth/concepts/drivers.md "mention").
{% endhint %}

***

### Profiles (`-pf`)

You can apply one or more [profiles.md](../in-depth/concepts/profiles.md "mention") (comma-separated) to set many options at once.

<details>

<summary><strong>Example -</strong> run a polite, passive domain scan</summary>

```bash
secator s domain mydomain.com -pf polite,passive
```

</details>

***

### Sync / worker mode (`-sync`, `-np`)

When a Celery worker is configured, runs are sent to workers by default. Use `-sync` to run locally instead, or `-np` (`--no-poll`) to send the run to workers without waiting for its results.

<details>

<summary><strong>Example -</strong> send a scan to workers and return immediately</summary>

```bash
secator s host mydomain.com -np
```

</details>

{% hint style="info" %}
Learn more about [distributed-runs-with-celery.md](../in-depth/distributed-runs-with-celery.md "mention").
{% endhint %}

***

### Inspect a runner (`-dry`, `-tree`, `-yaml`)

Show what a runner would do without running it:

```bash
secator x nmap mydomain.com -dry   # show the exact command that would run
secator s host -tree               # show the scan tree (workflows and tasks)
secator w host_recon -yaml         # show the workflow YAML
```

***

### Runtime stats and profiling (`-stat`, `-pyinstrument`, `-memray`)

`-stat` prints runtime statistics (CPU, memory) of the commands being run. `-pyinstrument` and `-memray` profile `secator` itself (install the `trace` addon first); results are saved to `~/.secator/performance`.

```bash
secator x httpx mydomain.com -stat
```

***

### Target scope (Python only)

Runners accept `in_scope` and `out_of_scope` options: allow / deny lists checked against the inputs of every runner, including targets discovered during a workflow or scan. Out-of-scope inputs are dropped with a warning. Entries can be IPs, CIDR ranges, exact hosts, wildcards (`*.example.com` matches sub-domains, not the apex) or regexes. Deny wins over allow, and an empty `in_scope` allows everything not denied. Non-network inputs (emails, usernames, paths) are never filtered.

```python
from secator.workflows import host_recon

workflow = host_recon(
    'mydomain.com',
    in_scope=['mydomain.com', '*.mydomain.com', '10.0.0.0/24'],
    out_of_scope=['admin.mydomain.com'],
)
workflow.run()
```

***
