---
description: >-
  Search, filter and export findings across your workspace with the
  `secator query` command and its Python-like filter language.
---

# Querying results

`secator query` (alias `secator q`) is a single entry point for pulling findings back out
of your workspace. It runs a **filter expression** against every result secator has stored,
consolidates the matches into a report, and prints (or exports) them.

It is the query-first sibling of [`secator report show`](../getting-started/reports-and-workspaces.md#querying-reports):
both share the exact same filter language and backends, but `query` adds three conveniences:

- **saved queries** — name a filter once, replay it forever (`secator q vuln_high`)
- **smart dispatch** — a bare finding type, a filter expression, a saved name, or plain
  English are all accepted as the single argument and routed automatically
- **natural-language fallback** — anything that is not a filter or a saved name is handed to
  the [AI assistant](../getting-started/ai-assistant.md) as a chat prompt

```bash
# Filter expression
secator q "vulnerability.severity == 'critical'"

# Bare finding type (all URLs in the current workspace)
secator q url

# Saved query by name
secator q vuln_high

# Natural language -> AI chat
secator q "what are the most exposed hosts?"
```

## How the argument is interpreted

`query` takes a single positional argument and decides what to do with it, in this order:

1. **`--save <name>` present** → the argument is stored as a named query, nothing is run.
2. **No argument** → return *all* findings in the workspace (optionally scoped by
   `--workspace` / `--report-filter`).
3. **Argument matches a saved query name** → the saved expression is run.
4. **Argument looks like a filter expression** → it is parsed and run as a filter.
5. **Otherwise** → the argument is treated as natural language and sent to the AI assistant.

An argument "looks like a filter expression" when it contains a comparison or logical
operator (`==`, `!=`, `<`, `>`, `<=`, `>=`, `~=`, `!~=`, `&&`, `||`), the `in [ ... ]`
list operator, a dotted `type.field` path, or is simply a bare known output-type name
(`url`, `vulnerability`, `port`, …). The bare words `and` / `or` on their own are **not**
enough — they only ever join comparison clauses, which are already detected, so a prompt
like `"subdomains and ips"` correctly falls through to the AI assistant.

{% hint style="info" %}
The same filter language is available on `secator report show -q "<expr>"`. Use `query` when
you want the smart dispatch, saved queries, or the natural-language fallback; use
`report show` when you are already reasoning in terms of a specific report.
{% endhint %}

## The filter language

A filter follows the pattern:

```
<type>.<field> <operator> <value>
```

- `<type>` is an output-type name (`vulnerability`, `url`, `port`, `ip`, `subdomain`,
  `domain`, `tag`, `exploit`, `certificate`, `technology`, `user_account`, `record`).
- `<field>` is any field on that type (see [Output types](concepts/output-types.md)).
- `<value>` is a string, number or boolean. Strings may be quoted with `'` or `"`;
  `true`/`false` become real booleans and numeric literals become `int`/`float`.

The type prefix is optional — a bare `field` (or the neutral `item.field`) matches the
field regardless of type. But adding the prefix both scopes the match and enables field
validation (see below).

### Operators

| Operator        | Meaning                              | Example |
| --------------- | ------------------------------------ | ------- |
| `==`            | equals                               | `url.status_code == 200` |
| `!=`            | not equals                           | `port.state != 'closed'` |
| `>` `>=` `<` `<=` | numeric / lexical comparison       | `vulnerability.cvss_score >= 7` |
| `~=`            | regex match (case-insensitive)       | `url.title ~= admin` |
| `!~=`           | negated regex (does NOT match)       | `url.url !~= '\.png$'` |
| `in [ ... ]`    | value is in the list                 | `vulnerability.severity in [critical, high]` |
| `not in [ ... ]`| value is not in the list             | `port.port not in [80, 443]` |
| `&&` / `and`    | logical AND                          | `port.port == 443 && port.state == 'open'` |
| `\|\|` / `or`   | logical OR                           | `vulnerability.severity == 'critical' \|\| vulnerability.severity == 'high'` |

Additional shorthands:

- **Type only** — a bare type name returns every finding of that type: `secator q vulnerability`.
- **Truthiness** — a bare `type.field` keeps findings where the field is truthy (non-empty,
  non-zero, not `false`, present): `secator q ip.alive`, `secator q vulnerability.verified`.
- **Negated truthiness** — `not type.field` keeps findings where the field is falsy, null or
  absent: `secator q "not url.verified"`.
- **Raw MongoDB JSON** — an argument starting with `{` is parsed as a MongoDB-style query
  dict and used verbatim: `secator q '{"_type": "port", "port": {"$gt": 1024}}'`.

{% hint style="warning" %}
You cannot mix `&&` and `||` in the same expression — split it into two queries, use an
`in [ ... ]` list, or drop to raw MongoDB JSON for complex boolean logic.
{% endhint %}

Regex operators (`~=` / `!~=`) are always applied **case-insensitively** (an implicit
`(?i)` is prepended) and the pattern stays a string, so standard regex syntax works across
all backends.

### Field validation

When a filter names a known `type`, the queried fields are validated against that type's
schema. An unknown field is dropped and a warning is printed listing the valid fields, e.g.:

```bash
secator q "vulnerability.svrity == 'critical'"
# Warning: Field 'svrity' does not exist on type 'vulnerability'.
# Available fields: confidence, cvss_score, description, epss_score, id, matched_at,
# name, provider, references, remediation, severity, status, verified, ...
```

If *every* field in a fragment is invalid the fragment is dropped entirely, so a typo does
not silently degrade into "match all vulnerabilities".

### Default type exclusions

Unless your query explicitly constrains a type, the verbose `target` and `ai` result types
are hidden from the output. Query them explicitly (`secator q target`, `secator q ai`) to
see them.

## Scoping the query

Beyond the filter expression itself, several options narrow *where* secator looks:

- **`-w` / `--workspace <name>`** — query a specific workspace (defaults to the current one).
- **`-rf` / `--report-filter <paths>`** — restrict the query to specific runner paths, e.g.
  `scans/5`, `tasks/3`, or a comma-separated list `scans/5,tasks/3`. This is the same
  `REPORT_QUERY` accepted positionally by `report show`.
- **`-d` / `--time-delta <delta>`** — keep only results newer than a relative time, e.g.
  `26m`, `1d`, `1y`.
- **`-l` / `--limit <n>`** — cap the number of results (`0` = no limit).
- **`--dedupe` / `--no-dedupe`** — toggle deduplication (defaults to the
  `runners.remove_duplicates` config value).

```bash
# Critical vulns found in the last day, inside scan 5, in the "acme" workspace
secator q "vulnerability.severity == 'critical'" -w acme -rf scans/5 -d 1d
```

## Output and formatting

By default results are printed to the console. Use exporters and format strings to change
that:

- **`-o` / `--output <exporters>`** — comma-separated exporters (`console`, `table`, `json`,
  `csv`, `txt`, …). See [Exporters](concepts/exporters.md).
- **`-of` / `--output-folder <dir>`** — where exported files are written (defaults to the
  current directory).
- **`-f` / `--format <spec>`** — a format string applied to each result (console only).

The `--format` spec uses `{type.field}` placeholders and supports several styles:

```bash
# One line per URL: "host:status"
secator q url -f '{url.host}:{url.status_code}'

# Per-type templates separated by ||
secator q "port || url" -f '{port.host}:{port.port} || {url.url}'

# Nested field access (dotted) into extra_data
secator q vulnerability -f '{vulnerability.matched_at} {extra_data.cve_id}'

# Bare field name when a single type is in the result set
secator q subdomain -f '{host}'
```

`\n` and `\t` in the format string are unescaped, and if the spec is a path to an existing
file, the template is loaded from that file. `--format` is console-only — combining it with
any file exporter raises an error.

## Saved queries

Save a filter once and replay it by name. Saved queries live in your secator config under
`queries.<name>`:

```bash
# Save
secator q "vulnerability.severity in [critical, high]" --save vuln_high
# 🎉 Saved query "vuln_high". Run it with: secator q vuln_high

# Replay (any time, any workspace)
secator q vuln_high
secator q vuln_high -w acme -d 7d -o csv
```

A saved name is resolved *before* the expression heuristics, so pick names that are not also
valid bare type names (don't name a query `url`).

## Query backends (drivers)

Queries run against whichever backend is active. Select one with `--driver`, otherwise the
first configured driver in `drivers.defaults` that has a query backend is used (falling back
to the local filesystem):

| Driver     | Backend                                             |
| ---------- | --------------------------------------------------- |
| `local`    | JSON reports on disk (default)                      |
| `mongodb`  | MongoDB collection                                  |
| `sqlite`   | SQLite database                                     |
| `api`      | Remote secator API                                  |

```bash
secator q "port.state == 'open'" --driver mongodb
```

See [Drivers](concepts/drivers.md) for how to configure each backend.

## Library usage

The engine behind the command is `secator.query.QueryEngine`. It exposes `search`,
`iterate`, `count` and `update`, and picks a backend from the context drivers (defaulting to
the local JSON backend).

```python
from secator.query import QueryEngine
from secator.query.utils import python_expr_to_mongo

# Translate a CLI-style expression into a MongoDB-style query dict
query = python_expr_to_mongo("vulnerability.severity in [critical, high]")
# -> {'_type': 'vulnerability', 'severity': {'$in': ['critical', 'high']}}

engine = QueryEngine(
    workspace_id='default',
    context={'workspace_name': 'default', 'drivers': []},  # [] -> local JSON backend
)

# One-shot search
results = engine.search(query, limit=50, dedupe=True)

# Stream large result sets in batches (never materializes all N at once)
for finding in engine.iterate(query, batch_size=1000):
    print(finding['_type'], finding.get('matched_at'))

# Count without fetching
n = engine.count(query)
```

You can also build the MongoDB-style dict yourself and skip `python_expr_to_mongo`
entirely — `search` / `count` / `iterate` accept any MongoDB-style query dict.

{% hint style="info" %}
Field names in library queries are the same as in the CLI, plus the internal `_type` key to
constrain the output type (`{'_type': 'url', 'status_code': 200}`).
{% endhint %}
