# Philosophy & design

***

## Why do we need another tool ?

Traditional pentesting sessions can be a pain:

* Use of dozens of commands (each very good at what it does)
* Each command has different options
* Each command outputs results in a different format

Here is for instance a basic host scan that we run day-to-day on many targets:

{% tabs %}
{% tab title="Standard" %}
<pre class="language-bash"><code class="lang-bash"><strong>naabu -Pn -silent -host example.com -json -rate 10 -c 50 > open_ports.txt
</strong>nuclei -silent -sj -si 20 -hm -u example.com -jsonl -tags network,ssl -proxy socks5://tor-privoxy:9050 -rate-limit 10 -c 50
httpx -silent -td -asn -cdn -l open_ports.txt -json -proxy socks5://tor-privoxy:9050 -rate-limit 10 -threads 50 -match-code 200,204,301,302,307,401,403,405,500
katana -silent -jc -js-crawl -known-files all -u example.com -json -proxy socks5://tor-privoxy:9050 -rate-limit 10 -concurrency 50
echo https://example.com | cariddi -info -s -err -e -ext 1 -json -proxy socks5://tor-privoxy:9050 -c 50
</code></pre>
{% endtab %}

{% tab title="Secator" %}
```bash
secator s host example.com -json -proxy socks5://tor-privoxy:9050 -rl 10 -threads 50 -mc 200,204,301,302,307,401,403,405,500
```
{% endtab %}
{% endtabs %}

With `secator` the goal is to unify all these awesome tools by creating an abstract layer for input and output, such that all tools "speak" the same language and we can mutualize options that will apply to all tools, unlocking the ability to run complex workflows.

***

## Who is it made for ?

* [x] Bug-bounty hunters
* [x] Pentesters
* [x] Security researchers
* [x] Companies of any size

***

## Why is the license BSL ?

We believe in open-source 100%.&#x20;

Freelabz founders have written code for open-source for as long as they started working in the tech industry. `secator` is and will remain free-to-use, forkable and open to community contributions forever, and we believe in the collective to make it one of the de-facto tools in the security world.

However, Freelabz is a young company that is seeking to make a living and pay its workers correctly. We are working on a paid product derived from `secator` and BSL allows us to restrict commercial uses of `secator` by big tech actors who could profit from its success.  All standard OSS rules still apply, which means you can still read / fork / modify it and even use it in production **as long as you don't sell a service based on it**.&#x20;

Feel free to reach out to us if you want to use `secator` in a commercial tool, and we will review your request on a case-by-case basis.

***

## Design principles

### **Curated list of tools**

Tools integrated to `secator` <mark style="color:red;">**MUST**</mark> be <mark style="color:orange;">**fast**</mark>, <mark style="color:orange;">**efficient**</mark>, <mark style="color:orange;">**well-maintained**</mark>, and have <mark style="color:orange;">**structured output**</mark> (either `JSON`, `JSON lines`, `CSV`, or `XML`).

{% hint style="info" %}
We do make exceptions for really awesome tools and write custom parsers (e.g: `nmap`).
{% endhint %}

### **Unified input options**

`secator` tools belonging to the same category (eg: fuzzers) <mark style="color:red;">**MUST**</mark> end up with <mark style="color:orange;">**mutualized**</mark> [<mark style="color:orange;">**input options**</mark>](../more-options/input-formats.md), while still retaining the capability to use unique options for each command.

### **Unified output schema**

Tools belonging to the same category <mark style="color:red;">**MUST**</mark> have <mark style="color:orange;">**unified**</mark> [<mark style="color:orange;">**output types**</mark>](concepts/output-types.md), allowing you to run multiple commands and aggregate results quickly.

### **CLI and library usage**

When `secator` is called as a library from other Python code, the output <mark style="color:red;">**MUST**</mark> be <mark style="color:orange;">**structured**</mark> (list of dicts). Results <mark style="color:red;">**MUST**</mark> also be yielded in <mark style="color:orange;">**realtime**</mark>.

When `secator` is called as a CLI, various [output formats](../more-options/output-options.md) <mark style="color:red;">**MUST**</mark> be available, such as <mark style="color:orange;">**csv**</mark>, <mark style="color:orange;">**json**</mark>, <mark style="color:orange;">**txt**</mark>, or <mark style="color:orange;">**table**</mark>.

### **Distributed options**

`secator` <mark style="color:red;">**MUST**</mark> work in both <mark style="color:orange;">**synchronous**</mark> mode (default) and [<mark style="color:orange;">**distributed**</mark> ](distributed-runs-with-celery.md)mode.

Switch from synchronous to distributed when you want to increase the scanning speed <mark style="color:red;">**MUST**</mark> be easy, by simply [configuring Celery worker with your broker and results backend of choice](distributed-runs-with-celery.md#step-1-configure-a-broker-optional).

### **From simple tasks to complex workflows**

`secator` <mark style="color:red;">**MUST**</mark> be useful for <mark style="color:orange;">**running simple tasks**</mark> like in CTFs, bug-bounties or hackathon, or to <mark style="color:orange;">**automate entire workflows**</mark>.

### **Customizable**

`secator` <mark style="color:red;">**MUST**</mark> be <mark style="color:orange;">**customizable**</mark>, so that the community can contribute tasks, workflows, and scans to the repo if they can serve the greater good.

***
