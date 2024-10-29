---
description: ... or how to integrate tools that save their output to a file.
---

# Parsing output files

If your tool supports output as individual files, you can easily integrate it with `secator`.

* If you can set  the output file path in advance, read [#setting-the-file-path](parsing-output-files.md#setting-the-file-path "mention").
* If you cannot know, set, or guess the output file path in advance, read [#using-a-regular-expression-to-get-the-file-path](parsing-output-files.md#using-a-regular-expression-to-get-the-file-path "mention").

***

## Setting the file path

**Steps:**

* Set the file path before the command runs using the `on_init` hook
* Use the `on_cmd_done` hook to read the file and yield `secator` output types.

#### **Example:**

Assume `mytool` outputs to a JSON file like:

```bash
mytool -u mytarget.com -format json -o result.json
...
```

and the corresponding JSON would look like:

```json
[
  { "type": "url", "url": "http://mytarget.com", "status": 200 },
  { "type": "vulnerability", "target": "https://mytarget.com", "cve_id": "CVE-XXXX-XXXX", "name": "Bad vuln", "severity": "CRITICAL"},
]
```

An integration of `mytool` with `secator` would look like:

{% code title="secator/tasks/mytool.py" %}
```python
from secator.decorators import task
from secator.runners import Command
from secator.output_types import Url, Tag, Vulnerability
from secator.serializers import RegexSerializer
from secator.tasks._categories import Vuln

OUTPUT_REGEX = r'\[INF\] JSON report will be saved to (?P<output_path>)'


@task()
class mytool(Command):
  cmd = '/home/osboxes/.local/bin/mytool'
  input_flag = '-u'
  json_flag = '-format json'
  output_types = [Url, Vulnerability]

  # Set the output file path
  @staticmethod
  def on_init(self):
    self.output_path = self.get_opt_value(OUTPUT_PATH)
    if not self.output_path:
      self.output_path = f'{self.reports_folder}/.outputs/{self.unique_name}.json'
      self.cmd += f' -o {self.output_path}'

  # When the command completes, load the JSON file and yield secator output types
  @staticmethod
  def on_cmd_done(self):
    with open(self.output_path, 'r') as f:
      results = f.read()
    for r in results:
      if r['type'] == 'url':
        yield Url(
          url=r['url'],
          status_code=r['status'],
        )
      elif r['type'] == 'vulnerability':
        yield Vulnerability(
          id=r['cve_id'],
          name=r['name'],
          matched_at=r['target'],
          severity=r['severity'].lower()
        )
  
```
{% endcode %}

Run it with `secator`:

{% tabs %}
{% tab title="CLI" %}
```bash
$ secator x mytool mytarget.com

                         __            
   ________  _________ _/ /_____  _____
  / ___/ _ \/ ___/ __ `/ __/ __ \/ ___/
 (__  /  __/ /__/ /_/ / /_/ /_/ / /    
/____/\___/\___/\__,_/\__/\____/_/     v0.6.0

                        freelabz.com

No Celery worker alive.
/home/osboxes/.local/bin/mytool -u mytarget.com -format json -o <OUTPUT_FILE_PATH>
🔗 https://mytarget.com [200]
🚨 [Bad vuln 🡕] [critical] https://mytarget.com
```
{% endtab %}
{% endtabs %}

***

## Using a regular expression to get the file path

**Steps:**

* Use the `RegexSerializer` to read and set the output file path.
* Use the `on_cmd_done` hook to read the file and yield `secator` output types.

#### **Example:**

Assume `mytool` outputs to a JSON file like:

```bash
mytool -u mytarget.com -o json
[INF] JSON report will be saved to /path/to/custom/path.json
...
```

and the corresponding JSON would look like:

```json
[
  { "type": "url", "url": "http://mytarget.com", "status": 200 },
  { "type": "vulnerability", "target": "https://mytarget.com", "cve_id": "CVE-XXXX-XXXX", "description": "Bad vuln" },
]
```

First we need to find a named regular expression that will match the filename.

Here is the one we came up with:

{% code overflow="wrap" %}
```python
OUTPUT_REGEX = r'\[INF\] JSON report will be saved to (?P<output_path>)'
```
{% endcode %}

An integration of `mytool` with `secator` would look like:

{% code title="secator/tasks/mytool.py" %}
```python
from secator.decorators import task
from secator.runners import Command
from secator.output_types import Url, Tag, Vulnerability
from secator.serializers import RegexSerializer
from secator.tasks._categories import Vuln

OUTPUT_REGEX = r'\[INF\] JSON report will be saved to (?P<output_path>)'


@task()
class mytool(Command):
  cmd = '/home/osboxes/.local/bin/mytool'
  input_flag = '-u'
  json_flag = '-o json'
  output_types = [Url, Vulnerability]

  # Override the default item loader (JSONSerializer) with the RegexSerializer
  item_loaders = [
    RegexSerializer(
      OUTPUT_REGEX,
      fields=['output_path']
    )
  ]

  # React to items loaded by the RegexSerializer, and set the output path
  @staticmethod
  def on_regex_loaded(self, item):
    self.output_path = item['output_path']
    return

  # When the command completes, load the JSON file and yield secator output types
  @staticmethod
  def on_cmd_done(self):
    with open(self.output_path, 'r') as f:
      results = f.read()
    for r in results:
      if r['type'] == 'url':
        yield Url(
          url=r['url'],
          status_code=r['status'],
        )
      elif r['type'] == 'vulnerability':
        yield Vulnerability(
          id=r['cve_id'],
          name=r['name'],
          matched_at=r['target'],
          severity=r['severity'].lower()
        )

```
{% endcode %}

Run it with `secator`:

{% tabs %}
{% tab title="CLI" %}
```bash
$ secator x mytool mytarget.com

                         __            
   ________  _________ _/ /_____  _____
  / ___/ _ \/ ___/ __ `/ __/ __ \/ ___/
 (__  /  __/ /__/ /_/ / /_/ /_/ / /    
/____/\___/\___/\__,_/\__/\____/_/     v0.6.0

                        freelabz.com

No Celery worker alive.
/home/osboxes/.local/bin/mytool -u mytarget.com -o json
...
[INF] JSON report will be saved to /path/to/custom/path.json
🔗 https://mytarget.com [200]
🚨 [Bad vuln 🡕] [critical] https://mytarget.com
```
{% endtab %}

{% tab title="Python" %}
```python
from secator.tasks import mytool
task = mytool('mytarget.com')
for item in task:
    print(item)  # this will output Url, Vulnerability, or Tag items.

```
{% endtab %}
{% endtabs %}

***
