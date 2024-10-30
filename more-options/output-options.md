---
description: ... or how to change secator's console output.
---

# Output options

`secator` is built to be flexible in terms of output options.

***

### Console

The default `secator` output is the [output-types.md](../in-depth/concepts/output-types.md "mention") `repr` function. It is supposed to be pretty and readable to quickly understand `secator`'s findings:

<div align="left">

<figure><img src="../.gitbook/assets/2023-07-05 15_47_29-● 🔓 mydomain.com_554 • Untitled-1 - Untitled (Workspace) - Visual Studio Code.png" alt=""><figcaption><p>Console output</p></figcaption></figure>

</div>

Unicode icons are printed before each result to distinguish each output type:

* [#exploit](../in-depth/concepts/output-types.md#exploit "mention")
* [#ip](../in-depth/concepts/output-types.md#ip "mention")
* [#port](../in-depth/concepts/output-types.md#port "mention")
* [#record](../in-depth/concepts/output-types.md#record "mention")
* [#subdomain](../in-depth/concepts/output-types.md#subdomain "mention")
* [#tag](../in-depth/concepts/output-types.md#tag "mention")
* [#url](../in-depth/concepts/output-types.md#url "mention")
* [#useraccount](../in-depth/concepts/output-types.md#useraccount "mention")
* [#vulnerability](../in-depth/concepts/output-types.md#vulnerability "mention")

When an output type has a low `confidence`, the output will be dimmed:

<div align="left" data-full-width="false">

<figure><img src="../.gitbook/assets/vuln_dimmed.png" alt=""><figcaption></figcaption></figure>

</div>

***

### JSON lines (`-json`)

You can use `-json` to output live results as JSON lines:

```bash
secator x httpx example.com -json
```

{% hint style="info" %}
JSON lines output is pipeable / streameable to other tools like `jq`.
{% endhint %}

***

### Raw (`-raw`)

You can use `-raw`to output live results in plaintext format:

```
secator x httpx example.com -raw
```

{% hint style="info" %}
Raw output is saveable to txt files or can be used for chaining tasks using UNIX pipes.
{% endhint %}

***

### Custom format (`-fmt`)

You can use `-fmt`to output live results in a format of your choice:

```bash
secator x naabu example.com -fmt '{host}:{port} -> {service_name}'
```

{% hint style="info" %}
Custom formatting is based on the [output-types.md](../in-depth/concepts/output-types.md "mention") fields.
{% endhint %}

***
