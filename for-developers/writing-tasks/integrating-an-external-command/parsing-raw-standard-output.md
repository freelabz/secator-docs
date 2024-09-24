---
description: >-
  ... or how to integrate tools that prints to stdout and do not support JSON
  lines.
---

# Parsing raw standard output

If your tool does not output JSON lines / JSON files, it's requires a bit more effort to integrate it with `secator`.

Depending on how you want to parse the output, read:

* [#using-regular-expressions](parsing-raw-standard-output.md#using-regular-expressions "mention")
* [#writing-a-custom-item-loader](parsing-raw-standard-output.md#writing-a-custom-item-loader "mention")

***

## Using regular expressions

You can parse the standard output using regular expressions thanks to `secator`'s `RegexSerializer`.

#### **Example:**

Assume `mytool` outputs on stdout like:

```bash
mytool -u mytarget.com
[INF] This is an info message
[ERR] This is an error message
[FOUND] https://mytarget.com/api [type=url] [status=200] [content_type=application/json] [title=MyAwesomeWebPage]
[FOUND] https://mytarget.com/api/metrics [type=url] [status=403]
[FOUND] A3TBABCD1234EFGH5678 [type=aws_api_key] [matched_at=https://mytarget/api/.aws_key.json]
[FOUND] <-- an HTML comment --> [type=aws_api_key] [matched_at=https://mytarget/api/.aws_key.json]
[FOUND] CVE-2021-44228 [type=vulnerability] [matched_at=https://mytarget/api/sensitive_api_path]
```

First we need to find an expressions that will match the items marked with `[FOUND]` and get the individual values using a named regex (you can use [Pythex](https://pythex.org) for this).

Here is the one we came up with:

{% code overflow="wrap" %}
```python
OUTPUT_REGEX = r'\[\w+]\s(?P<value>.*)\s\[type=(?P<type>[\w_]+)\](\s\[status=(?P<status>\d+)\])?(\s\[content_type=(?P<content_type>[\w\/]+)\])?(\s\[title=(?P<title>.*)\])?(\s\[matched_at=(?P<matched_at>.*)\])?'
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

OUTPUT_REGEX = r'\[\w+]\s(?P<value>.*)\s\[type=(?P<type>[\w_]+)\](\s\[status=(?P<status>\d+)\])?(\s\[content_type=(?P<content_type>[\w\/]+)\])?(\s\[title=(?P<title>.*)\])?(\s\[matched_at=(?P<matched_at>.*)\])?'


@task()
class mytool(Command):
  cmd = '/home/osboxes/.local/bin/mytool'
  input_flag = '-u'
  json_flag = '-jsonl'
  output_types = [Url, Tag, Vulnerability]

  # Override the default item loader (JSONSerializer) with the RegexSerializer
  item_loaders = [
    RegexSerializer(
      OUTPUT_REGEX,
      fields=['value', 'type', 'status', 'content_type', 'title', 'matched_at']
    )
  ]

  # React to items loaded by the RegexSerializer, and yield secator output types
  # like Url, Vulnerability, and Tag.
  @staticmethod
  def on_regex_loaded(self, item):
    # this is called after the regex serializer runs,
    # so we can expect item to be a dict with the matched regex values
    if (item['type'] == 'url'):
      yield Url(
        url=item['value'],
        status_code=int(item['status']),
        content_type=item['content_type'],
        title=item['title']
      )
    elif (item['type'] == 'vulnerability'):
      cve_id = item['value']
      lookup_data = Vuln.lookup_cve(cve_id)  # perform vulnerability search
      vuln = {
        'matched_at': item['matched_at']
      }
      if lookup_data:
        vuln.update(**lookup_data)
      yield Vulnerability(**vuln)
    else:
      yield Tag(
        name=item['type'],
        match=item['matched_at'],
        extra_data={
          'secret': item['value']
        }
      )

```
{% endcode %}

Run it with `secator`:

{% tabs %}
{% tab title="CLI" %}
```bash
$ secator x mytool TARGET

                         __            
   ________  _________ _/ /_____  _____
  / ___/ _ \/ ___/ __ `/ __/ __ \/ ___/
 (__  /  __/ /__/ /_/ / /_/ /_/ / /    
/____/\___/\___/\__,_/\__/\____/_/     v0.6.0

                        freelabz.com

No Celery worker alive.
/home/osboxes/.local/bin/mytool -u mytarget -jsonl
[INF] This is an info message
[ERR] This is an error message
🔗 https://mytarget.com/api [200] [MyAwesomeWebPage] [application/json]
🔗 https://mytarget.com/api/metrics [403]
🏷️ aws_api_key found @ https://mytarget/api/.aws_key.json
    secret: A3TBABCD1234EFGH5678
🚨 [Object Injection 🡕] [critical] https://mytarget/api/sensitive_api_path
```
{% endtab %}

{% tab title="Python" %}
```python
from secator.tasks import mytool
task = mytool('TARGET')
for item in task:
    print(item)  # this will output Url, Vulnerability, or Tag items.

```
{% endtab %}
{% endtabs %}

***

### Writing a custom item loader

You can parse the standard output using a custom item loader by overriding the `item_loader` static method in the task definition file.

**Example:**

Assume `mytool` outputs on stdout like:

```bash
mytool -u mytarget.com
https://mytarget.com/api | url | 200 | application/json | MyAwesomePage
https://mytarget.com/api/metrics | url | 403
A3TBABCD1234EFGH5678 | aws_api_key | http://mytarget/api/.aws_key.json
<-- an HTML comment --> | html_comment | http://mytarget/api/.aws_key.json
CVE-2021-44228 | vulnerability | http://mytarget/api/sensitive_ap
```

```python
from secator.decorators import task
from secator.runners import Command
from secator.output_types import Url, Tag, Vulnerability


@task()
class mytool(Command):
  cmd = '/home/osboxes/.local/bin/mytool'
  input_flag = '-u'
  json_flag = '-jsonl'
  output_types = [Url, Tag, Vulnerability]

  @staticmethod
  def item_loader(self, line):
      items = [c.strip() for c in line.split('|')]
      value, item_type = tuple(items[0:2])
      if item_type == 'url':
          yield Url(
              url=value,
              status_code=items[3],
              content_type=items[4] if len(items) > 3 else '',
              title=items[5] if len(items) > 4 else ''
          )
      elif item_type == 'vulnerability':
          cve_id = value
          lookup_data = Vuln.lookup_cve(cve_id)  # perform vulnerability search
          vuln = {
            'matched_at': items[2]
          }
          if lookup_data:
            vuln.update(**lookup_data)
          yield Vulnerability(**vuln)
      else: # tag
          yield Tag(
              name=item_type,
              match=items[2],
              extra_data={
                  'value': value
              }
          )
 
```

