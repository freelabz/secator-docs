---
description: ... or how to pass targets to secator.
---

# Input formats

`secator` is built to be flexible in terms of input formats.

***

## **Direct input**

Inputs can be passed directly as an argument to the command / workflow / scan you wish to run:

```sh
secator x httpx example.com # single input
secator x httpx example.com,example2.com,example3.com # multiple comma-separated inputs
```

***

## **File input**

Input can also be passed from a file containing one item per line:

```sh
secator x httpx urls.txt
```

***

## **Stdin input**

Input can also be passed directly from `stdin`:

```sh
cat urls.txt | secator x httpx
```

This also means you can build basic workflow using UNIX pipes and the [`-raw`](broken-reference) output format:

<figure><img src="../.gitbook/assets/pipe.gif" alt=""><figcaption><p>Example of a piped workflow</p></figcaption></figure>

{% hint style="info" %}
For more complex workflows, we highly recommend using the YAML-based workflow definitions or the code-based workflow definitions (see [writing-workflows.md](../for-developers/writing-workflows.md "mention")).
{% endhint %}

***
