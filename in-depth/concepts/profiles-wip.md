# Profiles \[WIP]

{% hint style="info" %}
This page is a Work In Progress. Profiles are not yet integrated with `secator`.
{% endhint %}

`secator` profiles are a way to mutualize sets of options to be quickly re-used in tasks, workflows, and scans.

We have identified that for different security assessment we need vastly different option set.

For instance, we could imagine scan profiles focused on scan **speed** / **aggressivity** playing on the `rate_limit` and `delay` options:

{% tabs %}
{% tab title=" 🐆 Jaguar" %}
```yaml
type: profile
name: jaguar
opts:
    rate_limit: 100000
    delay: 0
```
{% endtab %}

{% tab title="🐇 Rabbit" %}
```yaml
type: profile
name: rabbit
opts:
    rate_limit: 1000
    delay: 1
```
{% endtab %}

{% tab title="🐢 Turtle" %}
```yaml
type: profile
name: turtle
opts:
    rate_limit: 10
    delay: 2
```
{% endtab %}

{% tab title="🐌 Snail" %}
```yaml
type: profile
name: snail
opts:
    rate_limit: 1
    delay: 5
```
{% endtab %}
{% endtabs %}

... or scan profiles focused on **furtivity** / **stealth**:

{% tabs %}
{% tab title="🥷  Ninja" %}
```yaml
type: profile
name: ninja
opts:
    proxy: auto
    tor: true
    vpn: true
```
{% endtab %}

{% tab title="🦎 Chameleon" %}
```yaml
type: profile
name: chameleon
opts:
    proxy: auto
    tor: true
    vpn: false
```
{% endtab %}

{% tab title="🐁 Mouse" %}
```yaml
type: profile
name: mouse
opts:
    proxy: auto
    tor: false
    vpn: false
```
{% endtab %}

{% tab title="🐘 Elephant" %}
```yaml
type: profile
name: elephant
opts:
    proxy: false
    tor: false
    vpn: false
```
{% endtab %}
{% endtabs %}

Running a task / workflow / scan with profiles be like:

{% tabs %}
{% tab title="Task" %}
```bash
secator x httpx -profiles ninja,jaguar
```
{% endtab %}

{% tab title="Workflow" %}
```bash
secator w host_recon -profiles ninja,jaguar
```
{% endtab %}

{% tab title="Scan" %}
```bash
secator s host_recon -profiles ninja,jaguar
```
{% endtab %}
{% endtabs %}
