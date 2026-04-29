# Quickstart — first run in 5 minutes

If you only have five minutes, follow these four steps and you will see your first findings appear:

1. **Sign in** at `secator.local:3000` (or your team's URL) with email + password, Google, or GitHub.
2. **Create a workspace** from the Dashboard prompt or from *Workspaces → Create workspace*. Name it after the engagement (e.g. `client-acme-feb`). The workspace is the container for everything that follows — targets, runs, findings, reports.
3. **Add a target** in the workspace's *Targets* tab. Pick the type (`url`, `domain`, `subdomain`, `host`, `cidr`, …), paste the asset, and tick the legal authorization checkbox.
4. **Run a scan**. Click *Run* on the workspace overview and pick the **`url`** scan if you added a URL, or the **`domain`** / **`subdomain`** / **`host`** / **`network`** scan that matches your target type. Leave defaults, accept the legal terms, hit *Run*.

> [!tip]
> Within seconds the Runner detail page shows a **task tree** filling in (each tool turns green as it finishes) and the **Findings tabs** populate live — vulnerabilities, ports, URLs, certificates. You don't need to refresh; the page polls every 20 seconds while a run is in progress.

What to do next:

- Open the **Findings** tab inside the runner to triage what was discovered. Use the severity filter to start with Criticals/Highs.
- Switch to the **Sitemap** view to see the URL map of the target.
- Switch to the **Infrastructure** force graph to see exposed assets and their relationships.
- Look at the **Suggestions** tab on the workspace — if AI suggestions are enabled, follow-up scans / new targets to add are proposed automatically based on what was found (see [AI suggestions](ai-suggestions.md)).
- When you are happy with the results, build a client-ready deliverable from *Reports → Create report*.

> [!warning]
> Always confirm you have written authorization to scan a target before running anything. The legal checkbox is not a formality — it is your audit trail.
