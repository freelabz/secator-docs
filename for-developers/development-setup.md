---
description: ... or how to setup a development environment for secator.
---

# Development setup

***

## Install a development build

To install `secator` in development mode, first make sure `pip` and `virtualenv` are installed, and run the following steps:

```bash
git clone https://github.com/freelabz/secator  # clone the repository
cd secator                                     # go to the repository folder
virtualenv .venv                               # create a virtualenv
source .venv/bin/activate                      # load the virtualenv
pip install -e .[dev]                          # install secator and dev dependencies
```

You can now run `secator health` to verify your installation. You can install addons / tools using the `secator install` command (choose what to install based on what you want to dev on).

***

## Running tests

### Unit tests

<pre class="language-bash"><code class="lang-bash"><strong>secator test unit
</strong></code></pre>

If you want to run unit tests to test a specific task only:

```sh
secator test unit --test test_task --task <TASK_NAME>
```

***

### Integration tests

```bash
secator test integration
```

If you want to run integration tests to test a specific task only:

```sh
secator test integration --test test_tasks --tasks <TASK_NAME>
```

***

### Lint tests

```bash
secator test lint
```

***
