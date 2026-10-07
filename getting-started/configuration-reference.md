---
description: ... or every configuration option, its default and its env var.
---

# Configuration reference

{% hint style="info" %}
This page is generated from secator's configuration models by `scripts/generate_config_reference.py` in the docs repository. To see the defaults of your installed version, run `secator config default`.
{% endhint %}

Set any key in `~/.secator/config.yml` (or with `secator config set <key> <value>`), or override it with its environment variable. See [Configuration](configuration.md) for how config files and overrides work.

***

## debug

Debug output filtering.

| Key | Type | Default | Env var | Description |
| --- | --- | --- | --- | --- |
| `debug` | `str` | `""` | `SECATOR_DEBUG` | Comma-separated debug components to print (`all` for everything, prefix match, or a regex such as `cve.*`). |

***

## dirs

Directories used by secator. Unset directories are created under `dirs.data`.

| Key | Type | Default | Env var | Description |
| --- | --- | --- | --- | --- |
| `dirs.bin` | `path` | `~/.local/bin` | `SECATOR_DIRS_BIN` | Where tool binaries are installed. |
| `dirs.share` | `path` | `~/.local/share` | `SECATOR_DIRS_SHARE` | Where shared tool data is installed. |
| `dirs.data` | `path` | `~/.secator` | `SECATOR_DIRS_DATA` | Root data folder. `config.yml` is read from this folder, so change it with the `SECATOR_DIRS_DATA` env var. |
| `dirs.templates` | `path` | `<dirs.data>/templates` | `SECATOR_DIRS_TEMPLATES` | Custom task, workflow, scan and profile templates. |
| `dirs.reports` | `path` | `<dirs.data>/reports` | `SECATOR_DIRS_REPORTS` | Reports, one subfolder per workspace. |
| `dirs.wordlists` | `path` | `<dirs.data>/wordlists` | `SECATOR_DIRS_WORDLISTS` | Downloaded wordlists. |
| `dirs.cves` | `path` | `<dirs.data>/cves` | `SECATOR_DIRS_CVES` | Cached CVE data. |
| `dirs.payloads` | `path` | `<dirs.data>/payloads` | `SECATOR_DIRS_PAYLOADS` | Downloaded payloads. |
| `dirs.performance` | `path` | `<dirs.data>/performance` | `SECATOR_DIRS_PERFORMANCE` | Profiling output (`-pyinstrument`, `-memray`). |
| `dirs.revshells` | `path` | `<dirs.data>/revshells` | `SECATOR_DIRS_REVSHELLS` | Reverse shells data. |
| `dirs.queries` | `path` | `<dirs.data>/queries` | `SECATOR_DIRS_QUERIES` | Query data. |
| `dirs.celery` | `path` | `<dirs.data>/celery` | `SECATOR_DIRS_CELERY` | Celery data folder. |
| `dirs.celery_data` | `path` | `<dirs.data>/celery/data` | `SECATOR_DIRS_CELERY_DATA` | Filesystem broker data. |
| `dirs.celery_results` | `path` | `<dirs.data>/celery/results` | `SECATOR_DIRS_CELERY_RESULTS` | Filesystem result backend data. |

***

## celery

Celery settings used for distributed runs (see [Distributed runs with Celery](../in-depth/distributed-runs-with-celery.md)).

| Key | Type | Default | Env var | Description |
| --- | --- | --- | --- | --- |
| `celery.broker_url` | `str` | `filesystem://` | `SECATOR_CELERY_BROKER_URL` | Broker URL (`filesystem://`, `redis://host:6379/0`, `amqp://...`). |
| `celery.broker_pool_limit` | `int` | `10` | `SECATOR_CELERY_BROKER_POOL_LIMIT` | Max broker connections. |
| `celery.broker_connection_timeout` | `float` | `4.0` | `SECATOR_CELERY_BROKER_CONNECTION_TIMEOUT` | Broker connection timeout (seconds). |
| `celery.broker_visibility_timeout` | `int` | `3600` | `SECATOR_CELERY_BROKER_VISIBILITY_TIMEOUT` | Broker visibility timeout (seconds). |
| `celery.broker_transport_options` | `str` | `""` | `SECATOR_CELERY_BROKER_TRANSPORT_OPTIONS` | Broker transport options (JSON string). |
| `celery.override_default_logging` | `bool` | `true` | `SECATOR_CELERY_OVERRIDE_DEFAULT_LOGGING` | Replace Celery logging with secator logging. |
| `celery.result_backend` | `str` | `""` | `SECATOR_CELERY_RESULT_BACKEND` | Result backend URL. Empty means `file://<dirs.celery_results>`. |
| `celery.result_backend_transport_options` | `str` | `""` | `SECATOR_CELERY_RESULT_BACKEND_TRANSPORT_OPTIONS` | Result backend transport options (JSON string). |
| `celery.result_expires` | `int` | `86400` | `SECATOR_CELERY_RESULT_EXPIRES` | Result TTL (seconds). |
| `celery.redis_backend_health_check_interval` | `int` | `0` | `SECATOR_CELERY_REDIS_BACKEND_HEALTH_CHECK_INTERVAL` | Redis result backend health check interval (seconds); `0` disables it. Keep it at `0`: enabling it can abort workflows with a Redis `PubSubError`. |
| `celery.task_acks_late` | `bool` | `false` | `SECATOR_CELERY_TASK_ACKS_LATE` | Acknowledge tasks after they finish instead of when they start. |
| `celery.task_send_sent_event` | `bool` | `false` | `SECATOR_CELERY_TASK_SEND_SENT_EVENT` | Emit task-sent events. |
| `celery.task_reject_on_worker_lost` | `bool` | `false` | `SECATOR_CELERY_TASK_REJECT_ON_WORKER_LOST` | Re-queue a task when its worker dies. |
| `celery.task_max_retries` | `int` | `-1` | `SECATOR_CELERY_TASK_MAX_RETRIES` | Max redeliveries of a task whose worker was lost before it is abandoned; `-1` disables the cap. |
| `celery.task_max_timeout` | `int` | `-1` | `SECATOR_CELERY_TASK_MAX_TIMEOUT` | Max task duration (seconds); `-1` = unlimited. Per-task override: `tasks.overrides.<task>.max_timeout`. |
| `celery.task_memory_limit_mb` | `int` | `-1` | `SECATOR_CELERY_TASK_MEMORY_LIMIT_MB` | Max task memory (MB); `-1` = unlimited. |
| `celery.worker_max_tasks_per_child` | `int` | `20` | `SECATOR_CELERY_WORKER_MAX_TASKS_PER_CHILD` | Tasks a worker process runs before it is recycled. |
| `celery.worker_prefetch_multiplier` | `int` | `1` | `SECATOR_CELERY_WORKER_PREFETCH_MULTIPLIER` | Tasks prefetched per worker process. |
| `celery.worker_send_task_events` | `bool` | `false` | `SECATOR_CELERY_WORKER_SEND_TASK_EVENTS` | Workers emit task events. |
| `celery.worker_kill_after_task` | `bool` | `false` | `SECATOR_CELERY_WORKER_KILL_AFTER_TASK` | Stop the worker after each task. |
| `celery.worker_kill_after_idle_seconds` | `int` | `-1` | `SECATOR_CELERY_WORKER_KILL_AFTER_IDLE_SECONDS` | Stop the worker after this many idle seconds; `-1` = never. |
| `celery.worker_command_verbose` | `bool` | `false` | `SECATOR_CELERY_WORKER_COMMAND_VERBOSE` | Print the commands run by the worker. |
| `celery.worker_cancel_long_running_tasks_on_connection_loss` | `bool` | `false` | `SECATOR_CELERY_WORKER_CANCEL_LONG_RUNNING_TASKS_ON_CONNECTION_LOSS` | Cancel in-flight tasks when the worker loses its broker connection (use with `task_acks_late` and `task_reject_on_worker_lost`). |

***

## cli

CLI behaviour.

| Key | Type | Default | Env var | Description |
| --- | --- | --- | --- | --- |
| `cli.github_token` | `str` | `""` | `SECATOR_CLI_GITHUB_TOKEN` | GitHub token used to avoid rate limits when installing tools (defaults to `$GITHUB_TOKEN`). |
| `cli.record` | `bool` | `false` | `SECATOR_CLI_RECORD` | Record CLI sessions. |
| `cli.stdin_timeout` | `int` | `1000` | `SECATOR_CLI_STDIN_TIMEOUT` | Time to wait for stdin input (ms). |
| `cli.show_http_response_headers` | `bool` | `false` | `SECATOR_CLI_SHOW_HTTP_RESPONSE_HEADERS` | Show HTTP response headers in console output. |
| `cli.show_command_output` | `bool` | `false` | `SECATOR_CLI_SHOW_COMMAND_OUTPUT` | Show raw tool output. |
| `cli.exclude_http_response_headers` | `list[str]` | `[connection, content_type, content_length, date, server]` | `SECATOR_CLI_EXCLUDE_HTTP_RESPONSE_HEADERS` | Response headers hidden from console output. |
| `cli.date_format` | `str` | `%m/%d/%Y` | `SECATOR_CLI_DATE_FORMAT` | Date format in CLI output (`%d/%m/%Y` for European format). |

***

## runners

Settings applied to every task, workflow and scan.

| Key | Type | Default | Env var | Description |
| --- | --- | --- | --- | --- |
| `runners.input_chunk_size` | `int` | `100` | `SECATOR_RUNNERS_INPUT_CHUNK_SIZE` | Inputs per chunk when a task is split across workers; `-1` disables chunking. |
| `runners.progress_update_frequency` | `int` | `20` | `SECATOR_RUNNERS_PROGRESS_UPDATE_FREQUENCY` | Progress update interval (seconds). |
| `runners.stat_update_frequency` | `int` | `20` | `SECATOR_RUNNERS_STAT_UPDATE_FREQUENCY` | Runtime stats update interval (seconds). |
| `runners.monitor_worker` | `bool` | `false` | `SECATOR_RUNNERS_MONITOR_WORKER` | Also report the worker process itself in runtime stats (useful with one task per worker). |
| `runners.backend_update_frequency` | `int` | `5` | `SECATOR_RUNNERS_BACKEND_UPDATE_FREQUENCY` | Interval between result pushes to drivers (seconds). |
| `runners.poll_frequency` | `int` | `5` | `SECATOR_RUNNERS_POLL_FREQUENCY` | Interval between result polls when running in a worker (seconds). |
| `runners.skip_cve_search` | `bool` | `false` | `SECATOR_RUNNERS_SKIP_CVE_SEARCH` | Skip CVE lookups. |
| `runners.skip_exploit_search` | `bool` | `false` | `SECATOR_RUNNERS_SKIP_EXPLOIT_SEARCH` | Skip exploit lookups. |
| `runners.skip_cve_low_confidence` | `bool` | `false` | `SECATOR_RUNNERS_SKIP_CVE_LOW_CONFIDENCE` | Skip CVE lookups for low-confidence matches. |
| `runners.remove_duplicates` | `bool` | `false` | `SECATOR_RUNNERS_REMOVE_DUPLICATES` | Remove duplicate findings. |
| `runners.threads` | `int` | `50` | `SECATOR_RUNNERS_THREADS` | Default number of threads. |
| `runners.prompt_timeout` | `int` | `20` | `SECATOR_RUNNERS_PROMPT_TIMEOUT` | Timeout for interactive prompts (seconds). |
| `runners.chunk_rate_limit` | `bool` | `true` | `SECATOR_RUNNERS_CHUNK_RATE_LIMIT` | Divide `rate_limit` by the number of chunks when a task is chunked. |

***

## http

HTTP and proxy settings.

| Key | Type | Default | Env var | Description |
| --- | --- | --- | --- | --- |
| `http.socks5_proxy` | `str` | `socks5://127.0.0.1:9050` | `SECATOR_HTTP_SOCKS5_PROXY` | SOCKS5 proxy used by `-proxy auto` (e.g. Tor). |
| `http.http_proxy` | `str` | `https://127.0.0.1:9080` | `SECATOR_HTTP_HTTP_PROXY` | HTTP proxy used by `-proxy auto`. |
| `http.store_responses` | `bool` | `true` | `SECATOR_HTTP_STORE_RESPONSES` | Store HTTP responses on disk. |
| `http.response_max_size_bytes` | `int` | `100000` | `SECATOR_HTTP_RESPONSE_MAX_SIZE_BYTES` | Max stored response size (bytes). |
| `http.proxychains_command` | `str` | `proxychains` | `SECATOR_HTTP_PROXYCHAINS_COMMAND` | Proxychains binary used by `-proxy proxychains`. |
| `http.freeproxy_timeout` | `int` | `1` | `SECATOR_HTTP_FREEPROXY_TIMEOUT` | Timeout used when testing free proxies (seconds). |
| `http.default_header` | `str` | `User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36` | `SECATOR_HTTP_DEFAULT_HEADER` | Default header sent by HTTP tasks. |

***

## tasks

Task settings.

| Key | Type | Default | Env var | Description |
| --- | --- | --- | --- | --- |
| `tasks.exporters` | `list[str]` | `[csv, txt, markdown]` | `SECATOR_TASKS_EXPORTERS` | Default exporters for tasks. |
| `tasks.overrides` | `dict[str, dict[str, any]]` | `{}` | `SECATOR_TASKS_OVERRIDES_<TASK>_<ATTR>` | Per-task attribute overrides, e.g. `tasks.overrides.nmap.max_timeout: 600` (see [Task overrides](configuration.md#task-overrides)). |

***

## workflows

Workflow settings.

| Key | Type | Default | Env var | Description |
| --- | --- | --- | --- | --- |
| `workflows.exporters` | `list[str]` | `[csv, txt, markdown]` | `SECATOR_WORKFLOWS_EXPORTERS` | Default exporters for workflows. |

***

## scans

Scan settings.

| Key | Type | Default | Env var | Description |
| --- | --- | --- | --- | --- |
| `scans.exporters` | `list[str]` | `[csv, txt, markdown]` | `SECATOR_SCANS_EXPORTERS` | Default exporters for scans. |

***

## payloads

Payloads served by `secator u serve`.

| Key | Type | Default | Env var | Description |
| --- | --- | --- | --- | --- |
| `payloads.templates` | `dict[str, str]` | `lse`, `linpeas`, `sudo_killer` | `SECATOR_PAYLOADS_TEMPLATES_<KEY>` | Payload name -> URL, `git+https://` repository or local path. |

***

## wordlists

Wordlists used by fuzzing and brute-force tasks.

| Key | Type | Default | Env var | Description |
| --- | --- | --- | --- | --- |
| `wordlists.defaults` | `dict[str, str]` | `http`, `dns`, `http_params` | `SECATOR_WORDLISTS_DEFAULTS_<KEY>` | Default wordlist per type (`http`, `dns`, `http_params`). |
| `wordlists.templates` | `dict[str, str]` | `bo0m_fuzz`, `combined_subdomains`, `directory_list_small`, `burp-parameter-names` | `SECATOR_WORDLISTS_TEMPLATES_<KEY>` | Wordlist name -> URL or local path. |
| `wordlists.lists` | `dict[str, list[str]]` | `{}` | `SECATOR_WORDLISTS_LISTS_<KEY>` | Inline wordlists (name -> list of words). |

***

## profiles

Profiles (see [Profiles](../in-depth/concepts/profiles.md)).

| Key | Type | Default | Env var | Description |
| --- | --- | --- | --- | --- |
| `profiles.defaults` | `list[str]` | `[]` | `SECATOR_PROFILES_DEFAULTS` | Profiles applied to every run. |

***

## drivers

Drivers (see [Drivers](../in-depth/concepts/drivers.md)).

| Key | Type | Default | Env var | Description |
| --- | --- | --- | --- | --- |
| `drivers.defaults` | `list[str]` | `[]` | `SECATOR_DRIVERS_DEFAULTS` | Drivers applied to every run. |

***

## workspaces

Workspaces (see [Workspaces](../in-depth/concepts/workspaces.md)). `workspaces.routes` is deprecated and ignored (a one-time warning is printed if your config still sets it).

| Key | Type | Default | Env var | Description |
| --- | --- | --- | --- | --- |
| `workspaces.current` | `str` | `""` | `SECATOR_WORKSPACES_CURRENT` | Current workspace (set with `secator ws use <name>`). Empty means `default`. |
| `workspaces.profiles` | `dict[str, list[str]]` | `{}` | `SECATOR_WORKSPACES_PROFILES_<KEY>` | Default profiles per workspace: workspace -> list of profiles. |

***

## addons

Addon settings. Install addons with `secator install addons <name>`.

| Key | Type | Default | Env var | Description |
| --- | --- | --- | --- | --- |
| `addons.gdrive.enabled` | `bool` | `false` | `SECATOR_ADDONS_GDRIVE_ENABLED` | Enable the Google Drive exporter. |
| `addons.gdrive.drive_parent_folder_id` | `str` | `""` | `SECATOR_ADDONS_GDRIVE_DRIVE_PARENT_FOLDER_ID` | Parent Google Drive folder ID. |
| `addons.gdrive.credentials_path` | `str` | `""` | `SECATOR_ADDONS_GDRIVE_CREDENTIALS_PATH` | Path to the service account credentials JSON. |
| `addons.gcs.enabled` | `bool` | `false` | `SECATOR_ADDONS_GCS_ENABLED` | Enable the Google Cloud Storage driver. |
| `addons.gcs.bucket_name` | `str` | `""` | `SECATOR_ADDONS_GCS_BUCKET_NAME` | Bucket name. |
| `addons.gcs.credentials_path` | `str` | `""` | `SECATOR_ADDONS_GCS_CREDENTIALS_PATH` | Optional path to credentials JSON (Application Default Credentials are used otherwise). |
| `addons.worker.enabled` | `bool` | `false` | `SECATOR_ADDONS_WORKER_ENABLED` | Enable the worker addon. |
| `addons.mongodb.enabled` | `bool` | `false` | `SECATOR_ADDONS_MONGODB_ENABLED` | Enable the MongoDB driver. |
| `addons.mongodb.url` | `str` | `mongodb://localhost` | `SECATOR_ADDONS_MONGODB_URL` | MongoDB connection URL. |
| `addons.mongodb.update_frequency` | `int` | `60` | `SECATOR_ADDONS_MONGODB_UPDATE_FREQUENCY` | Min interval between runner updates (seconds). |
| `addons.mongodb.max_pool_size` | `int` | `10` | `SECATOR_ADDONS_MONGODB_MAX_POOL_SIZE` | Max connection pool size. |
| `addons.mongodb.server_selection_timeout_ms` | `int` | `5000` | `SECATOR_ADDONS_MONGODB_SERVER_SELECTION_TIMEOUT_MS` | Server selection timeout (ms). |
| `addons.mongodb.max_items` | `int` | `-1` | `SECATOR_ADDONS_MONGODB_MAX_ITEMS` | Max items loaded per query; `-1` = unlimited. |
| `addons.mongodb.duplicate_exclude_types` | `list[str]` | `[info, warning, error, stat]` | `SECATOR_ADDONS_MONGODB_DUPLICATE_EXCLUDE_TYPES` | Output types never considered for duplicate tagging. |
| `addons.mongodb.duplicate_main_copy_fields` | `list[str]` | `[screenshot_path, stored_response_path, is_false_positive, is_acknowledged, verified, status, tags, poc]` | `SECATOR_ADDONS_MONGODB_DUPLICATE_MAIN_COPY_FIELDS` | Fields carried over from a previous copy of a finding onto the newly found one (when empty there), e.g. triage status. |
| `addons.sqlite.enabled` | `bool` | `false` | `SECATOR_ADDONS_SQLITE_ENABLED` | Enable the SQLite driver. |
| `addons.sqlite.path` | `str` | `""` | `SECATOR_ADDONS_SQLITE_PATH` | Database file path. Empty means `<dirs.data>/secator.db`. |
| `addons.sqlite.busy_timeout_ms` | `int` | `5000` | `SECATOR_ADDONS_SQLITE_BUSY_TIMEOUT_MS` | SQLite busy timeout (ms). |
| `addons.sqlite.max_items` | `int` | `-1` | `SECATOR_ADDONS_SQLITE_MAX_ITEMS` | Max items loaded per query; `-1` = unlimited. |
| `addons.sqlite.duplicate_main_copy_fields` | `list[str]` | `[screenshot_path, stored_response_path, is_false_positive, is_acknowledged, verified, status, tags, poc]` | `SECATOR_ADDONS_SQLITE_DUPLICATE_MAIN_COPY_FIELDS` | Fields carried over from a previous copy of a finding onto the newly found one (when empty there), e.g. triage status. |
| `addons.vulners.enabled` | `bool` | `false` | `SECATOR_ADDONS_VULNERS_ENABLED` | Enable the Vulners CVE provider. |
| `addons.vulners.api_key` | `str` | `""` | `SECATOR_ADDONS_VULNERS_API_KEY` | Vulners API key. |
| `addons.discord.enabled` | `bool` | `false` | `SECATOR_ADDONS_DISCORD_ENABLED` | Enable the Discord driver. |
| `addons.discord.webhook_url` | `str` | `""` | `SECATOR_ADDONS_DISCORD_WEBHOOK_URL` | Discord webhook URL. |
| `addons.discord.bot_token` | `str` | `""` | `SECATOR_ADDONS_DISCORD_BOT_TOKEN` | Discord bot token (alternative to the webhook). |
| `addons.discord.send_runner_updates` | `bool` | `true` | `SECATOR_ADDONS_DISCORD_SEND_RUNNER_UPDATES` | Send runner start / end notifications. |
| `addons.discord.send_findings` | `bool` | `true` | `SECATOR_ADDONS_DISCORD_SEND_FINDINGS` | Send finding notifications. |
| `addons.discord.finding_types` | `list[str]` | `[vulnerability]` | `SECATOR_ADDONS_DISCORD_FINDING_TYPES` | Output types to notify. |
| `addons.discord.min_severity` | `str` | `high` | `SECATOR_ADDONS_DISCORD_MIN_SEVERITY` | Minimum vulnerability severity to notify. |
| `addons.api.enabled` | `bool` | `false` | `SECATOR_ADDONS_API_ENABLED` | Enable the `api` driver. |
| `addons.api.url` | `str` | see `secator config default` | `SECATOR_ADDONS_API_URL` | Base URL of the HTTP API. |
| `addons.api.key` | `str` | `""` | `SECATOR_ADDONS_API_KEY` | API key. |
| `addons.api.header_name` | `str` | `Bearer` | `SECATOR_ADDONS_API_HEADER_NAME` | Authorization scheme sent before the key. |
| `addons.api.force_ssl` | `bool` | `true` | `SECATOR_ADDONS_API_FORCE_SSL` | Verify TLS certificates. |
| `addons.api.timeout` | `int` | `60` | `SECATOR_ADDONS_API_TIMEOUT` | Request timeout (seconds). |
| `addons.api.org_id` | `int` | `null` | `SECATOR_ADDONS_API_ORG_ID` | Organization ID to query (admins only); defaults to the user's own. |
| `addons.api.runner_create_endpoint` | `str` | `runners` | `SECATOR_ADDONS_API_RUNNER_CREATE_ENDPOINT` | Endpoint path (relative to `url`). |
| `addons.api.runner_get_endpoint` | `str` | `runner/{runner_id}` | `SECATOR_ADDONS_API_RUNNER_GET_ENDPOINT` | Endpoint path (relative to `url`). |
| `addons.api.runner_update_endpoint` | `str` | `runner/{runner_id}` | `SECATOR_ADDONS_API_RUNNER_UPDATE_ENDPOINT` | Endpoint path (relative to `url`). |
| `addons.api.finding_create_endpoint` | `str` | `findings` | `SECATOR_ADDONS_API_FINDING_CREATE_ENDPOINT` | Endpoint path (relative to `url`). |
| `addons.api.finding_update_endpoint` | `str` | `finding/{finding_id}` | `SECATOR_ADDONS_API_FINDING_UPDATE_ENDPOINT` | Endpoint path (relative to `url`). |
| `addons.api.finding_search_endpoint` | `str` | `findings/_search` | `SECATOR_ADDONS_API_FINDING_SEARCH_ENDPOINT` | Endpoint path (relative to `url`). |
| `addons.api.workspace_list_endpoint` | `str` | `workspaces` | `SECATOR_ADDONS_API_WORKSPACE_LIST_ENDPOINT` | Endpoint path (relative to `url`). |
| `addons.api.workspace_create_endpoint` | `str` | `workspaces` | `SECATOR_ADDONS_API_WORKSPACE_CREATE_ENDPOINT` | Endpoint path (relative to `url`). |
| `addons.api.workspace_get_endpoint` | `str` | `workspace/{workspace_id}` | `SECATOR_ADDONS_API_WORKSPACE_GET_ENDPOINT` | Endpoint path (relative to `url`). |
| `addons.api.workspace_delete_endpoint` | `str` | `workspace/{workspace_id}` | `SECATOR_ADDONS_API_WORKSPACE_DELETE_ENDPOINT` | Endpoint path (relative to `url`). |
| `addons.api.runners_list_endpoint` | `str` | `runners/any` | `SECATOR_ADDONS_API_RUNNERS_LIST_ENDPOINT` | Endpoint path (relative to `url`). |
| `addons.api.runner_delete_endpoint` | `str` | `runner/{runner_id}?type={runner_type}` | `SECATOR_ADDONS_API_RUNNER_DELETE_ENDPOINT` | Endpoint path (relative to `url`). |
| `addons.ai.enabled` | `bool` | `false` | `SECATOR_ADDONS_AI_ENABLED` | Enable the `ai` task. |
| `addons.ai.api_key` | `str` | `""` | `SECATOR_ADDONS_AI_API_KEY` | LLM provider API key. |
| `addons.ai.api_base` | `str` | `""` | `SECATOR_ADDONS_AI_API_BASE` | Custom LLM API base URL (e.g. a local OpenAI-compatible server). |
| `addons.ai.custom_disallow_config_token` | `bool` | `false` | `SECATOR_ADDONS_AI_CUSTOM_DISALLOW_CONFIG_TOKEN` | When a caller sets a custom `api_base`, require it to also pass its own API key instead of reusing `api_key`. |
| `addons.ai.default_model` | `str` | `claude-sonnet-4-6` | `SECATOR_ADDONS_AI_DEFAULT_MODEL` | Default model. |
| `addons.ai.intent_model` | `str` | `claude-haiku-4-5` | `SECATOR_ADDONS_AI_INTENT_MODEL` | Lightweight model used for intent detection. |
| `addons.ai.temperature` | `float` | `0.7` | `SECATOR_ADDONS_AI_TEMPERATURE` | Sampling temperature. |
| `addons.ai.max_tokens` | `int` | `30000` | `SECATOR_ADDONS_AI_MAX_TOKENS` | Max tokens per response. |
| `addons.ai.max_tokens_total` | `int` | `100000` | `SECATOR_ADDONS_AI_MAX_TOKENS_TOTAL` | Max tokens kept in the conversation (oldest messages are truncated). |
| `addons.ai.max_results` | `int` | `500` | `SECATOR_ADDONS_AI_MAX_RESULTS` | Max results passed to the model. |
| `addons.ai.max_iterations` | `int` | `25` | `SECATOR_ADDONS_AI_MAX_ITERATIONS` | Max agent iterations per run; `-1` (or `<= 0`) disables the cap. |
| `addons.ai.context_window` | `int` | `128000` | `SECATOR_ADDONS_AI_CONTEXT_WINDOW` | Model context window used when the provider does not report one. |
| `addons.ai.user_response_timeout` | `int` | `600` | `SECATOR_ADDONS_AI_USER_RESPONSE_TIMEOUT` | Time to wait for a user answer (seconds). |
| `addons.ai.encrypt_pii` | `bool` | `true` | `SECATOR_ADDONS_AI_ENCRYPT_PII` | Encrypt sensitive data before sending it to the model. |
| `addons.ai.permissions` | `dict` | see [AI task](../in-depth/ai-task.md#permission-engine) | `SECATOR_ADDONS_AI_PERMISSIONS` | Permission rules (`allow` / `deny` / `ask`), see [AI task](../in-depth/ai-task.md). |

***

## security

Security controls.

| Key | Type | Default | Env var | Description |
| --- | --- | --- | --- | --- |
| `security.allow_local_file_access` | `bool` | `true` | `SECATOR_SECURITY_ALLOW_LOCAL_FILE_ACCESS` | Allow wordlists / payloads to be loaded from local files outside `dirs.data`. |
| `security.auto_install_commands` | `bool` | `true` | `SECATOR_SECURITY_AUTO_INSTALL_COMMANDS` | Install missing tools automatically on first use. |
| `security.force_source_install` | `bool` | `false` | `SECATOR_SECURITY_FORCE_SOURCE_INSTALL` | Build tools from source instead of downloading binaries. |
| `security.prompt_sudo_password` | `bool` | `true` | `SECATOR_SECURITY_PROMPT_SUDO_PASSWORD` | Prompt for the sudo password when a task needs it. |
| `security.sudo_password` | `str` | `""` | `SECATOR_SECURITY_SUDO_PASSWORD` | Non-interactive sudo password, for headless workers (prefer the env var). |
| `security.shell_isolated` | `bool` | `false` | `SECATOR_SECURITY_SHELL_ISOLATED` | Default for the `ai` task `--isolated` flag (run shell commands in a Docker sandbox). |
| `security.scope_hard_deny` | `bool` | `false` | `SECATOR_SECURITY_SCOPE_HARD_DENY` | Deny out-of-scope AI targets outright instead of asking for approval. |

***

## providers

Default enrichment providers.

| Key | Type | Default | Env var | Description |
| --- | --- | --- | --- | --- |
| `providers.defaults` | `dict[str, str]` | `cve: circl`<br>`exploit: exploitdb`<br>`ghsa: ghsa` | `SECATOR_PROVIDERS_DEFAULTS_<KEY>` | Default provider per data type (`cve`: `circl` or `vulners`, `exploit`: `exploitdb`, `ghsa`: `ghsa`). |

***

## queries

Saved queries for `secator query` (see [Querying results](querying-results.md)).

| Key | Type | Default | Env var | Description |
| --- | --- | --- | --- | --- |
| `queries` | `dict[str, str]` | `{}` | `SECATOR_QUERIES_<KEY>` | Saved queries: name -> query expression. |

***

## offline_mode

Offline mode.

| Key | Type | Default | Env var | Description |
| --- | --- | --- | --- | --- |
| `offline_mode` | `bool` | `false` | `SECATOR_OFFLINE_MODE` | Disable all network downloads and lookups (wordlists, payloads, tools, CVEs). |

