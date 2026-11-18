# Platform overview

Secator orchestrates more than 45 specialized open-source security tools through three layers of automation:

| Type | What it is |
|---|---|
| **Task** | A single tool execution (e.g. `nmap`, `httpx`, `nuclei`) with its options. |
| **Workflow** | A predefined chain of tasks that share inputs and outputs (e.g. *url_crawl*, *subdomain_recon*). |
| **Scan** | A higher-level composition of workflows for an entire engagement (e.g. *host*, *domain*, *network*). |

When you launch a runner, the platform:

1. Resolves the input target against the workspace **scope** (allowlist / denylist).
2. Applies the chosen **profile** (aggressive, passive, stealth, default) to fill in option presets.
3. Schedules the underlying tasks across a worker pool and streams the **task tree** to the UI in real time.
4. Normalises every tool's output into the same **finding** schema, deduplicates across tools, and stores it in the workspace.
5. Aggregates findings into per-workspace charts, sitemaps, and an **infrastructure force graph**.

Both *Available scans* and *Available workflows* below list every runner that ships with the platform, with the full task tree per workflow.

> [!note]
> Scans, workflows and tasks are configured as YAML files inside the secator package. The cards below are generated directly from those files, so they always reflect what you can launch from the *Run* form.
