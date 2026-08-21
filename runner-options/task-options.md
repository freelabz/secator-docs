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

### Profiles (`-pf`)

Profiles are named presets of options (rate limits, ports, tools to enable, drivers, exporters, ...) that you can apply to any runner. Pass one or more comma-separated profile names.

<details>

<summary><strong>Example -</strong> run with the <code>aggressive</code> profile</summary>

```bash
secator x httpx mydomain.com -pf aggressive
secator w host_recon mydomain.com -pf aggressive
secator s domain mydomain.com -pf aggressive,all_ports
```

</details>

{% hint style="info" %}
Use **`secator profile list`** (alias `secator p list`) to list available profiles.
{% endhint %}

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

