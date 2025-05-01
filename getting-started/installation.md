---
description: ... or how to install secator and it's dependencies on different platforms.
---

# Installation

***

## Installing secator

{% tabs %}
{% tab title="Pipx" %}
```bash
pipx install secator
```
{% endtab %}

{% tab title="Pip" %}
```bash
pip install secator
```
{% endtab %}

{% tab title="Bash" %}
```bash
wget -O - https://raw.githubusercontent.com/freelabz/secator/main/scripts/install.sh | sh
```
{% endtab %}

{% tab title="Docker" %}
```bash
docker run -it --rm --net=host -v ~/.secator:/root/.secator freelabz/secator --help
```

{% hint style="info" %}
The volume mount `-v` is necessary to save all `secator` reports to your host machine, and`--net=host` is recommended to grant full access to the host network.
{% endhint %}

You can alias this command to run it easier:

```
alias secator="docker run -it --rm --net=host -v ~/.secator:/root/.secator freelabz/secator"
```

Now you can run `secator` like if it was installed on baremetal:

```
secator --help
```
{% endtab %}

{% tab title="Docker Compose" %}
<pre class="language-bash"><code class="lang-bash">git clone https://github.com/freelabz/secator
cd secator
<strong>docker-compose up -d
</strong><strong>docker-compose exec secator secator --help
</strong></code></pre>
{% endtab %}
{% endtabs %}

{% hint style="success" %}
If you chose the Bash, Docker, or Docker Compose installation methods, you can jump straight to [cli-usage.md](cli-usage.md "mention").
{% endhint %}

***

## Installing languages (optional)

`secator` uses external tools, so you might need to install languages used by those tools assuming they are not already installed on your system.

We provide a subcommand to install required languages if you don't manage them externally:

<pre class="language-bash"><code class="lang-bash"><strong>secator install langs go   # install Go
</strong>secator install langs ruby # install Ruby
</code></pre>

***

## Installing tools (optional)

`secator` can install tools automatically at runtime (provided `security.auto_install_commands` is enabled, which is the default), but you can also do it manually.

We provide a subcommand to install or update each supported tool which should work on all systems supporting `apt`:

```bash
secator install tools httpx  # install httpx
secator install tools        # install all supported tools
```

***

## Installing addons (optional)

`secator` comes installed with the minimum amount of dependencies.

We provide a subcommand to install additional addons which are required for various features:

{% tabs %}
{% tab title="worker" %}
Add support for Celery (see [distributed-runs-with-celery.md](../in-depth/distributed-runs-with-celery.md "mention")).

```sh
secator install addons worker
```
{% endtab %}

{% tab title="google" %}
Add support for Google Drive exporter (see [exporters.md](../in-depth/concepts/exporters.md "mention")).

```sh
secator install addons google
```
{% endtab %}

{% tab title="mongodb" %}
Add support for MongoDB driver (see [#mongodb-driver](../in-depth/concepts/drivers.md#mongodb-driver "mention")).

```sh
secator install addons mongodb
```
{% endtab %}

{% tab title="redis" %}
Add support for Celery Redis broker / backend.

```sh
secator install addons redis
```
{% endtab %}

{% tab title="dev" %}
Add development tools like `coverage` and `flake8` required for running tests.

```sh
secator install addons dev
```
{% endtab %}

{% tab title="trace" %}
Add tracing tools like `memray` and `pyinstrument` required for tracing functions.

```sh
secator install addons trace
```
{% endtab %}
{% endtabs %}

***

## Checking installation health

To figure out which languages or tools are installed on your system (along with their version):

```bash
secator health
```

<div align="left"><figure><img src="../.gitbook/assets/2025-04-29 15_55_22-Debian 10.x 64-bit - VMware Workstation.png" alt=""><figcaption><p>Secator Health CLI Output</p></figcaption></figure></div>

***
