# Secator AI: Tool Calling Architecture

## Overview

Secator's AI task uses native LLM tool calling (OpenAI function calling format via litellm) to dispatch security tasks, workflows, shell commands, queries, and other actions. This document covers the current implementation, the token management strategy, and the tradeoffs between different approaches for exposing secator's task catalog to the LLM.

---

## Current Architecture

### How It Works

The AI loop sends **6 generic tool schemas** to the LLM via litellm's `tools` parameter:

| Tool | Action | Purpose |
|------|--------|---------|
| `run_task` | task | Run any secator task (nmap, httpx, nuclei, ai...) |
| `run_workflow` | workflow | Run a composed workflow |
| `run_shell` | shell | Execute arbitrary shell commands |
| `query_workspace` | query | MongoDB-style query on stored findings |
| `follow_up` | follow_up | Ask the user a follow-up question |
| `add_finding` | add_finding | Add a finding to the workspace |

The tool schemas define the **calling convention** (API shape). The **task catalog** (what task names exist, what options each accepts) lives in the system prompt as a "library reference".

### Two Separate Channels

```
┌─────────────────────────────────────────────┐
│ System Prompt                               │
│  - Persona, constraints, rules              │
│  - Library reference:                       │
│    TASKS: nmap|desc|ports,rate_limit,...     │
│    WORKFLOWS: host_recon|desc               │
│    PROFILES: aggressive|desc                │
│    WORDLISTS: common, big, ...              │
│    OUTPUT_TYPES: vulnerability|fields,...    │
│    OPTION_FORMATS: header, cookie, proxy    │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ tools= parameter (separate from messages)   │
│  - run_task(name, targets, opts)            │
│  - run_workflow(name, targets, opts)        │
│  - run_shell(command)                       │
│  - query_workspace(query, limit)            │
│  - follow_up(reason, choices)               │
│  - add_finding(_type, ...)                  │
└─────────────────────────────────────────────┘
```

The tool schemas tell the LLM **how** to call. The library reference tells it **what** to call with.

### Token Budget

| Component | Approximate size |
|-----------|-----------------|
| System prompt (persona + constraints) | ~650 words |
| Library reference (tasks + workflows + profiles + wordlists + output types) | ~450 words |
| Tool schemas (6 tools) | ~400 tokens |
| **Total fixed cost per LLM call** | **~1,500 tokens** |

The library reference is paid on **every LLM call** since it's in the system prompt.

---

## AI Subagents

The AI task can spawn autonomous subagents by calling `run_task` with `name: "ai"`. The subagent gets a fresh context window and runs non-interactively.

```
Parent AI ──run_task(name="ai", targets=[...], opts={
    "prompt": "Exploit CVE-2024-XXXX on target",
    "mode": "exploiter",
    "internal": true,
    "max_iterations": 5
})──> Child AI (fresh context, focused objective)
```

### When to Spawn Subagents

- Vulnerability needs focused exploitation/verification (mode: `exploiter`)
- Complex sub-task benefits from dedicated context
- User explicitly requests it
- Current context has grown large; fresh agent is more efficient

### Subagent Modes

| Mode | Purpose | Max iterations |
|------|---------|---------------|
| `attack` | Full recon/pentest | 10 (default) |
| `chat` | Analysis/queries only | 10 (default) |
| `exploiter` | Focused exploitation/verification | 5 |

---

## Token Display

Token usage is displayed in three places:

### 1. LLM Spinner (while thinking)

```
⠋ Analyzing attack surface...  • ⬆ 8.2k/200.0k (system:3.2k | user:1.5k | assistant:2.1k | tool:1.4k)
```

- Current total / max context window (max in dim red)
- Per-role breakdown in orange

### 2. Prompt / Response Output

```
❯ Scan for vulnerabilities  • ⬆ 3.3k/200.0k (system:3.2k | user:63)
🧠 (1/10) I'll start with...  • ⬇ 5.1k/200.0k (system:3.2k | user:63 | assistant:1.8k)
```

- Compact format: `Xk/Yk` (no "tokens" suffix)
- Per-role breakdown shows where tokens are spent

### 3. Batch Execution Panel

```
┌─ Batch execution ──────────────────────────────────────┐
│ ⠋ httpx on target.com    RUNNING   0:05  3 results  2.1k/10.0k │
│ ⠋ nmap on target.com     RUNNING   0:12              │
│ ✓ nuclei on target.com   SUCCESS   0:08  12 results 8.4k/10.0k │
└────────────────────────────────────────────────────────┘
```

- Per-task output token count vs action budget
- Helps visualize context window pressure from each task

---

## Alternative Approaches: Catalog Exposure

The core question: **how should the LLM know what tasks/options are available?**

### Approach 1: Library Reference in System Prompt (Current)

The full catalog (task names, descriptions, options) is embedded in the system prompt.

```
System prompt contains:
  TASKS:
  nmap|Port scanner|ports,rate_limit,timeout,...
  httpx|HTTP probe|follow_redirects,threads,...
  nuclei|Vulnerability scanner|templates,...
  ... (45+ tasks)
```

| Pros | Cons |
|------|------|
| Zero extra tool calls | ~450 words paid every LLM call |
| LLM always knows the full catalog | Options for unused tasks waste tokens |
| Simplest implementation | Doesn't scale well with more tasks |

### Approach 2: Internal Discovery Tools

Add `list_tasks` and `get_task_options` as LLM-callable tools. Remove the library reference from the system prompt.

```
LLM calls list_tasks() → gets task names in tool result message
LLM calls get_task_options("nmap") → gets nmap options in tool result message
LLM calls run_task("nmap", targets, opts)
```

| Pros | Cons |
|------|------|
| On-demand loading (pay only for what you use) | +1-2 tool calls on first iteration |
| Options loaded per-task, not in bulk | Discovery results persist in conversation history |
| System prompt stays lean | **Token cost accumulates**: results stay in messages |
| No transport overhead (in-process) | After discovery, same cost as approach 1 |

**Key issue**: Tool results become part of the message history. Once the LLM calls `list_tasks()`, that response is in every subsequent LLM call — effectively the same as having it in the system prompt, just deferred.

### Approach 3: MCP Server (secator-mcp)

Use the existing secator-mcp server. The MCP layer handles discovery and routing outside the LLM context.

```
LLM sees: run_task(name, targets, opts)  ← simple schema
MCP server handles: validation, option lookup, execution
Discovery: happens outside LLM context via MCP protocol
```

| Pros | Cons |
|------|------|
| Discovery outside LLM context | Higher latency (stdio transport per call) |
| **Token cost stays low across iterations** | Two codebases to maintain |
| Formal, reusable interface | More moving parts |
| Any MCP client can use it | Model compatibility with many tools |
| Validation at MCP layer | |

**Key advantage over approach 2**: MCP discovery is a side-channel. The LLM context stays clean — `list_tasks()` results don't pollute the conversation history. Token cost for the catalog is paid once by the MCP client, not carried in every LLM call.

### Approach 4: Hybrid (Recommended)

Combine the best of each approach:

- **Enum for task/workflow names** in `run_task`/`run_workflow` tool schemas — always visible, near-zero token cost
- **Compact one-liner per task** in system prompt (just `name|description`, drop options)
- **`get_task_options(name)` tool** for detailed options on-demand

```
Tool schema:  run_task(name: enum["nmap","httpx",...], targets, opts)
System prompt: nmap|Port scanner
               httpx|HTTP probe
               ...
On-demand:    get_task_options("nmap") → ports, rate_limit, timeout, ...
```

| Pros | Cons |
|------|------|
| LLM always knows task names (enum) | Options results persist in history |
| Descriptions guide task selection (cheap) | Slightly more complex than current |
| Options loaded only when needed | |
| No external dependencies | |

### Comparison Matrix

| | System prompt (current) | Internal discovery | MCP | Hybrid |
|---|---|---|---|---|
| **Tool calls per task** | 0 extra | +1-2 first time | +1-2 first time | +1 first time |
| **Token cost (iteration 1)** | High | Low | Low | Medium |
| **Token cost (iteration N)** | High | High (results in history) | **Low** (outside context) | Medium-High |
| **Latency** | Lowest | Low | Higher (transport) | Low |
| **Maintenance** | Single codebase | Single codebase | Two codebases | Single codebase |
| **External reuse** | No | No | Yes (any MCP client) | No |
| **Scales with tasks** | Poorly | Moderately | Well | Well |

---

## Key Files

| File | Purpose |
|------|---------|
| `secator/ai/tools.py` | Tool schemas (OpenAI format), `build_tool_schemas(mode)`, `tool_call_to_action()` |
| `secator/ai/prompts.py` | System prompts, library reference builders, mode configs |
| `secator/ai/actions.py` | Action handlers: `dispatch_action()`, `_run_batch()`, `_run_runner()` |
| `secator/ai/history.py` | Chat history, token counting, compaction, truncation |
| `secator/ai/utils.py` | `call_llm()` wrapper around litellm |
| `secator/tasks/ai.py` | Main AI task: `_run_loop()`, spinner, prompt display |
| `secator/output_types/ai.py` | AI output type rendering (token display, markdown) |
| `secator-mcp/` | External MCP server (15 tools, same parametric model) |
