---
description: ... or how to turn a command that you use daily into an overpowered machine.
---

# Integrating an external command

***

### Creating a task file

Imagine we have a tool named `mytool` that we want to integrate with `secator`.

Start by creating a file named `mytool.py`:

```python
from secator.decorators import task  # required for `secator` to recognize tasks
from secator.runners import Command  # the `secator` runner to use


@task()
class mytool(Command): # make sure class name is lowercase and matches the filename.
    cmd = 'mytool'  # ... or whatever the name of your external command is.

```

{% hint style="info" %}
The `task` decorator is required for `secator` to recognize class-based definition that need to be loaded at runtime.
{% endhint %}

Move this file over to:

* `~/.secator/templates/` (or whatever your `dirs.templates` in [configuration.md](../../../getting-started/configuration.md "mention") points to)

&#x20; **OR**

* `secator/tasks/` if you have a [development-setup.md](../../development-setup.md "mention") and want to contribute your task implementation to the official `secator` repository.

***

### Adding an input flag \[optional]

If your tool requires an input flag or a list flag to take its targets, for instance:

* `mytool -u TARGET`
* `mytool -l TXT_FILE`

You need to set the `input_flag` and `file_flag` class options:

```python
from secator.decorators import task
from secator.runners import Command


@task()
class mytool(Command):
    cmd = 'mytool'
    input_flag = '-u'
    file_flag = '-l'

```

Setting these attributes allows us to run `mytool` with `secator` like:

```bash
secator x mytool TARGET    # will run mytool -u TARGET
secator x mytool TXT_FILE  # will run mytool -l TXT_FILE
```

#### Important Note on Command Availability

Ensure that the external command you are integrating is callable within your system's `PATH`. For example, a file located at `/opt/tools/testssl.sh/testssl.sh` **will not** work unless properly added to your `PATH`.

To verify if your command is callable, you can run:

```bash
which [command]
```

If it returns the path to your command, then it is available and can be used with secator. If not, you will need to update your PATH or move the file to a directory that is already included in your PATH.

### Parsing a command's output

Now that you have a basic implementation working, you need to convert your command's output into structured output (JSON).

Find out what your command's output looks like and pick the corresponding guide:

* Read [parsing-json-lines.md](parsing-json-lines.md "mention") if your tool has an option to stream JSON lines (**preferred**).
* Read [parsing-output-files.md](parsing-output-files.md "mention") if your tool has an option to output to a file (e.g JSON or CSV).
* Read [parsing-raw-standard-output.md](parsing-raw-standard-output.md "mention") if your tools **only** outputs to `stdout` .

***

### Adding more options \[optional]

To support more options, you can use the `opt_prefix`, `opts` , `opt_key_map` and `opt_value_map` attributes.

Assuming `mytool` has the `--delay`, `--debug` and `--include-tags` options, we would support them this way:

```python
@task()
class mytool(Command):
    # ...
    opt_prefix = '--'  # default is '-'
    opts = {
        'tags': {'type': str, 'short': 't', 'help': 'Tags'},
        'delay': {'type': int, 'short': 'dbg', 'help': 'Delay'},
        'debug': {'is_flag': True, 'short': 'd', 'help': 'Debug mode'},
    }
    opt_key_map = {   # to map input options
        'tags': 'include-tags',
    }
    opt_value_map = {  # to transform options values
        'delay': lambda x: x * 1000  # convert seconds to milliseconds
    }

```

With this config, running either of:

```bash
secator x mytool --tags tag1,tag2 --debug --delay 5 TARGET  # long option format
secator x mytool -t tag1,tag2 -dbg -d 5 TARGET              # short option format
```

&#x20;will result in running `mytool` like:

```bash
mytool --include-tags tag1,tag2 --debug --delay 5000 -u TARGET
```

{% hint style="warning" %}
All keys in `opts` must be in lowercase. If you need to support an uppercase option, follow these steps :

1. Define the option in opts using a lowercase key:
```py
opts = {
    'my_upper_cas_option':{'type':str, 'shor':'P', 'help': 'Products'}
}
```
2. Map the lowercase key to its corresponding uppercase option using `opt_key_map`:
```py
opt_key_map = {
    'my_upper_cas_option': 'P'
}
```
{% endhint %}

***

### Adding an install command \[optional]

To support installing your tool with secator, you can set the `install_cmd` , and / or `install_github_handle` attributes:

```python
@task()
class mytool(Command):
    # ...
    install_cmd = "sudo apt install -y mytool"
    install_github_handle = "myorg/mytool"

```

{% hint style="info" %}
If `install_github_handle` is set, `secator` will try to fetch a binary from GitHub releases specific to your platform, and fallback to `install_cmd` if it cannot find a suitable release, or if the API rate limit is reached.
{% endhint %}

Now you can install `mytool` using:

```bash
secator install tools mytool
```

***

### Using a category \[optional]

If your tool fits into one of `secator`'s built-in command categories, you can inherit from it's option set:

* `Http`: A tool that makes HTTP requests.
* `HttpCrawler`: A command that crawls URLs (subset of `Http`).
* `HttpFuzzer`: A command that fuzzes URLs (subset of `Http`).

You can inherit from these categories and map their options to your command.

{% hint style="info" %}
Categories are defined in `secator/tasks/_categories.py`
{% endhint %}

For instance, if `mytool` is an HTTP fuzzer, we would change it's implementation like:

```python
from secator.tasks._categories import HTTPFuzzer
from secator.definitions import OPT_NOT_SUPPORTED


@task()
class mytool(Command, HTTPFuzzer):
    # ...
    opt_key_map = {
        # HTTPFuzzer options mapping
        HEADER: 'header',
        DELAY: 'delay',
        DEPTH: OPT_NOT_SUPPORTED,
        FILTER_CODES: OPT_NOT_SUPPORTED,
        FILTER_REGEX: OPT_NOT_SUPPORTED,
        FILTER_SIZE: OPT_NOT_SUPPORTED,
        FILTER_WORDS: OPT_NOT_SUPPORTED,
        FOLLOW_REDIRECT: OPT_NOT_SUPPORTED,
        MATCH_CODES: OPT_NOT_SUPPORTED,
        MATCH_REGEX: OPT_NOT_SUPPORTED,
        MATCH_SIZE: OPT_NOT_SUPPORTED,
        MATCH_WORDS: OPT_NOT_SUPPORTED,
        METHOD: OPT_NOT_SUPPORTED,
        PROXY: OPT_NOT_SUPPORTED,
        RATE_LIMIT: OPT_NOT_SUPPORTED,
        RETRIES: OPT_NOT_SUPPORTED,
        THREADS: OPT_NOT_SUPPORTED,
        TIMEOUT: 'timeout',
        USER_AGENT: 'user-agent',

        # my tool specific options
        'tags': 'include-tags',
    }
    opt_value_map = {
        'delay': lambda x: x * 1000  # convert seconds to milliseconds
    }

```

{% hint style="info" %}
Make sure you map **all** the options from the **`HTTPFuzzer`** category. If some options are not supported by your tool, mark them with `OPT_NOT_SUPPORTED`.
{% endhint %}

With this config, running:

```bash
secator x mytool --help
```

would list:

* The `meta`options in the `HTTPFuzzer` category that are supported by `mytool`.
* The options only usable by `mytool`.&#x20;

For instance, running:

{% tabs %}
{% tab title="CLI" %}
```bash
secator x mytool \
  -header "Authorization: Bearer MYTOKEN" \
  -delay 1 \
  -ua "secator/0.6 (Debian)" \
  -timeout 5 \
  -t tag1,tag2 \
  TARGET
```
{% endtab %}

{% tab title="Python" %}
```python
from secator.tasks import mytool

task = mytool(
  'TARGET',
  header="Authorization: Bearer MYTOKEN",
  delay=1,
  user_agent="secator/0.6 (Debian)",
  timeout=5,
  tags='tag1,tag2'
)
for item in task:
     print(item)
```
{% endtab %}
{% endtabs %}

would result in running `mytool` like:

```bash
mytool \
  --header "Authorization: Bearer MYTOKEN" \
  --delay 1000 \
  --user-agent "secator/0.6 (Debian)" \
  --timeout 5 \
  --include-tags tag1,tag2
  -u TARGET
```

***

### Supporting proxies \[optional]

If your tool supports proxies, `secator` has first-class support for **`proxychains`**, **`HTTP`** and **`SOCKS5`** proxies, and can dynamically choose the type of proxy to use based on the following attributes:

* `proxy_socks5` : boolean indicating if your command supports `SOCKS5` proxies.
* `proxy_http` : boolean indicating if your command supports `HTTP` / `HTTPS` proxies.
* `proxychains`: boolean indicating if your command supports being run with `proxychains`.

{% hint style="warning" %}
If your proxy supports `SOCKS5`or `HTTP` proxies, make sure to have an option called **`proxy`** in your **`opts`** definition or it won't be picked up.

If your proxy supports `proxychains`, `secator` will use the local `proxychains` binary and  `proxychains.conf` configuration, so make sure those are functional.
{% endhint %}

{% hint style="info" %}
Read [proxies.md](../../../in-depth/concepts/proxies.md "mention")for more details on how proxies work and how to configure them properly.
{% endhint %}

#### Example:

Assuming `mytool` does not support HTTP or SOCKS5 proxies, but works with `proxychains`, you can update your task definition like:

```python
@task()
class mytool(Command):
    # ...
    proxychains = True
    proxy_socks5 = False
    proxy_http = True
```

With the above configuration, running with `-proxy <VALUE>` would result in the following behaviour:

{% tabs %}
{% tab title="proxychains / auto" %}
```bash
secator x mytool -proxy proxychains TARGET
secator x mytool -proxy auto TARGET # auto-pick from proxychains > socks5 > http
```

becomes:

```bash
proxychains mytool -u TARGET
```
{% endtab %}

{% tab title="http" %}
```bash
secator x mytool -proxy "http://testmyproxy.com" <TARGET>
```

becomes:

```bash
mytool --use-proxy "http://testmyproxy.com" -u <TARGET>
```
{% endtab %}

{% tab title="random" %}
```bash
secator x mytool -proxy random <TARGET>
```

becomes:

```bash
mytool --use-proxy "http://30.10.23.42" -u <TARGET> # random proxy (FreeProxy)
```
{% endtab %}
{% endtabs %}

***

### Hooking onto runner lifecycle

You can hook onto any part of the runner lifecycle by override the hooks methods (read [#lifecyle-hooks](../../../in-depth/concepts/runners.md#lifecyle-hooks "mention") to know more).&#x20;

#### Example:

{% tabs %}
{% tab title="CLI" %}
```python
@task()
class mytool(Command):
    # ...
    @staticmethod
    def on_line(self, line):
        return line.rstrip(',')  # strip trailing comma of stdout lines

    @staticmethod
    def on_item_pre_convert(self, item):
        item['extra_data'] = {
            'version': '2.0'  # add extra data to items
        }
        return item

```
{% endtab %}

{% tab title="Python" %}
```python
from secator.tasks import mytool

hooks = {
    'on_line': lambda x: x.strip(','),
    'on_item_pre_convert': lambda x: x | {'extra_data': {'version': '2.0'}},
}
task = mytool('TARGET', hooks=hooks)
for item in task:
     print(item)

```
{% endtab %}
{% endtabs %}

***

### Chunking

`secator` allows to chunk a task into multiple children tasks when the length of the input grows, or some other specific requirements (e.g: your command only takes one target at a time).

{% hint style="warning" %}
Chunking only works when [distributed-runs-with-celery.md](../../../in-depth/distributed-runs-with-celery.md "mention") are enabled.
{% endhint %}

You can specify the chunk size using the `input_chunk_size` attribute:

```python
@task()
class mytool(Command):
    # ...
    input_chunk_size = 10  # additional tasks will be spawned every 10 targets

```

With this config, running:

```bash
secator x mytool tasks.txt  # tasks.txt contains 20 targets
```

would result in:

```bash
mytool -l /tmp/task_0_9.txt
mytool -l /tmp/task_10_19.txt
```

{% hint style="info" %}
If `mytool` did not support file input (i.e: `file_flag` not defined in the task definition class), the above would still work with an `input_chunk_size = 1`, thus splitting into one command per target passed.
{% endhint %}

***
