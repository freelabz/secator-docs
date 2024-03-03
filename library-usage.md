# Library usage

`secator` can also be used as a Python library.&#x20;

{% hint style="info" %}
We recommend using `secator` as a library when building complex systems around `secator` to overcome CLI limitations.
{% endhint %}

***

## **Using a command as a generator**

Since most commands yield results live, we can run them as a generator by simply calling them in a `for` loop like, and consume results lazily with e.g a Celery task.

```python
from secator.tasks.http import ffuf
from .models import Urls

app = Celery(__name__)

@app.task
def process_url(url):
    Urls.objects.create(**url)

host = 'wikipedia.org'
for url in ffuf(host):
    process_url.delay(url)
```

{% hint style="info" %}
All commands support being run like generators, even if some of them have to wait for the command to finish before outputting results (e.g: `nmap`).
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
