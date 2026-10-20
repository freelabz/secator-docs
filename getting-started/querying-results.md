---
description: ... or how to find, filter and reuse everything secator has found.
---

# Querying results & reports

Every task, workflow and scan you run with `secator` is saved as a **report**. You can then list them, inspect them, and query findings across all of them, without running anything again.

This page covers the `secator report` (`secator r`) and `secator query` (`secator q`) commands.

***

## Where reports are stored

By default, reports are saved under `~/.secator/reports/`, grouped by [workspaces.md](../in-depth/concepts/workspaces.md "mention") and then by runner type:

```
~/.secator/reports/
└── <workspace>/
    ├── tasks/
    │   ├── 0/
    │   │   ├── report.json        # runner info + results
    │   │   ├── report_url.csv     # exporter outputs (one file per output type)
    │   │   ├── report_url.txt
    │   │   ├── .inputs/           # input files passed to the tools
    │   │   └── .outputs/          # raw tool outputs (screenshots, responses...)
    │   └── 1/
    ├── workflows/
    │   └── 0/
    └── scans/
        └── 0/
```

Each run gets the next free number in its folder. A report is referred to by its **runner path**, `<type>/<id>`, for example `tasks/0`, `workflows/3` or `scans/12`. All commands below use this format.

{% hint style="info" %}
The reports folder follows the `dirs.data` setting. Set `SECATOR_DIRS_DATA=/path/to/folder` to use a different data folder, e.g. one per engagement. See [configuration.md](configuration.md "mention").
{% endhint %}

***

## Listing reports

Use `secator report list` (or `secator r list`) to list your reports:

```bash
secator r list
```

The table shows the workspace, runner name, runner path (`Id`), targets, profiles, start / end dates, elapsed time, status, and vulnerability counts by severity.

Without `-w`, reports from **all** workspaces are listed. Use these options to narrow the list:

| Option | Description |
| --- | --- |
| `-w`, `-ws`, `--workspace` | Only list reports from this workspace. |
| `-r`, `--runner-type` | Only list one runner type: `task`, `workflow` or `scan`. |
| `-d`, `--time-delta` | Only list reports newer than a time delta, e.g. `26m`, `1d`, `1y`. |
| `--status` | Filter by runner status, as a case-insensitive regex, e.g. `SUCCESS`, `FAIL`, `'(RUNNING\|FAILURE)'`. |
| `-i`, `--interesting` | Only list reports that have vulnerabilities. |
| `--show-children` | Also list nested sub-tasks / sub-workflows. By default, only outermost runners are shown. |
| `--show-all` | Show all columns, including the report path. |
| `--driver` | Query backend to read from: `local`, `mongodb`, `api` or `sqlite` (see [#query-backends](querying-results.md#query-backends "mention")). |

{% tabs %}
{% tab title="Recent scans" %}
List the scans run in the `mydomain` workspace in the last two days:

```bash
secator r list -w mydomain -r scan -d 2d
```
{% endtab %}

{% tab title="Failed runs" %}
List runs that failed or are still running:

```bash
secator r list --status '(RUNNING|FAILURE)'
```
{% endtab %}

{% tab title="With vulnerabilities" %}
List only reports that found vulnerabilities, with their paths on disk:

```bash
secator r list -i --show-all
```
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
`-i` and `-d` only work with the `local` driver. `--show-children` only has an effect with the `mongodb` and `api` drivers, because local reports don't store sub-runners separately.
{% endhint %}

***

## Inspecting a report

`secator report info <RUNNER_PATH>` shows the metadata of one run: name, targets, options, status, timings, context, plus its errors and warnings.

```bash
secator r info scans/0
secator r info tasks/12 -w mydomain
```

By default, long lists are truncated, the verbose `config` and `output` fields are hidden, and only the last error / warning is shown. Use `--show-all` to see everything:

```bash
secator r info scans/0 --show-all
```

***

## Showing report results

`secator report show` prints the results of one or more reports. Pass runner paths as a comma-separated `REPORT_QUERY`:

```bash
secator r show tasks/0                 # results of task 0
secator r show scans/5,tasks/3         # results of scan 5 and task 3
secator r show -w mydomain             # all results from the 'mydomain' workspace
secator r show                         # all results from the current workspace
```

Without `-w`, the current workspace is used (see [workspaces.md](../in-depth/concepts/workspaces.md "mention")).

{% hint style="info" %}
`target` and `ai` results are hidden by default because they are verbose. To see them, query their type explicitly, e.g. `-q target`.
{% endhint %}

### Filtering with `-q`

Use `-q` / `--query` to filter results with an expression (see [#query-syntax](querying-results.md#query-syntax "mention")):

```bash
secator r show scans/5 -q "port.state == 'open'"
secator r show -q "vulnerability.severity in [critical, high]"
```

### Formatting with `-f`

Use `-f` / `--format` to print only the fields you need, one line per finding. This works well for piping into other tools.

{% tabs %}
{% tab title="Braces" %}
Use `{type.field}` placeholders to build a line from several fields:

```bash
secator r show -q port -f "{port.host}:{port.port}"
secator r show -q url -f "{url.url} [{url.status_code}]"
```

When the results contain a single output type, you can drop the type prefix:

```bash
secator r show -q url -f "{url} {status_code} {title}"
```
{% endtab %}

{% tab title="Dot-path" %}
Use `type.field` (no braces) to print a single field:

```bash
secator r show -q vulnerability -f vulnerability.matched_at
```

Nested fields work too, e.g. for values stored in `extra_data`:

```bash
secator r show -q tag -f extra_data.value
```
{% endtab %}

{% tab title="Several types" %}
Separate one format per output type with `||`. Each finding is formatted with the spec that matches its type:

```bash
secator r show scans/5 -f "{port.host}:{port.port} || vulnerability.matched_at"
```
{% endtab %}

{% tab title="Template file" %}
`-f` also accepts a path to a file containing the format. `\n` and `\t` are expanded:

```bash
echo '{url.url}\n  title: {url.title}' > url.fmt
secator r show -q url -f url.fmt
```
{% endtab %}
{% endtabs %}

{% hint style="warning" %}
`-f` only works with the `console` exporter. It can't be combined with `-o json`, `-o csv`, and so on.
{% endhint %}

### Sorting, counting and grouping

These options reshape the output after the query runs:

| Option | Description |
| --- | --- |
| `-l`, `--limit` | Limit the number of results (`0` = no limit). |
| `--sort <field>` | Sort by a field, numeric-aware. Prefix the field with `-` to sort in descending order, e.g. `--sort port` or `--sort -cvss_score`. |
| `--uniq` | Drop duplicate `--format` values. |
| `--count` | Group identical `--format` values and prefix each one with its number of occurrences, most frequent first. With `--sort`, values are ordered by value instead. |
| `--group` | Group findings by their output type's default field(s) and list the related values on one row (see below). |

{% tabs %}
{% tab title="Top ports" %}
```bash
secator r show -q port -f port --count -l 15
```
{% endtab %}

{% tab title="Unique hosts" %}
```bash
secator r show -q url -f host --uniq
```
{% endtab %}

{% tab title="Riskiest vulns first" %}
```bash
secator r show -q vulnerability --sort -cvss_score -l 20
```
{% endtab %}

{% tab title="Grouped vulnerabilities" %}
Show each vulnerability once, with all the targets it was matched at:

```bash
secator r show -q vulnerability --group
```
{% endtab %}
{% endtabs %}

The default `--group` fields are:

| Output type | Grouped by | Values listed |
| --- | --- | --- |
| `vulnerability` | `name` | `matched_at` |
| `exploit` | `name` | `matched_at` |
| `port` | `host` | `port` |
| `url` | `host` | `url` |
| `subdomain` | `domain` | `host` |
| `technology` | `product` | `match` |
| `tag` | `category`, `name` | `match` |

`--group` can be combined with `--format`, `--count` and `--sort`. For example, `-q vulnerability --group -f severity --count` counts **unique** vulnerabilities by severity.

### Exporting

Use `-o` / `--output` to export the results with one or more [exporters.md](../in-depth/concepts/exporters.md "mention"), and `-of` / `--output-folder` to choose where the files go (the current directory by default):

```bash
secator r show scans/5 -o json,csv -of ./exports
```

### Deduplication

`--dedupe` removes duplicate findings, e.g. the same URL found by several tools or runs. `--no-dedupe` keeps them. When neither is passed, `secator` uses the `runners.remove_duplicates` setting:

```bash
secator r show -w mydomain --dedupe
secator config set runners.remove_duplicates true   # dedupe by default
```

### Time filter

Use `-d` / `--time-delta` to keep only recent findings:

```bash
secator r show -w mydomain -q vulnerability -d 1d
```

***

## Querying with `secator query`

`secator query` (or `secator q`) is the quickest way to search for findings. It accepts the same options as `secator r show`, but takes the filter expression as its argument:

```bash
secator q "vulnerability.severity == 'critical'"
secator q url -f "{url} {status_code}"
secator q "port.state == 'open'" -w mydomain
```

To scope a query to specific runs, use `-rf` / `--report-filter`. It works like the `REPORT_QUERY` argument of `r show`:

```bash
secator q "port.state == 'open'" -rf scans/23,tasks/10
```

With no argument, `secator q` returns all results, filtered by the options you pass:

```bash
secator q -rf scans/23 -o json
```

### How the argument is read

`secator q <ARG>` reads its argument in this order:

1. **Saved query.** If `ARG` is the name of a saved query, its expression is used (see [#saved-queries](querying-results.md#saved-queries "mention")).
2. **Filter expression.** If `ARG` looks like an expression (it contains an operator such as `==`, `<`, `~=`, `&&`, `||` or `in [`, is a dotted field path like `ip.alive`, or is an output type name like `url`), it is run as a query.
3. **Natural language.** Otherwise, the question is sent to the `ai` task in chat mode, run against the selected workspace:

```bash
secator q "Which hosts expose an admin panel?"
# same as: secator x ai --mode chat -p "Which hosts expose an admin panel?"
```

{% hint style="info" %}
The natural-language mode needs the `ai` task to be set up. Only `-w` / `--workspace` is used in this mode.
{% endhint %}

### Saved queries

Save a query under a name with `--save`, then run it by name:

```bash
secator q "vulnerability.severity in [critical, high] && vulnerability.confidence == 'high'" --save vuln_high
secator q vuln_high -f "{vulnerability.matched_at}" -w mydomain
```

Saved queries are stored in the `queries` section of your config, so you can also manage them with `secator config`:

```bash
secator config set queries.kev "vulnerability.tags ~= 'kev'"   # save a query
secator config get queries                                      # list saved queries
```

***

## Query syntax

`-q` (for `r show`) and the argument of `secator q` use the same expression syntax.

### Selecting a type

Use an output type name on its own to select all findings of that type:

```bash
secator q vulnerability
secator q url
```

See [output-types.md](../in-depth/concepts/output-types.md "mention") for the list of types. To filter on a field, use `type.field`:

```bash
secator q "url.status_code == 200"
```

### Operators

| Operator | Meaning | Example |
| --- | --- | --- |
| `==` | Equals | `port.port == 443` |
| `!=` | Not equal | `url.status_code != 404` |
| `>`, `>=`, `<`, `<=` | Numeric comparison | `vulnerability.cvss_score >= 7` |
| `~=` | Matches regex (case-insensitive) | `url.url ~= 'admin'` |
| `!~=` | Doesn't match regex (case-insensitive) | `subdomain.host !~= '^dev'` |
| `in [...]` | Value is in list | `port.port in [22, 80, 443]` |
| `not in [...]` | Value is not in list | `vulnerability.severity not in [info, low]` |
| `type.field` | Field is truthy | `ip.alive` |
| `not type.field` | Field is not `True` | `not url.verified` |

Values can be quoted or not. `true` / `false` become booleans, and numbers become numbers. Nested fields use dots, e.g. `vulnerability.extra_data.template_id ~= 'cve'`.

`!=`, `!~=` and `not in` only match findings that **have** the field: `vulnerability.severity != 'info'` doesn't return ports or URLs.

### Combining conditions

Combine conditions with `&&` / `and` (all must match) or `||` / `or` (any can match):

```bash
secator q "vulnerability.severity == 'critical' && vulnerability.tags ~= 'exploitable'"
secator q "port.port == 22 || port.port == 3389"
```

{% hint style="warning" %}
You can't mix `&&` and `||` in the same expression.
{% endhint %}

### MongoDB JSON

You can also pass a MongoDB-style JSON filter:

```bash
secator r show -q '{"_type": "port", "port": {"$in": [80, 443]}}'
```

### Unknown fields

If a field doesn't exist on the type you query, `secator` prints a warning with the list of available fields, so you can use a typo as a quick field reference:

```bash
secator q "port.foo == 1"
# [WRN] Field 'foo' does not exist on type 'port'. Available fields: confidence, cpes, extra_data, host, ip, ...
```

{% hint style="info" %}
Findings marked as **false positives** are always hidden from query results.
{% endhint %}

### Examples

```bash
# Known-exploited (KEV) vulnerabilities with high confidence
secator q "vulnerability.tags ~= 'kev' && vulnerability.confidence == 'high'"

# Critical and high vulnerabilities (severity_nb: 0 = critical, 1 = high, ...)
secator q "vulnerability.severity_nb < 2"

# Exploits found for a given CVE
secator q "exploit.cves ~= 'CVE-2021-44228'"

# Top 15 open ports, services and technologies
secator q "port.state == 'open'" -f port --count -l 15
secator q port -f service_name --count -l 15
secator q technology -f "{product}/{version}" --count -l 15

# Live URLs, ready to pipe into another tool
secator q "url.status_code == 200" -f url --uniq | secator x nuclei
```

***

## Query backends

All `secator r` and `secator q` commands read from a **query backend**, selected with `--driver`:

| Driver | Reads from |
| --- | --- |
| `local` | The JSON reports in `~/.secator/reports/` (default). |
| `mongodb` | A MongoDB database filled by the `mongodb` driver. |
| `sqlite` | A SQLite database filled by the `sqlite` driver. |
| `api` | A remote API filled by the `api` driver. |

If `--driver` isn't set, `secator` uses the first backend listed in `drivers.defaults`, and falls back to `local`:

```bash
secator x httpx example.com -driver mongodb       # store results in MongoDB
secator q url --driver mongodb                    # query them
secator config set drivers.defaults mongodb       # ... or use MongoDB by default
```

See [drivers.md](../in-depth/concepts/drivers.md "mention") to set drivers up.

***

## Deleting reports

`secator report delete` (or `secator r rm`) deletes one or more reports. It accepts space- or comma-separated runner paths, and numeric ranges:

```bash
secator r delete tasks/23 tasks/24 workflows/21
secator r delete tasks/23,workflows/21
secator r delete tasks/136-140,workflows/10-21 -w mydomain
```

The command lists what will be deleted and asks for confirmation. Pass `-y` / `--yes` to skip the prompt.

With the `local` driver, the report folders are removed. With the `mongodb`, `sqlite` or `api` drivers, the runner and its findings are deleted from the backend.

To delete a whole workspace and all its reports, use `secator ws rm` (see [workspaces.md](../in-depth/concepts/workspaces.md "mention")).
