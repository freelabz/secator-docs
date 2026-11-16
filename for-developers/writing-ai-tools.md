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
results. Anything that touches a target belongs in a `secator` task or workflow,
which the agent runs through `run_task` / `run_workflow` under the
[permission engine](../in-depth/ai-task.md#permission-engine) and the run's
scope.
