---
description: ... or concrete use cases for secator.
---

# Examples

***

### **Find subdomains using `subfinder` and run HTTP probes using `httpx`**

{% tabs %}
{% tab title="CLI" %}
```bash
secator x subfinder -raw alibaba.com | secator x httpx -rl 10 -ss
```
{% endtab %}

{% tab title="Python" %}
```python
from secator.tasks import subfinder, httpx

target = 'alibaba.com'
results = subfinder(target).run()
hosts = [_.host for _ in results if _._type == 'subdomain']
for probe in httpx(hosts, rate_limit=10, screenshot=True):
    print('Found alive subdomain URL {url}[{status_code}]'.format(**probe))
```
{% endtab %}
{% endtabs %}

***

### **Run host reconnaissance workflow**

{% tabs %}
{% tab title="CLI" %}
```bash
secator w host_recon cnn.com
```
{% endtab %}

{% tab title="Python" %}
```python
from secator.workflows import host_recon

target = 'cnn.com'
for result in host_recon(target):  # consume results live
    print(result)
```
{% endtab %}
{% endtabs %}

***

### **Fuzz URLs with multiple fuzzers and a custom wordlist**

{% tabs %}
{% tab title="CLI" %}
```bash
secator w url_fuzz example.com -mc 200,302 -rl 1 -w dicc.txt -o table -quiet 
```
{% endtab %}

{% tab title="Python" %}
<pre class="language-python"><code class="lang-python">from secator.workflows import url_fuzz
<strong>
</strong>target = 'example.com'
opts = {
    'match_codes': '200, 302',
    'rate_limit': 1 # req/s
    'quiet': True,
    'ffuf.wordlist': 'dicc.txt' # ffuf wordlist
}

# Print results live and a summary table at the end of the run
for result in url_fuzz(target, exporters=['table']):
    print(result)
</code></pre>
{% endtab %}
{% endtabs %}

***
