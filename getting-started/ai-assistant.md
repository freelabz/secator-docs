---
description: ... or how to use AI-powered penetration testing assistance.
---

# AI assistant

`secator` includes an AI-powered penetration testing assistant that can help automate security assessments, analyze results, and provide intelligent guidance during engagements.

{% hint style="warning" %}
The AI assistant requires the `ai` addon. Install it with:
```bash
secator install addons ai
```
{% endhint %}

***

## Setup

### Installation

```bash
# Install the AI addon
secator install addons ai
```

### Authentication

The recommended way to authenticate is through provider environment variables. This allows you to easily switch between models using the `--model` flag:

```bash
# Set your provider API keys
export ANTHROPIC_API_KEY=<YOUR_KEY>  # For Claude models
export OPENAI_API_KEY=<YOUR_KEY>     # For GPT models
export OPENROUTER_API_KEY=<YOUR_KEY> # For OpenRouter models

# Now you can switch models on the fly
secator x ai example.com -p "Scan this target" --model claude-sonnet-4-6
secator x ai example.com -p "Scan this target" --model gpt-4o
secator x ai example.com -p "Scan this target" --model openrouter/anthropic/claude-haiku-4-5
```

{% hint style="warning" %}
**Cost warning:** The default models (`claude-sonnet-4-6` for main tasks and `claude-haiku-4-5` for intent detection) can get expensive fast, especially Claude Sonnet during long attack sessions. Consider using cheaper models like `gpt-4o-mini` or `claude-haiku-4-5` for cost-sensitive use cases.
{% endhint %}

{% hint style="info" %}
Alternatively, you can set a single API key in the secator config:
```bash
secator config set addons.ai.api_key <YOUR_API_KEY>
```
{% endhint %}

### Supported providers

The AI assistant uses [LiteLLM](https://docs.litellm.ai/) under the hood, which supports many LLM providers. See the [full list of supported models](https://models.litellm.ai/).

Common providers include:

- **OpenAI**: `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`
- **Anthropic**: `claude-sonnet-4-20250514`, `claude-opus-4-20250514`
- **OpenRouter**: `openrouter/anthropic/claude-3.5-sonnet`
- **Local models**: Via Ollama or other local providers

Set `addons.ai.api_base` if using a custom endpoint:

```bash
secator config set addons.ai.api_base http://localhost:11434
```

***

## Usage

### Basic usage

{% tabs %}
{% tab title="CLI" %}
```bash
# Start an AI-assisted attack on a target
secator x ai example.com -p "Find vulnerabilities on this target"

# Chat mode - analyze previous results
secator x ai -p "What are the most critical findings?"

# Specify mode explicitly
secator x ai example.com -p "Enumerate subdomains" --mode attack
secator x ai -p "Summarize the vulnerabilities" --mode chat

# Use a specific model
secator x ai example.com -p "Scan for open ports" --model gpt-4o
```
{% endtab %}

{% tab title="Library" %}
```python
from secator.tasks import ai

# Run AI-assisted attack
results = ai('example.com', prompt='Find vulnerabilities on this target').run()

# Chain with previous results
from secator.tasks import nmap, httpx

ports = nmap('example.com').run()
urls = httpx('example.com').run()
analysis = ai('example.com', prompt='Analyze these results', results=ports + urls).run()
```
{% endtab %}
{% endtabs %}

***

## Modes

The AI assistant has two primary modes:

### Attack mode

In **attack mode**, the AI actively executes security tasks:

- Runs `secator` tasks and workflows
- Executes shell commands for reconnaissance
- Queries previous results
- Makes decisions about next steps

```bash
secator x ai example.com -p "Perform a full reconnaissance" --mode attack
```

### Chat mode

In **chat mode**, the AI analyzes and discusses findings:

- Summarizes vulnerabilities
- Explains technical details
- Provides remediation advice
- Answers security questions

```bash
secator x ai -p "What are the most critical vulnerabilities found?" --mode chat
```

{% hint style="info" %}
If you don't specify a mode, the AI automatically detects intent from your prompt using a fast intent classification model.
{% endhint %}

***

## Options

### AI task options

| Option | CLI | Library | Default | Description |
|--------|-----|---------|---------|-------------|
| Prompt | `-p, --prompt` | `prompt` | `''` | The instruction or question for the AI |
| Mode | `--mode` | `mode` | auto-detect | `attack` or `chat` |
| Model | `--model` | `model` | `claude-sonnet-4-6` | LLM model to use |
| API Key | `--api-key` | `api_key` | config or env var | API key for LLM provider |
| API Base | `--api-base` | `api_base` | `''` | Custom API endpoint |
| Temperature | `--temperature` | `temperature` | `0.7` | LLM temperature (0-1) |
| Max Iterations | `--max-iterations` | `max_iterations` | `10` | Maximum action iterations |
| Sensitive | `--sensitive` | `sensitive` | `True` | Encrypt sensitive data (PII) |
| Dry Run | `--dry-run` | `dry_run` | `False` | Show actions without executing |
| Auto Accept | `-y, --yes` | `yes` | `False` | Auto-accept all actions |
| Interactive | `--interactive` | `interactive` | `True` | Prompt for follow-up actions |
| Intent Model | `--intent-model` | `intent_model` | `claude-haiku-4-5` | Model for intent detection |
| Max Tokens | `--max-tokens-total` | `max_tokens_total` | `100000` | Token budget limit |

***

## AI actions

The AI can perform the following actions:

### Task execution
Run any `secator` task:
```
AI: I'll run an nmap scan to discover open ports.
[Executes: secator x nmap example.com]
```

### Workflow execution
Run predefined workflows:
```
AI: Let me perform a full subdomain reconnaissance.
[Executes: secator w subdomain_recon example.com]
```

### Shell commands
Execute shell commands for additional reconnaissance:
```
AI: I'll check the DNS records.
[Executes: dig example.com ANY]
```

### Query results
Query previous findings:
```
AI: Let me check for critical vulnerabilities.
[Queries: severity == 'critical']
```

### Follow-up
Continue the conversation with new questions or tasks.

### Add finding
Manually add a finding based on analysis.

***

## Configuration

### Configuration options

| Config Key | Default | Description |
|------------|---------|-------------|
| `addons.ai.enabled` | `false` | Enable/disable AI addon |
| `addons.ai.api_key` | `''` | API key for LLM provider |
| `addons.ai.api_base` | `''` | Custom API base URL |
| `addons.ai.default_model` | `claude-sonnet-4-6` | Default LLM model |
| `addons.ai.intent_model` | `claude-haiku-4-5` | Model for intent classification |
| `addons.ai.temperature` | `0.7` | Default temperature |
| `addons.ai.max_tokens` | `30000` | Max tokens per response |
| `addons.ai.max_tokens_total` | `100000` | Total token budget |
| `addons.ai.max_results` | `500` | Max results to send to LLM |
| `addons.ai.encrypt_pii` | `true` | Encrypt sensitive data |

### Setting configuration

```bash
# Adjust temperature (0-1, higher = more creative)
secator config set addons.ai.temperature 0.5

# Limit max tokens per response
secator config set addons.ai.max_tokens 20000

# Limit max results sent to LLM
secator config set addons.ai.max_results 200

# Disable PII encryption (for local models)
secator config set addons.ai.encrypt_pii false
```

***

## Features

### Sensitive data encryption

When `sensitive` mode is enabled (default), the AI assistant automatically encrypts:

- IP addresses
- Domain names
- Email addresses
- API keys and tokens
- Other PII patterns

This prevents sensitive data from being sent to external LLM providers in plain text.

```bash
# Disable encryption (for local models)
secator x ai example.com -p "Scan this target" --no-sensitive
```

### Token management

The AI assistant automatically manages token usage:

- Tracks token consumption per request
- Compacts chat history when approaching limits
- Truncates large results to fit token budget
- Shows token usage in status messages

### Interactive mode

By default, the AI operates in interactive mode:

- Prompts for confirmation before actions
- Allows follow-up questions
- Supports mode switching mid-conversation

Disable for automated pipelines:

```bash
secator x ai example.com -p "Full scan" --no-interactive -y
```

***

## Examples

### Full reconnaissance

```bash
secator x ai example.com -p "Perform comprehensive reconnaissance including subdomain enumeration, port scanning, and web vulnerability scanning"
```

### Analyze existing results

```bash
# First, run some scans
secator w host_recon example.com

# Then analyze with AI
secator x ai -p "Summarize the findings and prioritize remediation"
```

### Automated pipeline

```bash
# Non-interactive mode with auto-accept
secator x ai example.com \
  -p "Find and report all critical vulnerabilities" \
  --no-interactive \
  -y \
  --max-iterations 20 \
  -o json
```

### Using with workflows

```python
from secator.workflows import host_recon
from secator.tasks import ai

# Run reconnaissance
results = host_recon('example.com').run()

# Analyze results with AI
analysis = ai(
    'example.com',
    prompt='What are the security risks?',
    results=results,
    mode='chat'
).run()
```

***

## Troubleshooting

### Authentication errors

```
Error: AuthenticationError
```

Solution: Verify your API key is correctly set:
```bash
secator config get addons.ai.api_key
secator config set addons.ai.api_key <VALID_KEY>
```

Or ensure the appropriate environment variable is set:
```bash
export ANTHROPIC_API_KEY=<YOUR_KEY>  # For Claude models
export OPENAI_API_KEY=<YOUR_KEY>     # For GPT models
```

### Rate limiting

The AI assistant automatically handles rate limits by waiting and retrying. If you encounter persistent rate limiting, consider:

- Using a model with higher rate limits
- Reducing `max_iterations`
- Adding delays between requests

### Empty responses

If the LLM returns empty responses:

- Check your API key permissions
- Try a different model
- Verify the API endpoint is accessible

***
