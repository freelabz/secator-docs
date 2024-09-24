---
description: ... or how to integrate groups of tasks with similar options.
---

# Example: cat hunters

This section will present a more complex use case where we have three commands: `bigdog`, `catkiller` and `eagle` which purpose is to find cats.&#x20;

We will start by integrating `bigdog` to `secator` before realizing that most options can be mutualized between the three tools, and a common output type `Cat` can be created for all three.

***

## Bigdog

Let's suppose we have a **fictional** utility called `bigdog` which purpose is to hunt cats on the internet. We want to add `bigdog` to `secator`.

Here are some of `bigdog`'s options:

{% tabs %}
{% tab title="-site" %}
`bigdog` can be run on a single site using `-site`:

```sh
$ bigdog -site loadsofcats.com
   / \__
  (    @\___   =============
  /         O  BIGDOG v1.0.0
 /   (_____/   =============
/_____/
garfield [boss, 14]
tony [admin, 18]
```
{% endtab %}

{% tab title="-list" %}
`bigdog` can be run on a list of sites using `-list`:

```sh
$ bigdog -list sites.txt -json
   / \__
  (    @\___   =============
  /         O  BIGDOG v1.0.0
 /   (_____/   =============
/_____/
garfield [boss, 14]
romuald [minion, 5]
tony [admin, 18]
```
{% endtab %}

{% tab title="-json" %}
`bigdog` can output JSON lines using `-json`:

```sh
$ bigdog -site loadsofcats.com -json
   / \__
  (    @\___   =============
  /         O  BIGDOG v1.0.0
 /   (_____/   =============
/_____/
{"name": "garfield", "age": 14, "host": "loadsofcat.com", "position": "boss"}
{"name": "tony", "age": 18, "host": "loadsofcats.com", "position": "admin"}
```
{% endtab %}
{% endtabs %}

A basic definition of `bigdog` using basic `secator` concepts will be:

{% code title="secator/tasks/bigdog.py" lineNumbers="true" %}
```py
from secator.runners import Command
from secator.decorators import task


@task
class bigdog(Command):
    cmd = 'bigdog'
    json_flag = '-json'
    input_flag = '-site'
    file_flag = '-list'
```
{% endcode %}

You can now run `bigdog` from the CLI or the library:

{% tabs %}
{% tab title="CLI" %}
```bash
secator x bigdog --help
secator x bigdog loadsofcats.com
```
{% endtab %}

{% tab title="Python" %}
```python
from secator.tasks import bigdog

# Get all results as a list, blocks until command has finished running
bigdog('loadsofcats.com').run()
[
    {"name": "garfield", "age": 14, "host": "loadofcats.com", "position": "boss"},
    {"name": "tony", "age": 18, "host": "loadsofcats.com", "position": "admin"}
]

# Get result items in real-time as they arrive to stdout
for cat in bigdog('loadsofcats.com'):
    print(cat['name'] + '(' + cat['age'] + ')')

# Will print
garfield (14)
tony (18)
```
{% endtab %}
{% endtabs %}

Okay, this is a good start.

Now what if the `bigdog` command has some more options that you would like to integrate ?

* `-timeout` allows to specify a request timeout.
* `-rate` allows to specify the max requests per minute.

You can add the `opts` parameter to your `Command` object to define the cmd options:

<pre class="language-py" data-line-numbers><code class="lang-py"><strong>from secator.runners import Command
</strong>from secator.decorators import task


@task
class bigdog(Command):
    cmd = 'bigdog'
    json_flag = '-json'
    input_flag = '-site'
    file_flag = '-list'
    opt_prefix = '-'
    opts = {
        'timeout': {'type': int, 'help': 'Timeout (in seconds)'},
        'rate': {'type': int, 'help': 'Max requests per minute'}
    }
</code></pre>

You can now use `bigdog` with this set of options:

{% tabs %}
{% tab title="CLI" %}
```bash
secator x bigdog --help
secator x bigdog loadsofcats.com -json
secator x bigdog loadsofcats.com -timeout 1 -rate 100 -o table,csv,txt,gdrive
```
{% endtab %}

{% tab title="Python" %}
```python
from secator.tasks import bigdog
bigdog('loadsofcats.com', rate=100, timeout=3).run()  # adding rate and timeout options
```
{% endtab %}
{% endtabs %}

***

## Cat hunters category

One advantage of having class-based definitions is that we can group similar tools together in categories.

Let's assume we have 2 other tools that can hunt cats: `catkiller` and `eagle`...

... but each of those tools might be written by a different person, and so the interface and output is different for each of them:

{% tabs %}
{% tab title="catkiller" %}
<pre class="language-bash"><code class="lang-bash"><strong>$ catkiller --host loadsofcats.com --max-wait 1000 --max-rate 10 --json
</strong>Starting catkiller session ...
{"_info": {"name": "tony", "years": 18}, "site": "loadsofcats.com", "job": "admin"}
{"_info": {"name": "garfield", "years": 14}, "site": "loadsofcats.com", "job": "boss"}

# or to pass multiple hosts, it needs to be called like:
$ cat hosts.txt | catkiller --max-wait 1000 --max-rate 10 --json
</code></pre>

**Inputs:**

* `--host` is equivalent to `bigdog`'s `-site`.
* `--max-wait` is equivalent to `bigdog`'s `-timeout`, but in milliseconds instead of seconds.
* `--max-rate` is equivalent to `bigdog`'s `-rate`.
* `--json` is equivalent to `bigdog's` `-json` option, but uses a different option character "`--`".
* `cat hosts.txt | catkiller` is the equivalent to`bigdog`'s `-list`.

**Output:**

* `_info` has the data for `name` and `age`, but `age` is now `years`.
* `site` is the equivalent of `bigdog`'s `host`.
* `job` is the equivalent of `bigdog`'s `position`.
{% endtab %}

{% tab title="eagle" %}
<pre class="language-bash"><code class="lang-bash"><strong>$ eagle -u loadsofcats.com -timeexpires 1 -jsonl
</strong>                  _      
                 | |     
  ___  __ _  __ _| | ___ 
 / _ \/ _` |/ _` | |/ _ \
|  __/ (_| | (_| | |  __/  v2.2.0
 \___|\__,_|\__, |_|\___|
             __/ |       
            |___/       
{"alias": "tony", "occupation": "admin", "human_age": 105}

# or to pass multiple hosts, it needs to be called like:
$ eagle -l hosts.txt -timeexpires 1 -jsonl
                  _      
                 | |     
  ___  __ _  __ _| | ___ 
 / _ \/ _` |/ _` | |/ _ \
|  __/ (_| | (_| | |  __/  v2.2.0
 \___|\__,_|\__, |_|\___|
             __/ |       
            |___/    
{"alias": "tony", "occupation": "admin", "human_age": 105, "host": "loadsofcats.com"}
</code></pre>

**Inputs:**

* `-u` is equivalent to `bigdog`'s `-site`.
* `-l` is equivalent to `bigdog`'s `-list`.
* `-timeexpires` is equivalent to `bigdog`'s `-timeout`.
* `eagle` **does not support** setting the maximum requests per seconds (`bigdog`'s `-rate`).
* `-jsonl` is the flag to output JSON lines, instead of `bigdog`'s `-json`.

**Output:**

* `alias` is the equivalent of `bigdog`'s `name`.
* `occupation` is the equivalent of `bigdog`'s `job`.
* `human_age` is the human age conversion of the cat age.
{% endtab %}
{% endtabs %}

### Cat output type

We first define a base `Cat` dataclass to define the common output schema and a `CatHunter` category as an input interface.

We take `bigdog`'s output schema as reference to create the `Cat` output type:

{% code title="secator/output_types/cat.py" %}
```py
from secator.definitions import OPT_NOT_SUPPORTED
from secator.output_types import OutputType
from secator.decorators import task
from dataclasses import dataclass, field


@dataclass
class Cat(OutputType):
    name: str
    age: int
    alive: bool = False
    _source: str = field(default='', repr=True)
    _type: str = field(default='cat', repr=True)
    _uuid: str = field(default='', repr=True, compare=False)

    _table_fields = [name, age]
    _sort_by = (name, age)

    def __str__(self) -> str:
        return self.ip

```
{% endcode %}

### CatHunter category

We take `bigdog`'s options names as reference and add the ones that can be mutualized to the `CatHunter` category:

{% code title="secator/tasks/_categories.py" %}
```python
from secator.output_types import Cat
# ...

class CatHunter(Command):
    meta_opts = {
        'timeout': {'type': int, 'default': 1, 'help': 'Timeout (in seconds)'},
        'rate': {'type': int, 'default': 1000, 'help': 'Max requests per minute'},
    }
    output_types = [Cat]
```
{% endcode %}

### Tools implementation

Finally we inherit all commands implementation from `CatHunter` and write the option mapping for the remaining cat-hunter commands:

{% tabs %}
{% tab title="bigdog" %}
{% code title="secator/tasks/bigdog.py" %}
```python
from secator.categories import CatHunter
from secator.decorators import task


@task()
class bigdog(CatHunter):
    cmd = 'bigdog'
    json_flag = '-json'
    input_flag = '-site'
    file_flag = '-list'
    opt_prefix = '-'
```
{% endcode %}
{% endtab %}

{% tab title="catkiller" %}
{% code title="secator/tasks/catkiller.py" %}
```python
from secator.categories import CatHunter
from secator.decorators import task
from secator.output_types import Cat


@task()
class catkiller(CatHunter):
    cmd = 'catkiller'
    json_flag = '--json'
    input_flag = '--host'

    # stdin-like input using 'cat <FILE> | <COMMAND>'
    file_flag = None

    # catkiller options start with "--" unlike the other tools
    opt_prefix = '--' 

    # Map `catkiller` options to CatHunter.meta_opts
    opt_key_map = {
        'rate': 'max-rate'
        'timeout': 'max-wait'
    }
    opt_value_map = {
        'timeout': lambda x: x / 1000 # converting milliseconds to seconds
    }

    # Map `catkiller` output schema to Cat schema
    output_map = {
	Cat: {
	    'name': lambda x: x['_info']['name'], # note: you can use any function, we use
	    'age': lambda x: x['_info']['age'],   #       lambdas for readability here
	    'host': 'site',   # 1:1 mapping
	    'job': 'job' # 1:1 mapping
	}
    }
```
{% endcode %}
{% endtab %}

{% tab title="eagle" %}
<pre class="language-python" data-title="secator/tasks/eagle.py"><code class="lang-python">from secator.categories import CatHunter
from secator.decorators import task
from secator.definitions import OPT_NOT_SUPPORTED
from secator.output_types import Cat
<strong>
</strong><strong>
</strong><strong>@task()
</strong>class eagle(CatHunter):
    cmd = 'eagle'
    json_flag = '-jsonl'
    input_flag = '-u'
    file_flag = '-l'

    # Map `eagle` input options to CatHunter.meta_opts
    opt_key_map = {
        'rate': 'timeexpires',
        'timeout': OPT_NOT_SUPPORTED # explicitely state that this option not supported by the target tool
    }

    # Map `eagle` output schema to Cat schema:
    output_map = {
	Cat: {
	    'name': 'alias',
	    'age': lambda x: human_to_cat_age(x['human_age']),
	    'job': 'occupation',
	}
    }

    # Add 'host' key dynamically after the item has been converted to the output schema,
    # since `eagle` doesn't return the host systematically.
    @staticmethod
    def on_item(self, item):
        item['host'] = item.get('host') or self.input
        return item


def human_to_cat_age(human_age):
    cat_age = 0
    if human_age &#x3C;= 22:
        cat_age = human_age // 11
    else:
        cat_age = (human_age - 22) // 5 + 2
    return cat_age
</code></pre>
{% endtab %}
{% endtabs %}

Using these definitions, we can now use all the cat-hunter commands with a common interface (input options & output schema):

{% tabs %}
{% tab title="CLI" %}
```bash
secator x bigdog loadsofcats.com -rate 1000 -timeout 1 -json
secator x eagle loadsofcats.com -rate 1000 -timeout 1 -json
secator x catkiller loadsofcats.com -rate 1000 -timeout 1 -json
```
{% endtab %}

{% tab title="Python" %}
```python
>>> from secator.tasks import bigdog, catkiller, eagle
>>> meta_opts = {'timeout': 1, 'rate': 1000, 'json': True}
>>> bigdog('loadsofcats.com', **meta_opts).run()
[
    Cat(name="garfield", age=14, host="loadsofcats.com", position="boss", _source="bigdog"),
    Cat(name="tony", age=18, host="loadsofcats.com", position="admin", _source="bigdog")
]
>>> catkiller('catrunner.com', **meta_opts).run()
[
    Cat(name=fred, age=12, host="catrunner.com", position="minion", _source="catkiller"},
    Cat(name=mark, age=20, host="catrunner.com", position="minion", _source="catkiller"}
]
>>> eagle('allthecats.com', **meta_opts).run()
[
    Cat(name="marcus", age=4, host="allthecats.com", position="minion", _source="eagle"},
    Cat(name="rafik", age=7, host="allthecats.com", position="minion", _source="eagle"}
]
```
{% endtab %}
{% endtabs %}

***
