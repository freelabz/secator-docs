# AI suggestions

Suggestions are *actionable hints* generated automatically from the findings already collected in a workspace. They show up in the workspace's **Suggestions** tab and (optionally) appear on the Dashboard via the **View suggestions** button.

### Where they come from

Once **AI suggestions** is enabled (Workspace settings → *General* tab), a background job analyses each new wave of findings — open ports, exposed certificates, subdomains, web technologies, leaked emails — and proposes follow-up actions. There is no manual prompt to write; suggestions are pushed asynchronously as data accrues.

### What a suggestion looks like

Each suggestion is an expandable card with:

- **A title and an icon** — at a glance, the kind of action proposed (run a scan, run a workflow, run a single tool, add a target).
- **A natural-language `message`** — *why* the system proposed this. Examples: *"Ports 22, 80, 443 detected on `host-3.acme.com` — running an `sshaudit` task could surface weak ciphers"*, or *"`api.acme.com` was discovered via subdomain enumeration but is not yet a target — adding it lets you scan its endpoints"*.
- **`help` lines** — short reminders or warnings about the proposed action (run hours impact, scope, expected duration).
- **A `cost_evaluation`** — an estimate of how many run hours / how much wall-time the action will consume so you can decide before clicking.
- **A list of related runs** — if you have already executed similar runners on this target, they are linked here so you can compare results.

### Suggestion types

| Type | What clicking it does |
|---|---|
| **Runner** (scan / workflow / task) | Opens the *Run* form pre-filled with the suggested runner, target, and options. You can review and tweak before launching. |
| **Add target** | Opens the *Target* form pre-filled with the asset the system thinks should be in scope. Useful right after a subdomain or DNS recon run. |

### Actions on a suggestion

- **Run now** — Launches the proposed runner immediately. Once executed, the suggestion is marked *done* and decorated with the run's status.
- **Add target** — Opens the target sheet, with workspace and asset pre-filled.
- **Dismiss** — Removes the suggestion from the active list. Useful when the suggestion does not apply to your engagement.

> [!note]
> Suggestions are workspace-scoped. Disabling AI suggestions in *Workspace settings → General* stops new suggestions from being generated; existing ones stay until dismissed or executed.

### Tuning what suggestions you get

- **Workspace scope** (allowlist / denylist) — Suggestions only consider in-scope assets.
- **Display settings** (Workspace settings → *Display* tab) — Hiding finding types you don't care about prevents suggestions of that flavour.
- **Notifications** — You can subscribe to a notification when a new suggestion appears (Workspace settings → *Notifications* tab).

> [!tip]
> Use suggestions as a *checklist*, not a roadmap. Always review the proposed options and the cost estimate before clicking *Run now*.
