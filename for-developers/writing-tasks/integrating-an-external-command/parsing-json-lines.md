---
description: ... or how to integrate tools that already output JSON lines.
---

# Parsing JSON lines

If your tool outputs JSON lines, it's very easy to integrate it with `secator`.

Based on how your tool's output maps will map to `secator` output types, read:

* [#one-to-one-mapping](parsing-json-lines.md#one-to-one-mapping "mention") (1 JSON line = 1 `secator` output type).
* [#one-to-many](parsing-json-lines.md#one-to-many "mention") (1 JSON line = many`secator` output types).

***

## One-to-one mapping

**Steps:**

* Use the `JSONSerializer` item loader.
* Add an `output_map` to map your tool's output to one of secator's [output-types.md](../../../in-depth/concepts/output-types.md "mention")**.**

#### **Example:**

For instance, `mytool` outputs JSON lines when we run it like:

```bash
mytool -jsonl -u mytarget.com
{"url": "https://mytarget.com/api", "status": 200, {"details": {"ct": "application/json"}}
{"url": "https://mytarget.com/api/metrics", "status": 403, "details": {}}
```

An integration of `mytool` with `secator` would look like:

{% code title="secator/tasks/mytool.py" %}
```python
from secator.runners import Command
from secator.output_types import Url
from secator.serializers import JSONSerializer
from secator.definitions import URL, STATUS_CODE, CONTENT_TYPE


class mytool(Command):
  input_flag = '-u'
  json_flag = '-jsonl'
  output_types = [Url]
  item_loaders = [JSONSerializer()]
  output_map = {
    Url: {
     URL: 'url',
     STATUS_CODE: 'status',
     CONTENT_TYPE: lambda x: x['details'].get('ct', '')
    }
  }

```
{% endcode %}

**Steps taken:**

* Import the desired runner (`Command`).
* Import the desired output type(s) and the field names that we want to map.
* Set `input_flag` to `mytool`'s input flag `-u`.&#x20;
* Set `json_flag` to `mytool`'s JSON line flag `jsonl`.&#x20;
* Set `output_types` to our desired output types \[[`Url`](../../../in-depth/concepts/output-types.md#url)].&#x20;
* Set `output_map` to map `mytool`'s output fields to each [`Url`](../../../in-depth/concepts/output-types.md#url)'s fields (you need to map at least the `required=True` fields).

That's it ! You can now run `mytool` with `secator` and enjoy all the features it brings on top of it:

{% tabs %}
{% tab title="CLI" %}
```bash
secator x mytool mytarget.com
                         __            
   ________  _________ _/ /_____  _____
  / ___/ _ \/ ___/ __ `/ __/ __ \/ ___/
 (__  /  __/ /__/ /_/ / /_/ /_/ / /    
/____/\___/\___/\__,_/\__/\____/_/     v0.6.0

                        freelabz.com
mytool -u mytarget.com -jsonl
🔗 https://mytarget.com/api [200] [application/json]
🔗 https://mytarget.com/api/metrics [403]
```
{% endtab %}

{% tab title="Python" %}
```python
from secator.tasks import mytool

task = mytool('mytarget.com')
for item in task:
    print(item)  # item is now a secator output type like Vulnerability or Port

```
{% endtab %}
{% endtabs %}

***

## One-to-many

**Steps:**

* Add a static method `on_json_loaded` to hook onto the JSON Serializer output.
* Modify the data and yield `secator` [output-types.md](../../../in-depth/concepts/output-types.md "mention").

#### **Example:**

For instance, if `mytool` outputs urls in batch:

```bash
mytool -jsonl -u mytarget.com
{"urls": [{"url": "https://mytarget.com/api", "status": 200, "content-type": "application/json"}, {"url": "https://mytarget.com/api/metrics", "status": 403, "content-type": "application/text"}]
```

An integration of `mytool` with `secator` would look like:

{% code title="secator/tasks/mytool.py" %}
```python
from secator.runners import Command
from secator.output_types import Url
from secator.definitions import URL, STATUS_CODE, CONTENT_TYPE

class mytool(Command):
  input_flag = '-u'
  json_flag = '-jsonl'
  output_types = [Url]

  @staticmethod
  def on_json_loaded(self, data):
      for item in data['urls']:
          yield Url(
            URL: item['url'],
            STATUS_CODE: item['status'],
            CONTENT_TYPE: item.get('content-type', '')
          )

```
{% endcode %}

{% hint style="info" %}
See [#lifecyle-hooks](../../../in-depth/concepts/runners.md#lifecyle-hooks "mention") for more details on which hooks you can use.
{% endhint %}

That's it ! You can now run `mytool` with `secator` and enjoy all the features it brings on top of it:

{% tabs %}
{% tab title="CLI" %}
```bash
secator x mytool mytarget.com
                         __            
   ________  _________ _/ /_____  _____
  / ___/ _ \/ ___/ __ `/ __/ __ \/ ___/
 (__  /  __/ /__/ /_/ / /_/ /_/ / /    
/____/\___/\___/\__,_/\__/\____/_/     v0.6.0

                        freelabz.com
mytool -u mytarget.com -jsonl
🔗 https://mytarget.com/api [200] [application/json]
🔗 https://mytarget.com/api/metrics [403]
```
{% endtab %}

{% tab title="Python" %}
```python
from secator.tasks import mytool

task = mytool('mytarget.com')
for item in task:
    print(item)  # item is now a secator output type like Vulnerability or Port

```
{% endtab %}
{% endtabs %}
