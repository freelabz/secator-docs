---
description: ... or how to organize and query your security assessment results.
---

# Reports & Workspaces

`secator` provides built-in features for organizing results into workspaces and querying reports with powerful filters.

***

## Workspaces

Workspaces help you organize scan results into separate folders. Each workspace is a directory under `~/.secator/reports/` where all results for that workspace are stored.

### Managing Workspaces

```bash
# List all workspaces
secator workspace list
secator ws list        # short alias

# Use a workspace (set as default)
secator workspace use myproject
secator ws use myproject

# Show current default workspace
secator workspace current
secator ws current
```

### Using Workspaces

{% tabs %}
{% tab title="CLI" %}
```bash
# Run a scan in a specific workspace
secator w host_recon example.com -ws myproject

# All results will be saved to ~/.secator/reports/myproject/
```
{% endtab %}

{% tab title="Library" %}
```python
from secator.workflows import host_recon

# Run in a specific workspace
results = host_recon(
    'example.com',
    context={'workspace_id': 'myproject'}
).run()
```
{% endtab %}
{% endtabs %}

### Workspace Structure

```
~/.secator/reports/
├── default/              # Default workspace
│   ├── task/
│   │   └── 001/
│   │       └── report.json
│   └── workflow/
│       └── 001/
│           └── report.json
├── myproject/            # Custom workspace
│   ├── scan/
│   │   └── 001/
│   │       └── report.json
│   └── workflow/
│       └── 002/
│           └── report.json
└── production/           # Another workspace
    └── ...
```

***

## Reports

### Listing Reports

```bash
# List all reports
secator report list
secator r list        # short alias

# Filter by workspace
secator r list -w myproject

# Filter by runner type
secator r list -r workflow
secator r list -r scan
secator r list -r task

# Filter by time (reports newer than)
secator r list -d 1d   # last day
secator r list -d 1h   # last hour
secator r list -d 7d   # last week

# Combine filters
secator r list -w myproject -r scan -d 7d
```

### Showing Report Contents

```bash
# Show a specific report (by path or fuzzy match)
secator report show /path/to/report.json
secator r show myproject/scan/001    # fuzzy match

# Show all reports in a workspace
secator r show -w myproject

# Export to different formats
secator r show -w myproject -o json
secator r show -w myproject -o csv
secator r show -w myproject -o markdown
secator r show -w myproject -o table
```

### Querying Reports

The `-q` / `--query` option allows filtering results using Python expressions:

```bash
# Find critical vulnerabilities
secator r show -w myproject -q "vulnerability.severity == 'critical'"

# Find open ports
secator r show -w myproject -q "port.state == 'open'"

# Find URLs with specific status codes
secator r show -w myproject -q "url.status_code == 200"

# Combine with OR (||)
secator r show -q "vulnerability.severity == 'critical' || vulnerability.severity == 'high'"

# Combine with AND (&&)
secator r show -q "port.port == 443 && port.state == 'open'"
```

### Query Syntax

The query syntax follows the pattern: `<output_type>.<field> <operator> <value>`

**Available output types:**
- `vulnerability`
- `subdomain`
- `url`
- `port`
- `ip`
- `domain`
- `tag`
- `exploit`
- `useraccount`
- `certificate`

**Examples:**

| Query | Description |
|-------|-------------|
| `vulnerability.severity == 'critical'` | Critical vulnerabilities |
| `port.port == 443` | Port 443 findings |
| `url.status_code >= 400` | URLs with error status |
| `subdomain.verified == True` | Verified subdomains |
| `tag.name == 'waf'` | WAF detections |

### Formatting Output

Use `-f` / `--format` to extract specific fields:

```bash
# Show only URLs
secator r show -w myproject -f url

# Show only URL and status code
secator r show -w myproject -f url.url,url.status_code

# Show vulnerability names and severity
secator r show -w myproject -f vulnerability.name,vulnerability.severity
```

### Unified Results

Use `-u` / `--unified` to merge and deduplicate results across multiple reports:

```bash
# Merge all reports in a workspace
secator r show -w myproject -u

# Merge specific reports
secator r show report1.json,report2.json -u

# Pipe report paths
secator r list -w myproject | secator r show -u
```

### Exporting Reports

```bash
# Export to JSON
secator report export /path/to/report.json -o json

# Export to CSV
secator report export /path/to/report.json -o csv

# Export to custom folder
secator report export /path/to/report.json -o json --output-folder /tmp/exports
```

***

## Report Command Reference

### `secator report list`

| Option | Short | Description |
|--------|-------|-------------|
| `--workspace` | `-w` | Filter by workspace name |
| `--runner-type` | `-r` | Filter by type: `task`, `workflow`, `scan` |
| `--time-delta` | `-d` | Keep reports newer than: `1h`, `1d`, `7d`, `1y` |

### `secator report show`

| Option | Short | Description |
|--------|-------|-------------|
| `--output` | `-o` | Export format: `console`, `json`, `csv`, `markdown`, `table` |
| `--workspace` | `-w` | Filter by workspace name |
| `--runner-type` | `-r` | Filter by type: `task`, `workflow`, `scan` |
| `--time-delta` | `-d` | Keep reports newer than delta |
| `--query` | `-q` | Python expression filter |
| `--format` | `-f` | Extract specific fields |
| `--unified` | `-u` | Merge and deduplicate results |

### `secator report export`

| Argument | Description |
|----------|-------------|
| `json_path` | Path to the report.json file |

| Option | Description |
|--------|-------------|
| `--output` | Export format(s): `json`, `csv`, `markdown` |
| `--output-folder` | Output directory (default: current directory) |

***

## Workspace Command Reference

### `secator workspace list`

Lists all workspaces with their run counts and paths.

### `secator workspace use <name>`

Sets the default workspace. All subsequent runs will save to this workspace unless overridden with `-ws`.

### `secator workspace current`

Shows the current default workspace name.

***

## Examples

### Security Assessment Workflow

```bash
# 1. Create and use a workspace for the project
secator ws use client-assessment-2024

# 2. Run scans (results saved to workspace)
secator s domain example.com
secator s url https://example.com

# 3. Query for critical findings
secator r show -q "vulnerability.severity == 'critical'"

# 4. Export findings for reporting
secator r show -u -o csv > critical-findings.csv

# 5. Generate markdown report
secator r show -u -o markdown > assessment-report.md
```

### Multi-Project Management

```bash
# Work on Project A
secator ws use project-a
secator w host_recon target-a.com

# Switch to Project B
secator ws use project-b
secator w host_recon target-b.com

# Query across all workspaces
secator r list  # shows all workspaces
secator r show -w project-a -q "port.state == 'open'"
secator r show -w project-b -q "port.state == 'open'"
```

***
