# Exporters

`secator` exporters allow exporting runner results **at the end of the run**.

{% hint style="info" %}
To export results in **real-time**, see [hooks-and-drivers.md](hooks-and-drivers.md "mention") instead.
{% endhint %}

Available exporters out-of-the-box are:

* **`txt`**: exports results as TXT file.
* **`csv`**: exports results as CSV file.
* **`json`**: exports results as JSON file.
* **`gdrive`**: exports results to Google Drive.\
  _You need to set `GOOGLE_CREDENTIALS_PATH` and `GOOGLE_DRIVE_PARENT_FOLDER_ID` for this exporter to work._
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
from secator.exporters import GdriveExporter,CSVExporter,JSONExporter
from secator.runners import Workflow

config = ConfigLoader(name='workflows/host_recon')
workflow = Workflow(config, exporters=[CSVExporter, JSONExporter])
workflow.run()
```
{% endtab %}
{% endtabs %}
