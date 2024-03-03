# Writing workflows

New `secator` workflows should be easy to write to promote contributions from the community.&#x20;

Eventually we aim for our workflow library to become a reference in cyber-security much like Nuclei templates have become a reference for vulnerability searching.

***

## Basic YAML definition

`secator` workflows are defined through YAML configs:

{% code title="secator/configs/workflows/url_finder.yaml" %}
```yaml
type: workflow
name: url_finder
alias: ufind
description: URL finder and tagger
tags: [http]
input_types:
  - url
tasks:
  katana:
    description: Find URLs
    rate_limit: 100
    timeout: 1
  gf:
    description: Tag URLs
    pattern: xss
```
{% endcode %}

***

## Dynamic targets

You can specify dynamic targets for tasks using based on the current run results, by using the `targets_` key in your template like:

```yaml
...
tasks:
  ...
  gf:
    description: Tag URLs found by the previous task
    targets_:  # use previously found URLs
    - type: url
      field: url
      condition: item.status_code == 200
```

{% hint style="info" %}
The dynamic format keys are:

* `type` is the output type, lower-case (see [output-types.md](../in-depth/concepts/output-types.md "mention") for the whole list)
* `field` is the JSON field to use as target
* `condition` is the filtering condition.
{% endhint %}

***

## Concurrent tasks

You can specify tasks that run in parallel using the `_group` key:

```yaml
...
tasks:
  ...
  _group:
    gf:
      ...
    another_task:
      description: Runs concurrently with the `gf` task
```

In this configuration, the `katana`task will begin the run, followed by a grouped execution of `gf` and `another_task`.

{% hint style="info" %}
Parallel tasks specified with the `_group` key will run in parallel only when `secator` is in worker mode (see [distributed-runs-with-celery.md](../in-depth/distributed-runs-with-celery.md "mention")).
{% endhint %}

***

## Result filtering

You can customize which results you want to keep for workflows and scans by adding the `results` key to the respective runner YAML configuration:

<pre class="language-yaml"><code class="lang-yaml"><strong>...
</strong><strong>results:
</strong>- type: ip
  condition: item.alive
- type: url
  condition: item.status_code == 200
</code></pre>

{% hint style="info" %}
Filters apply to final run results sent to [exporters.md](../in-depth/concepts/exporters.md "mention"), but do not apply to real-time results sent to [hooks-and-drivers.md](../in-depth/concepts/hooks-and-drivers.md "mention").
{% endhint %}

***
