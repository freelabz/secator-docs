---
description: ... or how to integrate a command without JSON output.
---

# Example: integrating ls

This section will present a relatively simple (but complete) use case of integrating a **real-world** command into `secator`.

We picked the `ls` command because:

* It is relatively simple.
* It has no JSON output (we will need to fabricate it).
* It has no direct secator output type mapping.

***

## Writing the task file

Start by creating a file named `ls.py`:

{% code title="ls.py" %}
```python
from secator.runners import Command
from secator.decorators import task

@task()
class ls(Command):
    cmd = 'ls'
```
{% endcode %}

Move this file over to `~/.secator/templates/` (if you modified the default `dirs.templates`, move it to the corresponding location instead).

You can test the initial implementation like so:

<pre class="language-bash"><code class="lang-bash"><strong>$ secator x ls .
</strong>ls .
ls.py
__pycache__
tasks
🗄 Saved JSON report to ~/.secator/reports/default/tasks/94/report.json
🗄 Saved CSV reports to ~/.secator/reports/default/tasks/94/report_target.csv
</code></pre>

Okay, this works !&#x20;

{% hint style="warning" %}
<mark style="color:red;">**YES**</mark><mark style="color:red;">, but we don't have enough details in the results !</mark>
{% endhint %}

***

## Getting detailed output

To add more details to the results, we should add more beef to the ls command, let's try with `ls -al` instead as the default `cmd` instead:

{% code title="~/.secator/templates/ls.py" %}
```python
from secator.runners import Command
from secator.decorators import task

@task()
class ls(Command):
    cmd = 'ls -al'
```
{% endcode %}

and the output:

```bash
$ secator x ls .
ls -al .
total 16
drwxr-xr-x 3 osboxes osboxes 4096 May  2 04:50 .
drwxr-xr-x 4 osboxes osboxes 4096 May  2 04:49 ..
-rw-r--r-- 1 osboxes osboxes  119 May  2 04:51 ls.py
drwxr-xr-x 2 osboxes osboxes 4096 May  2 04:51 __pycache__
🗄 Saved JSON report to ~/.secator/reports/default/tasks/1/report.json
🗄 Saved CSV reports to ~/.secator/reports/default/tasks/1/report_target.csv
```

Okay, this gives more information already !

{% hint style="warning" %}
<mark style="color:red;">**YES**</mark><mark style="color:red;">, but we don't have any structured output ! I can't use -json and pipe the results to my super awesome CLI tool ...</mark>
{% endhint %}

***

## Adding JSON output

For this step we need to parse the `ls` command line text output by writing the `item_loader`  method.

The `item_loader` method takes a **line** as input and yield the **desired structured output** (dict).

Here is how to implement it for the `ls` command:

{% code title="~/.secator/templates/ls.py" %}
```python
from secator.runners import Command
from secator.decorators import task


@task()
class ls(Command):
    cmd = 'ls -al'

    @staticmethod
    def item_loader(self, line):
        fields = ['permissions', 'link_count', 'owner', 'group', 'size', 'month', 'day', 'hour', 'path']
        result = [c for c in line.split(' ') if c]
        if len(result) != len(fields):
    	    return None
        data = {}
        for ix, value in enumerate(result):
    	    data[fields[ix]] = value
        yield data

```
{% endcode %}

and the output:

```bash
$ secator x ls . --json
ls -al .
total 16
❌ Failed to load item as output type:
  {'permissions': 'drwxr-xr-x', 'link_count': '3', 'owner': 'osboxes', 'group': 'osboxes', 'size': '4096', 'month': 'May', 'day': '2', 'hour': '04:50', 'path': '.', '_type': 'unknown', '_context': {'workspace_name': 'default'}, '_source': 'ls', '_uuid': 'fa90033a-56a4-4df1-b280-bb6f7cfdcd37'}
❌ Failed to load item as output type:
  {'permissions': 'drwxr-xr-x', 'link_count': '4', 'owner': 'osboxes', 'group': 'osboxes', 'size': '4096', 'month': 'May', 'day': '2', 'hour': '04:49', 'path': '..', '_type': 'unknown', '_context': {'workspace_name': 'default'}, '_source': 'ls', '_uuid': 'a76c01e4-8e07-4bdd-a2cf-66e96f1cd112'}
❌ Failed to load item as output type:
  {'permissions': '-rw-r--r--', 'link_count': '1', 'owner': 'osboxes', 'group': 'osboxes', 'size': '508', 'month': 'May', 'day': '2', 'hour': '04:55', 'path': 'ls.py', '_type': 'unknown', '_context': {'workspace_name': 'default'}, '_source': 'ls', '_uuid': '7189352a-fd06-493e-9bf8-de8e4a083782'}
❌ Failed to load item as output type:
  {'permissions': 'drwxr-xr-x', 'link_count': '2', 'owner': 'osboxes', 'group': 'osboxes', 'size': '4096', 'month': 'May', 'day': '2', 'hour': '04:55', 'path': '__pycache__', '_type': 'unknown', '_context': {'workspace_name': 'default'}, '_source': 'ls', '_uuid': '2c1d78b6-0c4d-4fa8-90c8-d08f8eda4922'}
🗄 Saved JSON report to ~/.secator/reports/default/tasks/2/report.json
🗄 Saved CSV reports to ~/.secator/reports/default/tasks/2/report_target.csv
❗Found 0 results.
```

The JSON objects are properly output, but they fail to convert with an existing [output-types.md](../../../in-depth/concepts/output-types.md "mention").

To get the original JSON output, run with `--orig` flag:

```bash
$ secator x ls . --json --orig
ls -al .
total 16
{"permissions": "drwxr-xr-x", "link_count": "3", "owner": "osboxes", "group": "osboxes", "size": "4096", "month": "May", "day": "2", "hour": "04:50", "filename": ".", "_context": {"workspace_name": "default"}, "_source": "ls", "_uuid": "4aafe790-286a-4d59-9376-e6867d9bed6d", "_type": {}}
{"permissions": "drwxr-xr-x", "link_count": "4", "owner": "osboxes", "group": "osboxes", "size": "4096", "month": "May", "day": "2", "hour": "04:49", "filename": "..", "_context": {"workspace_name": "default"}, "_source": "ls", "_uuid": "733a0336-eef4-4601-a420-8de68315c3e3", "_type": {}}
{"permissions": "-rw-r--r--", "link_count": "1", "owner": "osboxes", "group": "osboxes", "size": "508", "month": "May", "day": "2", "hour": "04:55", "filename": "ls.py", "_context": {"workspace_name": "default"}, "_source": "ls", "_uuid": "f06836e1-844b-4e5d-9978-9fbbdba50d9c", "_type": {}}
{"permissions": "drwxr-xr-x", "link_count": "2", "owner": "osboxes", "group": "osboxes", "size": "4096", "month": "May", "day": "2", "hour": "04:56", "filename": "__pycache__", "_context": {"workspace_name": "default"}, "_source": "ls", "_uuid": "9eb6b94a-4765-4764-9d48-89f2fa72e327", "_type": {}}
🗄 Saved JSON report to ~/.secator/reports/default/tasks/3/report.json
🗄 Saved CSV reports to ~/.secator/reports/default/tasks/3/report_target.csv
```

Ok, in a few lines of code we successfully managed to turn the `ls` output into structured JSON lines.

{% hint style="warning" %}
<mark style="color:red;">**YES**</mark><mark style="color:red;">, but we don't have anything in the JSON reports !</mark>
{% endhint %}

***

## Mapping output types

To get some useful results that secator reports understand, we need to map this arbitrary JSON output to one of the existing output type that `secator` provides. For instance, the `Vulnerability` output type !

For instance, we could consider as a vulnerability any path that is executable by the public. That's the final `w` in the permission string.

Let's change the implementation to output objects of type `Vulnerability`:

{% code title="~/.secator/templates/ls.py" %}
```python
from secator.runners import Command
from secator.decorators import task
from secator.output_types import Vulnerability


@task()
class ls(Command):
    cmd = 'ls -al'
    output_types = [Vulnerability]

    @staticmethod
    def item_loader(self, line):
        fields = ['permissions', 'link_count', 'owner', 'group', 'size', 'month', 'day', 'hour', 'path']
        result = [c for c in line.split(' ') if c]
        if len(result) != len(fields):
            return None
        data = {}
        for ix, value in enumerate(result):
            data[fields[ix]] = value

        # Output vulnerabilities
        permissions = data['permissions']
        path = data['path']
        full_path = f'{self.input}/{path}'
        if permissions[-2] == 'w':  # found a vulnerability !
            yield Vulnerability(
                name='World-writeable path',
                severity='high',
                confidence='high',
                provider='ls',
                matched_at=full_path,
                extra_data={k: v for k, v in data.items() if k != 'path'}
            )

```
{% endcode %}

Let's make the `ls.py` file world-writeable with `chmod a+w ls.py` to create a vulnerability, and re-run our command:

```bash
$ secator x ls .
ls -al .
total 16
drwxr-xr-x 3 osboxes osboxes 4096 May  2 06:14 .
drwxr-xr-x 4 osboxes osboxes 4096 May  2 04:49 ..
🚨 [World-writeable path 🡕] [high] ./ls.py [permissions:-rw-rw-rw-, link_count:1, owner:osboxes, group:osboxes, size:1015, month:May, day:2, hour:06:14]
drwxr-xr-x 2 osboxes osboxes 4096 May  2 06:14 __pycache__
🗄 Saved JSON report to /home/osboxes/.secator/reports/default/tasks/140/report.json
🗄 Saved CSV reports to 
   • /home/osboxes/.secator/reports/default/tasks/140/report_target.csv
   • /home/osboxes/.secator/reports/default/tasks/140/report_vulnerability.csv
✔ Found 1 vulnerability.
```

{% hint style="success" %}
We have successfully integrated the command `ls` with `secator` !
{% endhint %}

***
