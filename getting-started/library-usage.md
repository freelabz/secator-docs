---
description: >-
  ... or how you can use secator as a foundation to build powerful security
  software.
---

# Library usage

`secator` can also be used as a Python library.&#x20;

{% hint style="info" %}
We recommend using `secator` as a library when building complex systems around `secator` to overcome CLI limitations.
{% endhint %}

***

## **Running tasks, workflows, and scans**

You can run any task supported by `secator` by simply importing it by name from `secator.tasks`.&#x20;

You can run any workflow or scan by loading it's YAML configs and running it using the `secator.runners.Workflow` or `secator.runners.Scan` class.

```python
from secator.template import TemplateLoader
from secator.runners import Workflow
from secator.tasks import subfinder, httpx, naabu
from secator.workflows import host_recon
from secator.scans import host

# Run simple tasks, chain them together
target = 'wikipedia.org'
subdomains = subfinder(target).run()
alive_urls = httpx(subdomains).run()
ports_open = naabu(subdomains).run()

# ... or run a workflow
results = host_recon(target).run()

# ... or run a scan
config = host(target).run()

# ... or run any custom template by loading it dynamically
config = TemplateLoader('/path/to/my/workflow.yaml')
results = Workflow(config, target).run()
```

***

## Consuming results live

All runners yield results in real-time, which means you can run use them as generators to consume their results:

For instance, you can consume results lazily using threads or a Celery task:

{% tabs %}
{% tab title="Using threads" %}
```python
from threading import Thread
from secator.tasks import feroxbuster
from secator.workflows import url_crawl
from secator.output_types import Url, Tag
from .models import Urls, Tags

def process_url(url):
    Urls.objects.create(**url)
    print(f'Saved {url.url} [{url.status_code}] to database')
    
def process_tag(tag):
    Tags.objects.create(**tag)
    print(f'Found tag {tag.name} for target {tag.match}')

# Set the initial host
host = 'http://testphp.vulnweb.com'

# Use a task as a generator
for url in feroxbuster(host, rate_limit=100):
    Thread(target=process_url, args=(url,))

# Use a workflow as a generator
threads = []
for result in url_crawl(host, rate_limit=100):
  if isinstance(result, Url):
    thread = Thread(target=process_url, args=(result,))
  elif isinstance(result, Tag):
    thread = Thread(target=process_tag, args=(result,))
  threads.append(thread)
  thread.start()
  
for thread in threads:
  thread.join()
```
{% endtab %}

{% tab title="Using a Celery task" %}
```python
from celery import Celery
from secator.tasks.http import ffuf
from secator.output_types import Url, Tag
from .models import Urls, Tags
from secator.workflows import url_crawl

app = Celery(__name__)

@app.task
def process_url(url):
    Urls.objects.create(**url)
    print(f'Saved {url.url} [{url.status_code}] to database')

@app.task
def process_tag(tag):
    Tags.objects.create(**tag)
    print(f'Found tag {tag.name} for target {tag.match}')

# Set the initial host
host = 'http://testphp.vulnweb.com'

# Use a task as a generator
for url in feroxbuster(host, rate_limit=100):
    process_url.delay(url)

# Use a workflow as a generator
for result in url_crawl(host, rate_limit=100):
  if isinstance(result, Url):
    process_url.delay(result)
  elif isinstance(result, Tag):
    process_tag.delay(result)
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
All tasks support being run like generators, but some of them have to wait for the command to finish before outputting results (e.g: `nmap`).
{% endhint %}

***

## **Overriding global options**

Options specified with the name of the command name prefixed will override global options for that specific command.

For instance, if you want a global rate limit of `1000` (reqs/s), but for ffuf you want it to be `100` you can do so:

```python
from secator.tasks.http import ffuf, gau, gospider, katana
host = 'wikipedia.org'
options = {
    'rate_limit': 1000, # reqs/s
    'ffuf.rate_limit': 100,
    'katana.rate_limit': 30
}
for tool in [ffuf, gau, gospider, katana]:
    tool(host, **options)
```

{% hint style="info" %}
In the example above:

* `gau`, and `gospider` will have a rate limit of `1000` requests / second.
* `ffuf` will have a rate limit of `100` requests / second.
* `katana` will have a rate limit of `30` requests / second.
{% endhint %}

***

## **Disabling default options**

Sometimes you might wish to omit passing the option and use the command defaults. You can set the option to `False` in order to do this.

```python
options = {
    'rate_limit': 1000, # reqs/s
    'ffuf.rate_limit': False, # explicitely disabling `rate_limit` option, will use ffuf defaults
}
```

***
