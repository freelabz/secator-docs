---
description: >-
  ... or how to scan targets that aren't reachable from the platform, and
  still see the runners and findings show up there.
---

# Running internal scans and getting results on the platform

The Secator platform (Secator Cloud, or a self-hosted deployment of
`secator-api`/`secator-ui`) dispatches and executes scans through its own
worker fleet. That fleet can only reach what it has network access to — so an
internal/private target (an RFC1918 range, a VPN-only host, an on-prem
service) usually isn't reachable from it.

This page covers two ways to scan those targets from **outside** the platform
while still getting the runners and findings to show up **on** the platform:

* [**Method A — the `api` driver**](#method-a-the-api-driver): run `secator`
  wherever it *can* reach the target (your laptop, a jump box, an on-prem
  VM), and have it POST runners/findings straight to the platform's API. Works
  for **both Secator Cloud and self-hosted** deployments.
* [**Method B — custom queue prefixes**](#method-b-custom-queue-prefixes-self-hosted-only):
  for a **self-hosted** deployment, deploy a dedicated worker that sits on
  your internal network (so it already has a path to the target) and route
  specific scans to it. Not available on multi-tenant Secator Cloud, since it
  requires direct access to the deployment's Celery broker.

***

## Method A — the `api` driver

This is the same mechanism the platform's own workers already use to persist
runners and findings — you're just running it from a client instead of from
inside the platform. See [Drivers](concepts/drivers.md) for the general
concept.

### Prerequisite: network access to the platform's API

The machine running `secator` needs outbound HTTP(S) access to the platform's
API endpoint:

* Secator Cloud: `https://app.secator.cloud/api` (the default, no config
  needed).
* Self-hosted: your deployment's `secator-api` URL.

If the runner sits behind a restrictive firewall/proxy, add an allow-rule (or
point it at an egress proxy) for that one endpoint — `secator`'s HTTP client
is a standard `requests` session, so it honors the usual `HTTPS_PROXY` /
`NO_PROXY` environment variables.

### Step 1: point `secator` at the platform API

```bash
# Only needed for a self-hosted deployment — Secator Cloud is the default.
secator config set addons.api.url https://<your-secator-api-host>/api

# API token (Workspace or account settings on the platform -> API tokens).
secator config set addons.api.key <API_TOKEN>
```

Both can also be set via environment variables, which is usually more
convenient on a disposable scanning box:

```bash
export SECATOR_ADDONS_API_URL=https://<your-secator-api-host>/api
export SECATOR_ADDONS_API_KEY=<API_TOKEN>
```

{% hint style="info" %}
The token is sent as `Authorization: Bearer <API_TOKEN>` by default
(`addons.api.header_name`, default `Bearer`).
{% endhint %}

### Step 2: pick a workspace

Findings and runners must be attached to a real workspace — the special
`default` workspace cannot be used with the `api` driver. Create/select one
(this calls the platform API and is idempotent, so it's safe to re-run):

```bash
secator ws use my-internal-scans -driver api
```

`ws use` sets this as the **current workspace** (persisted to your config), so
every subsequent run and query uses it automatically — you don't need to pass
`-ws` each time. Pass `-ws <name>` on a single command only to override the
current workspace for that run.

### Step 3: run with `-driver api`

```bash
secator w host_recon 10.10.0.0/24 -driver api
```

Since `my-internal-scans` is already the current workspace from Step 2, no
`-ws` is needed here. If you skipped Step 2 (or want a different workspace for
this run), add it explicitly: `secator w host_recon 10.10.0.0/24 -driver api -ws my-internal-scans`.

`-driver` is comma-separated, so you can combine it with another driver, e.g.
also keep a local MongoDB copy: `-driver api,mongodb`.

As the scan runs, `secator` POSTs the runner (on start, on each progress
update, on completion) and every finding to the platform's API — the run
shows up live on the platform under the workspace you picked, exactly like a
scan dispatched from the platform itself.

***

## Method B — custom queue prefixes (self-hosted only)

Method A gets results from an external scan *into* the platform. Custom queue
prefixes solve a different problem: routing a scan *dispatched from the
platform* to a specific, dedicated pool of workers — for example a worker you
run on an internal network segment, so it can already reach targets the
shared worker fleet can't.

This requires direct connectivity between the platform's Celery broker and
your dedicated worker, which is only possible on a self-hosted deployment.

### Step 1: deploy a worker on a prefixed queue set

```bash
secator worker --queue-prefix fleet1
# short flag: secator worker -qp fleet1
```

A prefix of `fleet1` makes the worker subscribe to `fleet1-small`,
`fleet1-medium`, `fleet1-large`, `fleet1-extra_large`, `fleet1-poll`,
`fleet1-celery`, `fleet1-results` and `fleet1-mongodb` — the classic queue set,
prefixed. You can set the prefix with the flag, or deployment-wide via
`SECATOR_CELERY_QUEUE_PREFIX=fleet1` (equivalently `CONFIG.celery.queue_prefix`).

{% hint style="warning" %}
**mongodb/default-queue caveat**: the mongodb hook and other statically-routed
tasks are always routed using the **deployment-level**
`CONFIG.celery.queue_prefix` — never the per-run prefix below. So a dedicated
worker pool should also set `SECATOR_CELERY_QUEUE_PREFIX=fleet1` on itself,
otherwise its mongodb/default queue won't match what it's actually
subscribed to.
{% endhint %}

### Step 2: allow clients to choose a prefix

Custom queue-prefix routing is off by default — any client-supplied prefix is
silently dropped. On the platform's API, enable it with:

```bash
ALLOW_CUSTOM_QUEUE_PREFIX=1
```

Once set, `GET /capabilities` reports `{"custom_queue_prefix": true}`, and the
platform's UI shows a "Queue prefix" field on the run-creation form.

### Step 3: run a scan on that pool

* **CLI:** `secator w host_recon 10.10.0.0/24 --queue-prefix fleet1` (short:
  `-qp fleet1`)
* **Library:** `run_opts["queue_prefix"] = "fleet1"`
* **Platform UI:** fill in the "Queue prefix" field (only visible once Step 2
  is enabled).

If no prefix is given, `CONFIG.celery.queue_prefix` is used as a deployment
default; if that's also unset, the run goes to the normal, unprefixed queues.
Precedence is: **run option → deployment config → none**.

A prefix must match `^[a-z0-9][a-z0-9_-]{0,31}$` (lowercase alphanumeric,
`-`/`_`, starting with a letter or digit, 32 chars max) — anything else is
rejected.

### End-to-end example

```bash
# 1. On a box with access to your internal network, start a dedicated worker:
SECATOR_CELERY_QUEUE_PREFIX=fleet1 secator worker --queue-prefix fleet1

# 2. On the platform's API, allow clients to pick a prefix:
export ALLOW_CUSTOM_QUEUE_PREFIX=1

# 3. Dispatch a scan onto that pool (from the CLI, the library, or the UI):
secator w host_recon 10.10.0.0/24 --queue-prefix fleet1 -ws my-internal-scans
```

The scan is picked up only by workers listening on `fleet1-*`, and the runner
+ findings land on the platform under `my-internal-scans` like any other run.

***

## Combining both methods

The two methods are independent and can be combined: a self-hosted deployment
can route a scan to a dedicated internal worker pool (Method B) whose
mongodb/findings writes already land in the platform's own database — no
`api` driver needed there, since that worker *is* part of the platform. Method
A is for the case where `secator` runs **entirely outside** the platform's
Celery/Mongo infrastructure (e.g. your own laptop) and needs to phone results
home over HTTP instead.
