# Global options

**Global options** apply to most tasks and will be respected by any task which is part of the run, assuming the task supports the option.

***

## Workspace (`-ws`)

You can pass a workspace name to use for the runner:

{% tabs %}
{% tab title="Task" %}
```bash
secator x httpx mydomain.com -ws mydomain
```
{% endtab %}

{% tab title="Workflow" %}
```bash
secator w host_recon mydomain.com -ws mydomain
```
{% endtab %}

{% tab title="Scan" %}
```bash
secator s domain mydomain.com -ws mydomain
```
{% endtab %}
{% endtabs %}

***

## Threads (`-threads`)

You can set the number of threads to use for each task:

{% tabs %}
{% tab title="Task" %}
```bash
secator x httpx mydomain.com -threads 50
```
{% endtab %}

{% tab title="Workflow" %}
```bash
secator w host_recon mydomain.com -threads 50
```
{% endtab %}

{% tab title="Scan" %}
```bash
secator s domain mydomain.com -threads 50
```
{% endtab %}
{% endtabs %}

***

## Exporters (`-o`)

You can export results in various formats using exporters.

{% tabs %}
{% tab title="Task" %}
```bash
secator x httpx mydomain.com -o table,csv,json
```
{% endtab %}

{% tab title="Workflow" %}
```bash
secator w host_recon mydomain.com -o table,csv,json
```
{% endtab %}

{% tab title="Scan" %}
```bash
secator s domain mydomain.com -o table,csv,json
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
Learn more about [exporters.md](../in-depth/concepts/exporters.md "mention").
{% endhint %}

***

## Drivers (`-driver`)

You can route live results to different targets using drivers.

{% tabs %}
{% tab title="Task" %}
```bash
secator x httpx mydomain.com -driver mongodb
```
{% endtab %}

{% tab title="Workflow" %}
```bash
secator w host_recon mydomain.com -driver mongodb
```
{% endtab %}

{% tab title="Scan" %}
```bash
secator s domain mydomain.com -driver mongodb
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
Learn more about [#drivers](../in-depth/concepts/hooks-and-drivers.md#drivers "mention").
{% endhint %}
