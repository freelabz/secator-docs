---
description: Instructions for running tests.
---

# Running tests

{% hint style="info" %}
You need to [#install-a-development-build](development-setup.md#install-a-development-build "mention") in order to run tests.
{% endhint %}

***

## Unit tests

<pre class="language-bash"><code class="lang-bash"><strong>secator test unit
</strong></code></pre>

If you want to run unit tests to test a specific task only:

```sh
secator test unit --test test_task --task <TASK_NAME>
```

***

## Integration tests

```bash
secator test integration
```

If you want to run integration tests to test a specific task only:

```sh
secator test integration --test test_tasks --tasks <TASK_NAME>
```

***

## Lint tests

```bash
secator test lint
```

***
