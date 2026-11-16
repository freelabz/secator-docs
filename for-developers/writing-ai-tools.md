---
description: ... or how to give the AI task your own tools.
---

# Writing AI tools

The [`ai` task](../in-depth/ai-task.md) calls **tools** (`run_task`,
`query_workspace`, `add_finding`, ...). You can add your own without changing
`secator`: drop a Python file defining one `BaseTool` subclass in your templates
directory, and enable it with `--extra-tools`. It is the same drop-in model as a
[custom task](writing-tasks/README.md).

***

## A minimal tool

```python
# ~/.secator/templates/tools/word_count.py
from secator.ai.actions import _get_result_context
from secator.ai.tools.base import BaseTool
from secator.output_types import Ai, Error


class WordCount(BaseTool):
	name = "word_count"
	schema = {
		"type": "function",
		"function": {
			"name": "word_count",
			"description": "Count the words in a piece of text.",
			"parameters": {
				"type": "object",
				"properties": {
					"text": {"type": "string", "description": "The text to count words in."},
				},
				"required": ["text"],
			},
		},
	}

	def run(self, action, ctx):
		context = _get_result_context(action, ctx)
		text = action.get("text")
		if not isinstance(text, str):
			yield Error(message="word_count requires a `text` string.", _context=context)
			return
		count = len(text.split())
		# Shown in the transcript.
		yield Ai(content=f"{count} words", ai_type="word_count", _context=context)
		# Sent back to the model as the tool result.
		yield {"_type": "word_count", "count": count, "_context": {**context, "ai_query_result": True}}
```

```bash
secator x ai example.com -p "How many words are in 'scan example.com now'?" --extra-tools word_count
```

***

## The tool class

| Attribute | Required | What it is |
| --- | --- | --- |
| `name` | yes | The tool name the model calls. Must not clash with another tool. |
| `schema` | yes | The tool definition sent to the model, in the OpenAI function-calling format (`{"type": "function", "function": {"name", "description", "parameters"}}`). Keep `function.name` equal to `name`. |
| `action` | no | The action type the tool dispatches on. Defaults to `name`. |
| `run(self, action, ctx)` | yes | The handler: a generator of results (see below). |

`run()` receives:

- `action` - a dict of the arguments the model passed (as described by your
  `parameters`), plus an `action` key and the id of the tool call.
- `ctx` - the run's context: its targets, workspace and driver context, and the
  permission engine.

Built-in tools follow the same contract: each one lives in its own file under
`secator/ai/tools/`.

### What `run()` yields

Stamp **every** item you yield with the tool-call context,
`_context=_get_result_context(action, ctx)`, as in the example above. That is
how the result is matched to the model's tool call; an item without it breaks
the turn. Then:

| You yield | Shown in the transcript | Sent to the model |
| --- | :---: | :---: |
| `Ai(content=..., ai_type="<your tool>")` | yes | no |
| a plain `dict` with `"_context": {**context, "ai_query_result": True}` | no | yes |
| `Error` / `Warning` | yes | yes |
| a finding (`Vulnerability`, `Url`, ...) | yes, and recorded in the workspace | yes |
| `Info` | no | no |

The usual pattern is the one above: an `Ai` item for the person watching, and a
`dict` with the data the model should reason about. Yield an `Error` for bad
input instead of raising, so the model can correct itself.

***

## Where tools are loaded from

At startup, `secator` scans these directories (recursively) for Python files
that define a `BaseTool` subclass:

- your templates directory (`~/.secator/templates` by default; set with
  `dirs.templates` / `SECATOR_DIRS_TEMPLATES`). Any sub-folder works - e.g.
  `~/.secator/templates/tools/`.
- each directory listed in the `SECATOR_AI_TOOLS_DIRS` environment variable
  (`:`-separated), e.g. a shared directory of tools mounted on a worker.

```bash
export SECATOR_AI_TOOLS_DIRS=/opt/secator-tools:/srv/team-tools
```

{% hint style="info" %}
`SECATOR_AI_TOOLS_DIRS` is read directly by the tool loader, not by the config
system, so `secator` may print an "unknown config key, ignored" notice for it.
The directories are still loaded.
{% endhint %}

A tool file is not mistaken for a custom task: task discovery skips files that
define a `BaseTool` subclass.

***

## Enabling a tool

A loaded tool is **inactive** until you name it. The built-in modes choose their
tools with globs over the **built-in** tool names (see
[Tools per mode](../in-depth/ai-task.md#tools-per-mode)); those globs never match
a custom tool, not even `*`. Add it explicitly:

- for one run: `--extra-tools word_count` (comma-separated for several);
- for every run: `secator config set addons.ai.extra_tools word_count`
  (or `SECATOR_ADDONS_AI_EXTRA_TOOLS=word_count`).

Both lists are merged and deduplicated. A mode can still exclude a tool with a
`!name` entry in its `tools:` list.

***

## Validation and errors

A bad tool never breaks the AI task or the other tools:

- a file that fails to import (syntax error, missing dependency) is skipped with
  an error message naming the file;
- a tool whose `name` is missing, or clashes with an existing tool name or
  action, is skipped;
- a tool with an empty `schema`, or that does not override `run()`, is skipped.

Each skip prints a message saying why. If a name you pass in `--extra-tools` /
`addons.ai.extra_tools` does not match a loaded tool, the run fails with an error
listing the known tools.

***

## Permissions and safety

The permission engine **auto-allows** custom tools: calling one never prompts.
So a tool must not reach your targets or touch the filesystem on its own - keep
it to work like formatting, lookups in data you already have, or recording
results. Anything that touches a target belongs in a `secator` task or workflow:
either the agent runs it through `run_task` / `run_workflow`, or your tool runs
it with `run_task_from_tool` (below). Both go through the
[permission engine](../in-depth/ai-task.md#permission-engine) and the run's
scope.

***

## Running a task from a tool

`run_task_from_tool` runs a `secator` task or workflow from inside your tool,
through the **same** path as a `run_task` call from the model:

- the same permission check: the same deny rules, the same target approval and
  the same prompt (skipped only when the run uses `--dangerous`);
- the run's `--in-scope` / `--out-of-scope` boundary.

If the check denies the task, `run_task_from_tool` yields a `Warning` and nothing
runs. Calling it from an auto-allowed tool grants nothing: the task is checked
on its own.

```python
from secator.ai.actions import run_task_from_tool

# inside run(self, action, ctx):
yield from run_task_from_tool(ctx, "httpx", targets=["example.com"], description="Probe the web server")
```

Pass `runner_type="workflow"` to run a workflow instead.

{% hint style="warning" %}
Requires a `secator` version that includes
[secator#1662](https://github.com/freelabz/secator/pull/1662). In earlier
versions, the results of a task started this way are not matched to the model's
tool call and the agent's turn fails.
{% endhint %}

***

## Reusing your custom tasks and drivers

Custom tasks and drivers are loaded **before** custom tools, so a tool can use
them through two lookups in `secator.loader`:

- `get_task_class(name)` - the task class for a built-in or custom task, or
  `None`;
- `get_driver_hooks(name)` - the `HOOKS` mapping of a custom
  [driver](../in-depth/concepts/drivers.md) loaded from your templates
  directory (`{runner class: {hook name: [functions]}}`), or `None`.

For example, with a custom task `mytask` and a custom reporting driver
`reporting` in your templates directory:

```python
# ~/.secator/templates/tools/run_and_report.py
from secator.ai.actions import _get_result_context, run_task_from_tool
from secator.ai.tools.base import BaseTool
from secator.loader import get_driver_hooks, get_task_class
from secator.output_types import Ai, Error
from secator.runners import Task


class RunAndReport(BaseTool):
	name = "run_and_report"
	schema = {
		"type": "function",
		"function": {
			"name": "run_and_report",
			"description": "Run mytask against targets, then call the reporting driver's on_end hook.",
			"parameters": {
				"type": "object",
				"properties": {"targets": {"type": "array", "items": {"type": "string"}}},
				"required": ["targets"],
			},
		},
	}

	def run(self, action, ctx):
		context = _get_result_context(action, ctx)
		if get_task_class("mytask") is None:
			yield Error(message="run_and_report needs the custom task `mytask`.", _context=context)
			return
		# Same permission check and scope as a model-issued run_task.
		yield from run_task_from_tool(ctx, "mytask", targets=action.get("targets"),
		                              description="Collect data with mytask")
		# Reuse a hook of the custom `reporting` driver.
		hooks = (get_driver_hooks("reporting") or {}).get(Task, {})
		for fn in hooks.get("on_end", []):
			fn(None, None)  # this hook takes (runner, item) but uses neither
		yield Ai(content="run_and_report: done", ai_type="run_and_report", _context=context)
```

The task's own results (findings, errors) reach the model as the tool result,
like a `run_task` call. This example also needs
[secator#1662](https://github.com/freelabz/secator/pull/1662).

{% hint style="warning" %}
Driver hook functions are written for a runner: they receive `(runner, item)`
and often read the runner's context. Only call a hook from a tool when you know
what it uses; otherwise put the shared logic in a plain function the hook and
the tool both call.
{% endhint %}
