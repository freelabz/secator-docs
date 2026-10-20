# Targets

Targets are what you scan: a domain, subdomain, IP, CIDR, URL, or other asset. They live inside a workspace.

From the workspace's **Targets** tab you can:

- **Add target** — Open the form, choose the workspace, name the target, pick a type (domain, IP, URL, CIDR, …), and **confirm legal authorization** to scan it (required checkbox).
- **Edit target** — Click a row to update name, type, or tags.
- **Delete target** — From the action column, with confirmation.
- **Filter** by type, status, and tags.
- **Sort** by name or creation date.
- **Search** by name.
- **Paginate** through long lists.

A dedicated target detail page (`Target details`) is available by clicking a row — it shows the full asset profile and lets you drill into related findings.

> [!warning]
> The legal authorization checkbox on every target form is mandatory and creates an audit trail. Scanning an asset you do not own or have written permission to test can be illegal in most jurisdictions.
