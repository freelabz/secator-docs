---
description: ... or how to export reports to different destinations.
---

# Exporters

`secator` exporters allow exporting **reports** at the end of the run.

{% hint style="info" %}
To export **results** in **real-time**, see [drivers.md](drivers.md "mention") instead.
{% endhint %}

Available exporters out-of-the-box are:

* **`txt`**: exports results as TXT files, one file per output type (`report_<type>.txt`).
* **`csv`**: exports results as CSV files, one file per output type (`report_<type>.csv`).
* **`json`**: exports results as a JSON file (`report.json`).
* **`jsonl`**: prints results as JSON lines to stdout, for piping to tools like `jq`.
* **`markdown`**: saves the reports written by the [ai-task.md](../ai-task.md "mention") as `report_ai.md` (does nothing for runs without AI output).
* **`table`**: prints results as a table in the terminal.
* **`gdrive`**: exports results to Google Drive. Install the `gdrive` addon and set `addons.gdrive.credentials_path` and `addons.gdrive.drive_parent_folder_id` in your config for this exporter to work.

Reports are saved to the runner's report folder (`~/.secator/reports/<workspace>/<tasks|workflows|scans>/<id>/`).

The default exporters are `csv`, `txt` and `markdown` (see `tasks.exporters`, `workflows.exporters` and `scans.exporters` in the [configuration-reference.md](../../getting-started/configuration-reference.md "mention")).

{% hint style="info" %}
`json` is no longer a default exporter: the `report.json` file of each run is written live by the [#json-driver](drivers.md#json-driver "mention"). Use `-o json` to also write the end-of-run JSON export.
{% endhint %}

***

## Using exporters

{% tabs %}
{% tab title="CLI" %}
To use exporters from the CLI, use the `--output` or `-o` flag:

```bash
secator x httpx mydomain.com -o txt
secator w host_recon mydomain.com -o gdrive,table
secator s url http://testphp.vulnweb.com -o csv,json
```
{% endtab %}

{% tab title="Python" %}
To use exporters from the library, you can pass the `exporters` kwarg to any runner:

```python
from secator.workflows import host_recon

host = 'mydomain.com'
workflow = host_recon(host, exporters=['csv', 'json'])
workflow.run()
```
{% endtab %}
{% endtabs %}

***

## Exporting existing reports

Exporters can also be used on past reports with `secator report show` and `secator query`:

```bash
secator r show tasks/3 -o csv -of /tmp/exports
secator q "vulnerability" -o jsonl | jq -r '.matched_at'
```

***

## Custom exporters

Drop a Python file defining an `Exporter` subclass in your templates folder (`~/.secator/templates/`). The exporter name is the class name without the `Exporter` suffix, lower-cased:

```python
# ~/.secator/templates/count_exporter.py
from secator.exporters._base import Exporter


class CountExporter(Exporter):
    def send(self):
        for output_type, items in self.report.data['results'].items():
            print(f'{output_type}: {len(items)}')
```

```bash
secator x httpx example.com -o count
```

***
