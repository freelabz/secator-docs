# Distributed runs with Celery

By default, `secator` runs all tasks synchronously. This guide shows how to enable distributed runs using Celery workers, which unlocks [#concurrent-tasks](../for-developers/writing-workflows.md#concurrent-tasks "mention").

***

## Step 1: Configure a broker \[optional]

{% hint style="info" %}
This step is _optional_. If you do not configure a broker, the **file system** will be used as a broker and result backend. Note that this works only if the client and worker run on the same VM.
{% endhint %}

You can set up a task queue using Celery with the broker and a results backend of your choice, and run Celery workers to execute tasks from the broker queue.

The following is an example using `redis`, but you can use any [supported Celery broker and backend](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/index.html).

**Install `worker`  and `redis`   addons:**

```
secator install addons worker
secator install addons redis
```

\
**Install `redis`:**

```sh
sudo apt install redis
```

\
**Start `redis` and enable at boot:**

```sh
sudo systemctl enable redis
sudo systemctl start redis
```

\
**Configure `secator` to use Redis:**

Create a `.env` file in the directory where you run `secator`, and fill it like so:

<pre class="language-sh"><code class="lang-sh"><strong>CELERY_BROKER_URL=redis://&#x3C;REDIS_IP>:6379/0
</strong>CELERY_RESULT_BACKEND=redis://&#x3C;REDIS_IP>:6379/0
</code></pre>

{% hint style="info" %}
Make sure you replace `<REDIS_IP>` in the variables above with the IP of your Redis server.
{% endhint %}

***

## **Step 2: Start a Celery worker**

```sh
secator worker
```

***

## **Step 3: Run a task, workflow or scan**

{% tabs %}
{% tab title="CLI" %}
```bash
secator w host_scan wikipedia.org
```
{% endtab %}

{% tab title="Python" %}
```python
from secator.runners import Workflow
from secator.config import ConfigLoader

config = ConfigLoader(name='workflows/host_scan')
workflow = Workflow(config)
results = workflow.run()
print(results)
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
If you want to run synchronously (bypassing the broker), you can use the `--sync` flag (CLI) or the `sync` kwarg (Python).
{% endhint %}
