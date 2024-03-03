# Meta Options

**Meta options** are options that apply to tasks of the same category. Meta options can passed to tasks, workflows, or scans.

When passed to workflows or scans, they will be passed to each task contained in the runner.

***

## Network options

The following options will apply to all tasks making network (TCP / UDP / HTTP) requests:

{% hint style="info" %}
Some tasks making HTTP requests do not support some of the options mentioned below. Run**`secator x <task> --help`** for the complete list of supported options.
{% endhint %}

***

### Proxy (`-proxy`)

You can use an automatic proxy to use for each task:

```
secator x httpx mydomain.com -proxy auto
secator w host_recon mydomain.com -proxy auto
secator s host mydomain.com -proxy auto
```

{% hint style="info" %}
Learn more about [proxies.md](../in-depth/concepts/proxies.md "mention").
{% endhint %}

***

### Rate limit (`-rl`)

You can use a rate limit of 50 requests/second to use for each task:

```
secator x httpx mydomain.com -rl 50
secator w host_recon mydomain.com -rl 50
secator s host mydomain.com -rl 50
```

***

### Timeout (`-timeout`)

You can use a request timeout of 10 seconds to use for each task:

<pre><code><strong>secator x httpx mydomain.com -timeout 10
</strong></code></pre>

***

### Retries (`-retries`)

Retries is the number of retries for the port scan \[default: 3 ]

```bash
secator x naabu mydomain.com -retries [INT]
```

***

***

## HTTP Options

The following options will apply to all tasks making HTTP requests.

{% hint style="info" %}
Some tasks making HTTP requests do not support some of the options mentioned below. Run**`secator x <task> --help`** for the complete list of supported options.
{% endhint %}

***

### Header (`-header`)

Custom header to add to each request in the form "KEY1:VALUE1; KEY2:VALUE2"

```bash
secator x cariddi mydomain.com -header [TEXT]
```

***

### Method (`-method`)

HTTP method to use for request \[GET POST PUT DELETE]

```bash
secator x ffuf mydomain.com -method [METHOD]
```

***

### User-agent (`-ua`)

You can specific a custom user-agent on request \[Mozilla Firefox 1.0 ]

```bash
secator x dalfox mydomain.com -ua Mozilla Firefox 1.0
```

***

### **Match regex (`-mr)`**

Keep responses which body content match the regex input as argument:

```
secator x ffuf mydomain.com -mr MySQLError.*
```

***

### Match size (`-ms`)

Keep responses which body size match the size input as argument:

```bash
secator x katana mydomain.com -ms 1026  # bytes
```

***

### Match-words (`-mw)`

Keep responses which size match the word count input as argument:

```bash
secator x katana mydomain.com -mw 10
```

***

### Match code (`-mc`)

Keep responses which status codes match the codes input as argument:

```bash
secator x katana mydomain.com -mc 200,400,501
```

***

### Filter regex (`-fr`)

Test the body of the request and filter out responses with regular expression

```bash
secator x katana mydomain.com -fr 
```

***

### Filter codes (`-fc`)

Test the body of the request and filter out responses with HTTP codes.

```bash
secator x katana mydomain.com -fc [TEXT]
```

***

#### Filter size (`-fs)`

Test the body of the request and filter out responses with size

```bash
secator x katana mydomain.com -fs [NUMBER]
```

***

### Filter words (`-fw`)

Test the body request and filter out responses with word count

```bash
secator x katana mydomain.com -fw [NUMBER]
```

***

### Follow redirect (`-frd`)

This option follow all http redirect

```bash
secator x katana mydomain.com -frd
```

***

### Wordlist (`-w`)

To use a wordlist the default path is write like this : /usr/share/seclists/Fuzzing/fuzz-Bo0oM.txt

```bash
secator x ffuf mydomain.com/FFUF/ -w /usr/share/seclists/Fuzzing/fuzz-Bo0oM.txt
```

{% hint style="info" %}
This option only applies to HTTP Fuzzers.
{% endhint %}

***
