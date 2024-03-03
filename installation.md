---
description: Steps to install secator on a fresh environment
---

# Installation

***

## Installing secator

{% tabs %}
{% tab title="Pip" %}
```bash
pip3 install secator
```
{% endtab %}

{% tab title="Docker" %}
```bash
# Run secator commands with:
docker run -it freelabz/secator [SUBCOMMAND] [OPTIONS]

# ... or use the docker-compose deployment for a Redis + worker setup
docker-compose up -d
docker-compose exec secator secator w host_recon mydomain.com
```
{% endtab %}

{% tab title="Bash" %}
{% hint style="info" %}
This script also install Go, Ruby, a Python virtual env for `secator` and all `secator` supported commands.
{% endhint %}

```bash
git clone https://github.com/freelabz/secator && sh ./secator/scripts/install.sh
```
{% endtab %}

{% tab title="Dev build" %}
```bash
# Clone the repository
git clone https://github.com/freelabz/secator
cd secator

# Create a venv
python3 -m virtualenv -p python3 ~/.virtualenvs/secator

# Activate venv
source ~/.virtualenvs/secator/bin/activate

# Install secator lib + deps
pip3 install -e .

# Run secator
secator --help

# Run a worker in a separate terminal to use distributed mode
secator worker
```
{% endtab %}
{% endtabs %}

***

## Installing supported commands

By default, `secator` does not install any of the commands it supports.

If you are using Kali, most commands will already be installed on the system and we do not want to tamper with their installation.

However, we provide utilities to install each supported commands which should work on all Debian systems supporting `apt`:

```
secator utils install httpx  # install httpx
secator utils install        # install all supported commands
```

{% hint style="info" %}
If you chose the Docker or Bash one-liner installation methods, all supported commands should have been installed automatically.
{% endhint %}

Please make sure you are using the latest available versions for each tool before you run `secator` or you might run into parsing / formatting issues.
