---
description: ... or how to control how secator connects to targets.
---

# Proxies

`secator` provides a range of proxy options to choose from, by passing the `-proxy` option to any runner (task, workflow, scan).

***

## Auto

Using `-proxy auto` for a `secator` run will result in auto-detecting the right proxy to pass to each task. This is the recommended option for most runs.

The defaults to use for proxies in `auto` mode are set through config variables:

* <pre class="language-bash"><code class="lang-bash"><strong>secator config set http.socks5_proxy socks5://tor-privoxy:9050
  </strong></code></pre>
* ```bash
  secator config set http.http_proxy http://tor-privoxy:8118
  ```

#### **Example**

Running `secator w host_recon <TARGET> -proxy auto` will result in the following behavior:

* `naabu` supports Socks5 / HTTP proxy, but not proxychains, so it will use the first available SOCKS5 / HTTP proxy.
* `nmap` supports proxy through `proxychains4` but has no good support for proxychains, HTTP or Socks5 proxy, so it will use `proxychains4` for the execution.
* ...

***

## HTTP

You can pass an HTTP proxy to a task / workflow / scan by using `-proxy http://<PROXY_IP>:<PROXY_PORT>`.

***

## Socks5

You can pass a SOCKS5 proxy to a task / workflow / scan by using `-proxy socks5://<PROXY_IP>:<PROXY_PORT>`.

***

## Proxychains

You can pass `-proxy proxychains` to a task / workflow / scan by using `-proxy proxychains`. Remember to configure your `/etc/proxychains.conf` in that configuration, and test it prior to running `secator` tasks.

***
