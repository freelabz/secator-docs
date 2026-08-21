---
description: The `ai` task — running the AI assistant as a first-class secator task.
---

# AI task

`ai` is a first-class `secator` task (like `nmap`, `httpx` or `nuclei`) that runs the
AI-powered penetration testing assistant. Because it's a task, it can be launched from
the CLI (`secator x ai`), called from the library, chained with other tasks' results,
dispatched to a Celery worker, and even spawned by itself as an autonomous subagent.

{% hint style="info" %}
**Task vs. assistant.** The [AI assistant](ai-assistant.md) page is the getting-started
guide: installation, providers, authentication, modes and cost. **This page is the task
reference**: how to run the `ai` task, its full option set, output types, library/compose
usage, sessions and subagents. They are the same engine — start with the assistant page
to get set up, come here for the task mechanics.
{% endhint %}

{% hint style="warning" %}
The `ai` task requires the `ai` addon:
```bash
secator install addons ai
```
Run `secator x ai setup` once to configure a model and API key interactively.
{% endhint %}

***

## What it does

Unlike other tasks, `ai` is not a wrapper around an external CLI — it's a
`PythonRunner` that drives an LLM in a loop. On each iteration it:

1. Sends the conversation (system prompt + history) to the model via
   [LiteLLM](https://docs.litellm.ai/), exposing a small set of generic **tools**.
2. Receives the model's response and any **tool calls** (run a task, run a workflow,
   run a shell command, query the workspace, add a finding, ask a follow-up).
3. Validates each tool call against the **permission engine** (guardrails), dispatches
   the allowed ones, and feeds the results back into the conversation.
4. Repeats until the model stops, the user ends the session, or `max_iterations` is hit.

Everything the assistant discovers (ports, URLs, vulnerabilities, …) is reported into
the workspace as normal `secator` findings, so `ai` composes with the rest of the
framework exactly like any other task.

***

## Modes

The task runs in one of three modes. If you don't pass `--mode`, a fast
`intent_model` classifies your prompt and picks one automatically.

| Mode | Purpose |
|------|---------|
| `chat` | Analyse and discuss existing findings — summaries, explanations, remediation advice. No tasks are executed. |
| `attack` | Actively run tasks, workflows and shell commands to discover and enumerate. |
| `exploit` | Focused exploitation-verification of a specific vulnerability (builds a PoC). Primarily used by subagents. |

```bash
secator x ai example.com -p "Enumerate subdomains" --mode attack
secator x ai -p "Summarize the vulnerabilities" --mode chat
```

***

## CLI usage

{% tabs %}
{% tab title="Basic" %}
```bash
# Attack a target (mode auto-detected from the prompt)
secator x ai example.com -p "Find vulnerabilities on this target"

# Chat about findings already in the workspace (no target needed)
secator x ai -p "What are the most critical findings?"

# Pick a model
secator x ai example.com -p "Scan for open ports" --model gpt-4o

# Read the prompt from a file (pass a path to -p)
secator x ai example.com -p ./prompts/recon.txt
```
{% endtab %}

{% tab title="Non-interactive" %}
```bash
# Automated pipeline: no follow-up prompts, auto-accept actions, JSON output
secator x ai example.com \
  -p "Find and report all critical vulnerabilities" \
  --interactive auto \
  -y \
  --max-iterations 20 \
  -o json
```
{% endtab %}

{% tab title="Sessions" %}
```bash
# Name a session so you can resume it later
secator x ai example.com -n recon-run -p "Recon this host"

# Resume a previous session (interactive picker)
secator x ai --resume
```
{% endtab %}

{% tab title="Diagnostics" %}
```bash
# Interactive setup wizard (model + API key). Always runs locally.
secator x ai setup

# Preview actions without executing them
secator x ai example.com -p "Full scan" --dry-run

# Render the system prompt for a mode and exit (no LLM call)
secator x ai --mode attack --show-prompt
```
{% endtab %}
{% endtabs %}

***

## Library usage

```python
from secator.tasks import ai

# Run an AI-assisted attack
results = ai('example.com', prompt='Find vulnerabilities on this target').run()

# Chain with other tasks' results — the AI can query and reason over them
from secator.tasks import nmap, httpx

ports = nmap('example.com').run()
urls = httpx('example.com').run()
analysis = ai(
    'example.com',
    prompt='Analyze these results and prioritize remediation',
    results=ports + urls,
    mode='chat',
).run()
```

When you pass `results`, the task scope becomes `current` (it reasons over the results
you handed it); otherwise it operates over the whole `workspace` and queries findings on
demand.

{% hint style="info" %}
Run it on a Celery worker like any task by adding `async_tasks=True` (or the
`--async-tasks` flag) so the tasks/workflows it launches are dispatched to workers
instead of running inline.
{% endhint %}

***

## Options

| Option | CLI | Library | Default | Description |
|--------|-----|---------|---------|-------------|
| Prompt | `-p, --prompt` | `prompt` | `''` | Instruction/question. A path is read as a file. |
| Session name | `-n, --name` | `name` | `''` | Name the session (for resume) or a subagent. |
| Mode | `--mode` | `mode` | auto-detect | `chat`, `attack` or `exploit`. |
| Model | `--model` | `model` | `addons.ai.default_model` (`claude-sonnet-4-6`) | LLM model. |
| Intent model | `--intent-model` | `intent_model` | `addons.ai.intent_model` (`claude-haiku-4-5`) | Fast model for mode detection. |
| API key | `--api-key` | `api_key` | config / env var | Provider key (redacted from serialized state). |
| API base | `--api-base` | `api_base` | config | Custom endpoint (e.g. Ollama). |
| Temperature | `--temperature` | `temperature` | `0.7` | Sampling temperature. |
| Max iterations | `--max-iterations` | `max_iterations` | `10` | Max LLM/action loops. |
| Max tokens total | `--max-tokens-total` | `max_tokens_total` | `100000` | Hard token budget; oldest messages truncated beyond it. |
| Sensitive | `--sensitive` / `--no-sensitive` | `sensitive` | `True` | Encrypt PII before sending to the provider. |
| Dry run | `--dry-run` | `dry_run` | `False` | Show actions without executing them. |
| Auto-accept | `-y, --yes` | `yes` | `False` | Skip confirmation of actions. |
| Interactive | `--interactive` | `interactive` | `local` | `local` (rich prompts), `remote` (UI/DB), or `auto` (no prompts). |
| Resume | `--resume` | `resume` | `False` | Resume a saved session via a picker. |
| Context warnings | `--context-warnings` / `--no-context-warnings` | `context_warnings` | `True` | Prompt at 50%/75% context-window usage (local only). |
| Async tasks | `--async-tasks` | `async_tasks` | `False` | Dispatch launched tasks/workflows to Celery workers. |
| Show prompt | `--show-prompt` | `show_prompt` | `False` | Render the system prompt and exit. |
| Dangerous | `--dangerous` | `dangerous` | `False` | **Skip all guardrail checks.** Use with extreme care. |

A few options are internal (set programmatically, not meant for direct CLI use):
`context` (findings/scope/objective passed in), `subagent` (marks a spawned subagent and
suppresses its interactive prompts/progress), and `max_workers` (concurrency for batch
action execution, default `3`).

{% hint style="info" %}
Provider defaults, token budgets, PII encryption and the permission engine all live under
`addons.ai.*` in the config — see the [AI assistant](ai-assistant.md#configuration) page.
{% endhint %}

***

## AI actions (tool calling)

The task exposes six generic tools to the model. Each call is validated by the permission
engine before it runs:

| Tool | What it does |
|------|--------------|
| `run_task` | Run any `secator` task (including `ai` itself, as a subagent). |
| `run_workflow` | Run a composed workflow (e.g. `host_recon`). |
| `run_shell` | Run a shell command for extra reconnaissance. |
| `query_workspace` | MongoDB-style query over stored findings. |
| `add_finding` | Record a finding derived from analysis. |
| `follow_up` | Ask you a follow-up question / offer choices. |

The **calling convention** lives in these tool schemas; the **catalog** of task names,
options, profiles and wordlists lives in the system prompt as a library reference. For the
full design — token budget, subagent spawning, and the tradeoffs — see
[`secator_ai_tool_calling.md`](../secator_ai_tool_calling.md).

### Guardrails

Every task/workflow/shell/read/write/target is checked against the `addons.ai.permissions`
policy (`allow` / `deny` / `ask` rules). Targets found in the current workspace are
auto-approved; loopback and cloud-metadata addresses (`127.0.0.1`, `localhost`,
`169.254.169.254`) are denied by default; destructive shell commands are blocked. Passing
`--dangerous` bypasses all of it.

***

## Sessions & subagents

- **Sessions.** Every run is saved (history + workspace folder). Name one with `-n` and
  resume it later with `--resume`; the picker restores the conversation and model so you
  can keep going.
- **Subagents.** In `attack`/`exploit` mode the AI can call `run_task` with `name: "ai"`
  to spawn a focused, non-interactive child with a fresh context window (e.g. "verify
  CVE-XXXX on this host"). Subagents report back into the same workspace. Concurrency is
  capped by `max_workers`.

***

## Output types

The task produces the standard `secator` [output types](../in-depth/concepts/output-types.md)
plus an AI-specific one:

- **`Ai`** — the AI's own messages and actions. Its `ai_type` field distinguishes
  `prompt` (your input), `response` (model output), `task` / `workflow` / `shell` /
  `query` / `add_finding` (action taken), `shell_output`, `follow_up`, `stopped`
  (session ended) and `chat_compacted` (history was summarized). In the terminal these
  render as panels; in JSON they carry `content`, `ai_type`, `mode`, `model` and token/cost
  metadata in `extra_data`.
- **All finding types + `Target`** — anything the tasks and workflows it launches
  discover (ports, URLs, vulnerabilities, subdomains, …), reported into the workspace like
  any other run.

Combine with `-o json`, `-o table`, or any [exporter](../in-depth/concepts/exporters.md)
just as you would for other tasks.

***

## See also

- [AI assistant](ai-assistant.md) — setup, providers, modes and cost.
- [`secator_ai_tool_calling.md`](../secator_ai_tool_calling.md) — tool-calling architecture and subagents.
- [Output types](../in-depth/concepts/output-types.md) · [Exporters](../in-depth/concepts/exporters.md)
