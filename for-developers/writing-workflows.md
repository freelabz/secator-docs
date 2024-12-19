---
description: ... or how to integrate new workflows with secator.
---

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

### Finding the Original Workflow Files

The original YAML workflow files provided by secator are located in the installed library directory, typically under:

```
**/python3.11/site-packages/secator/configs/workflows/*.yaml
```

To locate these files on your system, you can use the following command:

```bash
find / -type f -path "*/secator/configs/workflows/*" -name "*.yaml"
```

This command will search your filesystem for YAML files under the `secator/configs/workflows` path.

### Adding Your Own Workflows

You can add your custom workflows by placing their YAML files in:

* `~/.secator/templates/` (or whatever your `dirs.templates` in [configuration.md](../../../getting-started/configuration.md "mention") points to)

This allows you to extend the functionality of secator without modifying the original library files, making it easier to manage updates and custom configurations.

## Dynamic targets

You can specify dynamic targets for tasks from current run results, by using the `targets_` key in your template like:

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

* `type` is the output type, lower-case (see [Broken link](broken-reference "mention") for the whole list)
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
  katana:
  _group:
    gf:
      ...
    another_task:
      description: Runs concurrently with the `gf` task
```

In this configuration, the `katana`task will begin the run, followed by a grouped execution of `gf` and `another_task`.

{% hint style="info" %}
Concurrent tasks require`secator` to be setup in worker mode (see [distributed-runs-with-celery.md](../in-depth/distributed-runs-with-celery.md "mention")).
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

{% hint style="warning" %}
Filters apply to final run results sent to [exporters.md](../in-depth/concepts/exporters.md "mention"), but do not apply to real-time results sent to [drivers.md](../in-depth/concepts/drivers.md "mention").
{% endhint %}

***
