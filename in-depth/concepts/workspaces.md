---
description: ... or how to keep each engagement's results separate.
---

# Workspaces

A **workspace** is a named container for reports and findings. Every task, workflow and scan runs in a workspace, and every query reads from one. Use one workspace per engagement, client or project to keep their results apart.

When you don't choose one, `secator` uses the `default` workspace.

***

## How workspaces are stored

With the default `local` backend, each workspace is a folder in your reports directory:

```
~/.secator/reports/
├── default/
│   ├── tasks/
│   ├── workflows/
│   └── scans/
└── mydomain/
    ├── tasks/
    ├── workflows/
    └── scans/
```

See [querying-results.md](../../getting-started/querying-results.md "mention") for the full report layout.

With the `mongodb`, `sqlite` or `api` [drivers.md](drivers.md "mention"), the workspace is saved with each runner and finding, so queries on these backends are also scoped to a workspace.

***

## Running in a workspace

Pass `-ws` to any task, workflow or scan to run it in a workspace. If the workspace doesn't exist yet, it's created:

{% tabs %}
{% tab title="Task" %}
```bash
secator x httpx mydomain.com -ws mydomain
```
{% endtab %}

{% tab title="Workflow" %}
```bash
secator w host_recon mydomain.com -ws mydomain
```
{% endtab %}

{% tab title="Scan" %}
```bash
secator s domain mydomain.com -ws mydomain
```
{% endtab %}
{% endtabs %}

***

## Managing workspaces

The `secator workspace` command (or `secator ws`) manages workspaces.

### Switching the current workspace

`secator ws use <NAME>` sets the **current** workspace. Runs without `-ws`, and commands like `secator q` and `secator r show` without `-w`, then use it:

```bash
secator ws use mydomain
secator s domain mydomain.com      # runs in 'mydomain'
secator q vulnerability            # queries 'mydomain'
```

The workspace folder is created if it doesn't exist. `secator ws create <NAME>` is an alias of `use`.

The current workspace is stored in the `workspaces.current` config key, so this also works:

```bash
secator config set workspaces.current mydomain
```

{% hint style="info" %}
With the `api` driver (passed with `--driver api` or set in `drivers.defaults`), `secator ws use` also creates the workspace on the remote API if it doesn't exist.
{% endhint %}

### Showing the current workspace

```bash
secator ws current
```

### Listing workspaces

```bash
secator ws list
```

With the `local` backend, the table shows each workspace's name, number of runs and folder. With the `mongodb`, `sqlite` or `api` backend (`--driver` or `drivers.defaults`), it shows the name, id, description, run count and findings count.

### Deleting a workspace

`secator ws rm <NAME>` deletes a workspace and **all** its reports. It shows what will be deleted and asks for confirmation. Use `-y` / `--yes` to skip the prompt:

```bash
secator ws rm old-engagement
secator ws rm old-engagement -y --driver mongodb
```

With the `local` backend, the workspace folder is removed. With the `mongodb` or `sqlite` backend, the workspace's runners and findings are also deleted from the database. With the `api` backend, a delete request is sent to the API.

`secator ws remove` and `secator ws delete` are aliases of `rm`.

***

## Summarizing a workspace

`secator ws summary` prints an overview of the findings in a workspace:

```bash
secator ws summary                 # current workspace
secator ws summary -w mydomain
```

The built-in summary shows:

* the top ports, hosts (IPs), subdomains, technologies and URLs,
* unique vulnerabilities by severity and by status,
* the top vulnerabilities, ranked by number of targets hit.

Use `--driver` to read from another backend, e.g. `secator ws summary -w mydomain --driver mongodb`.

### Custom summary templates

The summary is a [Jinja2](https://jinja.palletsprojects.com/) template. Use `--template` to render your own:

```bash
secator ws summary -w mydomain --template ./my_summary.j2
```

In the template, `workspace` is the workspace name, and `query(...)` (or its alias `q(...)`) runs a query and returns its output as text, one row per line. It takes the same options as [`secator q`](../../getting-started/querying-results.md#querying-with-secator-query):

```
query(type_or_expression, fmt=None, count=False, uniq=False, sort=None, limit=0, group=False)
```

For example:

{% code title="my_summary.j2" %}
```jinja
[bold]Summary for {{ workspace }}[/]

[bold cyan]Top 10 open ports[/]
{{ query("port.state == 'open'", fmt='port', count=True, limit=10) }}

[bold cyan]Web servers[/]
{{ query('technology', fmt='{product}/{version}', uniq=True) }}

[bold red]Critical and high vulnerabilities[/]
{{ query('vulnerability.severity_nb < 2', group=True, fmt='{vulnerability.name}: {vulnerability.matched_at}') }}
```
{% endcode %}

You can use [Rich markup](https://rich.readthedocs.io/en/stable/markup.html) like `[bold]...[/]` for styling. A query with no results renders as `(none)`.

***

## Routing targets to workspaces

You can send runs to a workspace **automatically**, based on their targets. Set `workspaces.routes.<workspace>` to a list of glob patterns:

```bash
secator config set --append workspaces.routes.acme '*acme.com*'
secator config set --append workspaces.routes.acme '10.10.*'
```

A run without `-ws` whose target matches one of the patterns runs in the `acme` workspace:

```bash
secator x httpx https://www.acme.com     # runs in 'acme'
secator x httpx https://example.com      # runs in the current workspace
```

Patterns use shell-style wildcards (`*`, `?`, `[...]`) and must match the **whole** target string, so add `*` on both sides to match part of a URL. Routes are checked in the order they appear in your config, and the first match wins.

{% hint style="warning" %}
Known limitation: when the workspace comes from a route or from a profile (rather than `-ws` or `secator ws use`), the run's local report files are currently still written under the current workspace folder, and the `workspaces.profiles` of that workspace are not applied. Pass `-ws` explicitly if you rely on either.
{% endhint %}

***

## Default profiles per workspace

You can apply [profiles.md](profiles.md "mention") automatically to every run in a given workspace with `workspaces.profiles.<workspace>`:

```bash
secator config set workspaces.profiles.acme-external passive,polite   # set the profiles
secator config set workspaces.profiles.acme-external stealth --append # add one
secator config unset workspaces.profiles.acme-external                # remove them
```

These profiles are added to the global `profiles.defaults` and to any profiles passed with `-pf`.

Here, every run in the `acme-external` workspace is passive and polite:

```bash
secator s domain example.com -ws acme-external
```

***

## Setting the workspace in a profile

A custom profile can also choose the workspace, with the `workspace` key:

{% code title="~/.secator/templates/profiles/acme.yaml" %}
```yaml
type: profile
name: acme
description: "ACME engagement"
workspace: acme
opts:
  rate_limit: 50
```
{% endcode %}

```bash
secator s host www.acme.com -pf acme    # runs in 'acme'
```

{% hint style="info" %}
See the known limitation in [#routing-targets-to-workspaces](workspaces.md#routing-targets-to-workspaces "mention").
{% endhint %}

***

## How the workspace is chosen

When a run starts, its workspace is picked in this order:

1. The `workspace` of an **enforced** profile (`enforce: true`).
2. The `-ws` option.
3. The `workspace` of a non-enforced profile.
4. The first `workspaces.routes` pattern that matches a target.
5. The current workspace (`workspaces.current`, set with `secator ws use`).
6. `default`.

***

## Example: one workspace per engagement

```bash
# Start a new engagement
secator ws use acme
secator config set workspaces.profiles.acme polite

# Run recon (saved to the 'acme' workspace)
secator s domain acme.com
secator s host 10.10.0.0/24

# Review the results
secator r list -w acme
secator ws summary
secator q "vulnerability.severity in [critical, high]" -f "{vulnerability.matched_at}"

# Clean up when the engagement is over
secator ws rm acme
```
