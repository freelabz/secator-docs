---
description: ... or how to route live results to a destination.
---

# Drivers

A driver is a set of hooks that constitute a full integration to route live results to certain destination.

Unlike hooks, you can use a driver from the CLI by using the `-driver` option. Several drivers can be combined with commas:

```bash
secator w host_recon example.com -driver mongodb,discord
```

To use drivers on every run, set them as defaults:

```bash
secator config set drivers.defaults mongodb
```

Available drivers:

| Driver    | Destination                                   | Addon                           | Queryable |
| --------- | --------------------------------------------- | ------------------------------- | --------- |
| `json`    | `report.json` file of each run (default)      | none                            | yes (`local` backend) |
| `mongodb` | MongoDB database                              | `secator install addons mongodb` | yes       |
| `sqlite`  | SQLite database file                          | none                            | yes       |
| `api`     | Any HTTP API implementing the expected routes | none                            | yes       |
| `gcs`     | Google Cloud Storage (files only)             | `secator install addons gcs`    | no        |
| `discord` | Discord channel (notifications)               | none                            | no        |

"Queryable" drivers are also **query backends**: `secator q`, `secator r` and `secator ws` can read results back from them with `--driver` (see [querying-results.md](../../getting-started/querying-results.md "mention")).

{% hint style="info" %}
When no database driver (`mongodb`, `sqlite` or `api`) is active, the `json` driver is enabled automatically, so every run is queryable. Pass `-driver local` to ignore the configured `drivers.defaults` for a single run.
{% endhint %}

***

## JSON driver

The `json` driver writes each runner's `report.json` (in its report folder) live, as results come in and as the runner status changes. Results can be queried while the run is still in progress:

```bash
secator w host_recon example.com -driver json
secator q "port" --driver local
```

This driver is enabled by default when no other database driver is active.

***

## MongoDB driver

To export live results to MongoDB database:

<pre class="language-bash"><code class="lang-bash"><strong>secator install addons mongodb
</strong>secator config set addons.mongodb.url mongodb://localhost
secator w host_recon example.com -driver mongodb
</code></pre>

Results will be added to the database in real-time as results come through from the various tools supported by `secator`.&#x20;

Runners are stored in the `tasks`, `workflows` and `scans` collections, and results (see [output-types.md](output-types.md "mention")) in the `findings` collection. Duplicate findings across runs of the same workspace are tagged automatically.

***

## SQLite driver

To store live results in a local SQLite database (no server needed):

```bash
secator w host_recon example.com -driver sqlite
secator q "vulnerability" --driver sqlite
```

The database file defaults to `~/.secator/secator.db`; change it with `addons.sqlite.path`. Runners are stored in the `tasks`, `workflows` and `scans` tables, and results in the `findings` table.

***

## API driver

The `api` driver sends runners and findings to an HTTP API as they are produced, and can query them back. It is meant to integrate `secator` with your own application:

```bash
secator config set addons.api.url https://myapp.example.com/api
secator config set addons.api.key <API_KEY>
secator w host_recon example.com -driver api
```

Requests are JSON, authenticated with an `Authorization: <header_name> <key>` header (`Bearer` by default). The driver uses the following routes, relative to `addons.api.url` (each one configurable with the matching `addons.api.*_endpoint` key):

| Action                 | Method | Default route               |
| ---------------------- | ------ | --------------------------- |
| Create a runner        | POST   | `runners`                   |
| Update a runner        | PUT    | `runner/{runner_id}`        |
| Create a finding       | POST   | `findings`                  |
| Update a finding       | PUT    | `finding/{finding_id}`      |
| Search findings        | POST   | `findings/_search`          |
| List / create workspaces | GET / POST | `workspaces`            |

See the `addons.api` section of the [configuration-reference.md](../../getting-started/configuration-reference.md "mention") for all routes and options.

***

## GCS driver

To upload files (screenshots and stored responses) from URL results to Google Cloud Storage:

<pre class="language-bash"><code class="lang-bash"><strong>secator install addons gcs
</strong>secator config set addons.gcs.bucket_name my-bucket-name
secator w host_recon example.com -driver gcs
</code></pre>

Files will be uploaded to Google Cloud Storage in real-time as results come through. The local file paths (`screenshot_path`, `stored_response_path`) in URL results will be replaced with GCS URLs (`gs://bucket-name/blob-name`).

{% hint style="info" %}
**Authentication**: The GCS driver uses the Google Cloud Storage client library which automatically detects credentials. You can authenticate using one of the following methods:

- Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to your credentials JSON file
- Use Application Default Credentials if running on Google Cloud Platform
- The client library will automatically detect credentials from your environment

The `addons.gcs.credentials_path` config option is available but optional, as the client library handles credential detection automatically.
{% endhint %}

{% hint style="info" %}
The `gcs` driver always runs before database drivers, so stored results already contain the GCS URLs.
{% endhint %}

***

## Discord driver

To send runner updates and findings to a Discord channel:

```bash
secator config set addons.discord.webhook_url https://discord.com/api/webhooks/<ID>/<TOKEN>
secator config set addons.discord.min_severity medium
secator w host_recon example.com -driver discord
```

By default, only `vulnerability` findings of severity `high` or above are sent (see `addons.discord.finding_types` and `addons.discord.min_severity`). If you also set `addons.discord.bot_token`, each runner gets its own thread, and its status message is edited in place.

***

## Custom drivers

You can write your own driver: drop a Python file defining a `HOOKS` dict in your templates folder (`~/.secator/templates/`). The file name becomes the driver name:

```python
# ~/.secator/templates/printer.py
from secator.runners import Task, Workflow, Scan


def on_item(self, item):
    print(f'[{self.name}] new {item._type}')
    return item


HOOKS = {
    Task: {'on_item': [on_item]},
    Workflow: {'on_item': [on_item]},
    Scan: {'on_item': [on_item]},
}
```

```bash
secator x httpx example.com -driver printer
```

{% hint style="info" %}
See [#lifecyle-hooks](runners.md#lifecyle-hooks "mention") for the list of available hooks.
{% endhint %}

***
