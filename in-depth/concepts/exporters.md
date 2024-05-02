---
description: ... or how to export reports to different destinations.
---

# Exporters

`secator` exporters allow exporting **reports** at the end of the run.

{% hint style="info" %}
To export **results** in **real-time**, see [drivers.md](drivers.md "mention") instead.
{% endhint %}

Available exporters out-of-the-box are:

* **`txt`**: exports results as TXT file.
* **`csv`**: exports results as CSV file.
* **`json`**: exports results as JSON file.
* **`gdrive`**: exports results to Google Drive. Set `addons.google.credentials_path` and `addons.google.drive_parent_folder_id` in your config for this exporter to work.
* **`table`**: prints results as a table in the terminal.

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
from secator.runners import Workflow
from secator.template import TemplateLoader

config = TemplateLoader(name='workflows/host_recon')
workflow = Workflow(config, exporters=['csv', 'json'])
workflow.run()
```
{% endtab %}
{% endtabs %}

