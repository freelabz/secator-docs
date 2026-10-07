---
description: >-
  ... or how you can 10x your scanning speed and massively parallelize your
  workflows.
---

# Distributed runs with Celery

By default, `secator` runs all tasks synchronously. This guide shows how to enable distributed runs using Celery workers, which unlocks [#concurrent-tasks](../for-developers/writing-workflows.md#concurrent-tasks "mention").

***

## Prerequisite

To use distributed runs, make sure the `worker` addon is installed:

```bash
secator install addons worker
```

## Step 1: Configure a broker and result backend \[optional]

{% hint style="info" %}
This step is **optional**. If you do not configure a broker, the **file system** will be used as a broker and result backend. Note that this works only if the client and worker run on the same VM.
{% endhint %}

You can set up a task queue using Celery with the broker and a results backend of your choice, and run Celery workers to execute tasks from the broker queue.

The following is an example using `redis`, but you can use any [supported Celery broker and backend](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/index.html).

**Install `redis` addon:**

```bash
secator install addons redis
```

**Install `redis`:**

```sh
sudo apt install redis
```

**Start `redis` and enable at boot:**

```sh
sudo systemctl enable redis
sudo systemctl start redis
```

**Configure `secator` to use Redis:**

<pre class="language-sh"><code class="lang-sh"><strong>secator config set celery.broker_url redis://&#x3C;REDIS_IP>:6379/0
</strong>secator config set celery.result_backend redis://&#x3C;REDIS_IP>:6379/0
</code></pre>

{% hint style="warning" %}
Make sure you replace `<REDIS_IP>` in the variables above with the IP of your Redis server.
{% endhint %}

***

## **Step 2: Start a Celery worker**

```sh
secator worker
```

Useful options (see `secator worker --help`):

```sh
secator worker -c 4                  # 4 child processes
secator worker -Q small,medium       # only consume some queues
secator worker -n worker1@%h         # set a unique worker hostname
secator worker --check               # check that a worker is alive
```

***

## **Step 3: Run a task, workflow or scan**

{% tabs %}
{% tab title="CLI" %}
```bash
secator x httpx wikipedia.org
secator w host_recon wikipedia.org
secator s host wikipedia.org
```
{% endtab %}

{% tab title="Python" %}
```python
from secator.tasks import httpx
from secator.workflows import host_recon
from secator.scans import host

target = 'testphp.vulnweb.com'

for result in httpx(target, sync=False):
  print(result)

for result in host_recon(target, sync=False):
  print(result)
  
for result in host(target, sync=False):
  print(result)
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
If you want to run synchronously (bypassing the broker), you can use the `--sync` flag (CLI) or the `sync` kwarg (Python).
{% endhint %}

***

## Worker queues

Tasks are routed to Celery queues named after their resource **profile**:

| Queue         | Used for                                                              |
| ------------- | --------------------------------------------------------------------- |
| `small`       | Lightweight tasks (default for most tasks).                           |
| `medium`      | Heavier tasks (for instance `search_vulns`, `wpscan`, `trufflehog`).  |
| `large`       | Resource-hungry runs (for instance `httpx` with screenshots, or fuzzers with large wordlists). |
| `extra_large` | Very heavy tasks (for instance `katana` in headless mode).            |

Workflow and scan orchestration runs on the `celery` queue, result aggregation on the `results` queue, polling on the `poll` queue and MongoDB driver jobs on the `mongodb` queue: make sure at least one worker consumes each of them. By default `secator worker` consumes all queues, so a single worker handles everything. To size workers differently, run one worker pool per queue with `-Q`, for instance:

```sh
secator worker -Q celery,results,poll,mongodb,small -c 8
secator worker -Q medium,large,extra_large -c 2
```

To send a task to another queue, override its profile (see [#task-overrides](../getting-started/configuration.md#task-overrides "mention")):

```sh
secator config set tasks.overrides.nmap.profile large
```

{% hint style="info" %}
Task timeouts, memory limits and redelivery of tasks whose worker died are controlled by the `celery.task_*` and `celery.worker_*` options listed in the [configuration-reference.md](../getting-started/configuration-reference.md "mention").
{% endhint %}

***
