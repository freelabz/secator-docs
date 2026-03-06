---
description: ... or how to use AI-powered penetration testing assistance.
---

# AI Assistant

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

# Configure your API key
secator config set addons.ai.api_key <YOUR_API_KEY>

# Optionally set a custom model
secator config set addons.ai.default_model gpt-4o
```

### Supported Providers

The AI assistant uses [LiteLLM](https://docs.litellm.ai/) under the hood, which supports many LLM providers:

- **OpenAI**: `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`
- **Anthropic**: `claude-sonnet-4-20250514`, `claude-opus-4-20250514`
- **OpenRouter**: `openrouter/anthropic/claude-3.5-sonnet`
- **Local models**: Via Ollama or other local providers

Set `addons.ai.api_base` if using a custom endpoint:

```bash
secator config set addons.ai.api_base http://localhost:11434/v1
```

***

## Usage

### Basic Usage

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

### Attack Mode

In **attack mode**, the AI actively executes security tasks:

- Runs `secator` tasks and workflows
- Executes shell commands for reconnaissance
- Queries previous results
- Makes decisions about next steps

```bash
secator x ai example.com -p "Perform a full reconnaissance" --mode attack
```

### Chat Mode

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

### AI Task Options

| Option | CLI | Library | Default | Description |
|--------|-----|---------|---------|-------------|
| Prompt | `-p, --prompt` | `prompt` | `''` | The instruction or question for the AI |
| Mode | `--mode` | `mode` | auto-detect | `attack` or `chat` |
| Model | `--model` | `model` | config default | LLM model to use |
| API Key | `--api-key` | `api_key` | config default | API key for LLM provider |
| API Base | `--api-base` | `api_base` | `''` | Custom API endpoint |
| Temperature | `--temperature` | `temperature` | `0.7` | LLM temperature (0-1) |
| Max Iterations | `--max-iterations` | `max_iterations` | `10` | Maximum action iterations |
| Sensitive | `--sensitive` | `sensitive` | `True` | Encrypt sensitive data (PII) |
| Dry Run | `--dry-run` | `dry_run` | `False` | Show actions without executing |
| Auto Accept | `-y, --yes` | `yes` | `False` | Auto-accept all actions |
| Interactive | `--interactive` | `interactive` | `True` | Prompt for follow-up actions |
| Intent Model | `--intent-model` | `intent_model` | config default | Model for intent detection |
| Max Tokens | `--max-tokens-total` | `max_tokens_total` | `100000` | Token budget limit |

***

## AI Actions

The AI can perform the following actions:

### Task Execution
Run any `secator` task:
```
AI: I'll run an nmap scan to discover open ports.
[Executes: secator x nmap example.com]
```

### Workflow Execution
Run predefined workflows:
```
AI: Let me perform a full subdomain reconnaissance.
[Executes: secator w subdomain_recon example.com]
```

### Shell Commands
Execute shell commands for additional reconnaissance:
```
AI: I'll check the DNS records.
[Executes: dig example.com ANY]
```

### Query Results
Query previous findings:
```
AI: Let me check for critical vulnerabilities.
[Queries: severity == 'critical']
```

### Follow-up
Continue the conversation with new questions or tasks.

### Add Finding
Manually add a finding based on analysis.

***

## Configuration

### Configuration Options

| Config Key | Default | Description |
|------------|---------|-------------|
| `addons.ai.enabled` | `false` | Enable/disable AI addon |
| `addons.ai.api_key` | `''` | API key for LLM provider |
| `addons.ai.api_base` | `''` | Custom API base URL |
| `addons.ai.default_model` | `gpt-4o` | Default LLM model |
| `addons.ai.intent_model` | `gpt-4o-mini` | Model for intent classification |
| `addons.ai.temperature` | `0.7` | Default temperature |
| `addons.ai.max_tokens` | `30000` | Max tokens per response |
| `addons.ai.max_tokens_total` | `100000` | Total token budget |
| `addons.ai.max_results` | `500` | Max results to send to LLM |
| `addons.ai.encrypt_pii` | `true` | Encrypt sensitive data |

### Setting Configuration

```bash
# Set API key
secator config set addons.ai.api_key sk-...

# Set default model
secator config set addons.ai.default_model claude-sonnet-4-20250514

# Set custom API endpoint (e.g., for local models)
secator config set addons.ai.api_base http://localhost:11434/v1

# Adjust temperature
secator config set addons.ai.temperature 0.5
```

***

## Features

### Sensitive Data Encryption

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

### Token Management

The AI assistant automatically manages token usage:

- Tracks token consumption per request
- Compacts chat history when approaching limits
- Truncates large results to fit token budget
- Shows token usage in status messages

### Interactive Mode

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

### Full Reconnaissance

```bash
secator x ai example.com -p "Perform comprehensive reconnaissance including subdomain enumeration, port scanning, and web vulnerability scanning"
```

### Analyze Existing Results

```bash
# First, run some scans
secator w host_recon example.com

# Then analyze with AI
secator x ai -p "Summarize the findings and prioritize remediation"
```

### Automated Pipeline

```bash
# Non-interactive mode with auto-accept
secator x ai example.com \
  -p "Find and report all critical vulnerabilities" \
  --no-interactive \
  -y \
  --max-iterations 20 \
  -o json
```

### Using with Workflows

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

### Authentication Errors

```
Error: AuthenticationError
```

Solution: Verify your API key is correctly set:
```bash
secator config get addons.ai.api_key
secator config set addons.ai.api_key <VALID_KEY>
```

### Rate Limiting

The AI assistant automatically handles rate limits by waiting and retrying. If you encounter persistent rate limiting, consider:

- Using a model with higher rate limits
- Reducing `max_iterations`
- Adding delays between requests

### Empty Responses

If the LLM returns empty responses:

- Check your API key permissions
- Try a different model
- Verify the API endpoint is accessible

***
