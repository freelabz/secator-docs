#!/usr/bin/env python3
"""Regenerate getting-started/configuration-reference.md from secator's pydantic config models.

Usage (from the root of this repo, with secator installed or its source on PYTHONPATH):

    python scripts/generate_config_reference.py > getting-started/configuration-reference.md

Keys, types, defaults and env var names come from `secator.config.SecatorConfig`.
Descriptions are curated below in DESCRIPTIONS; a key missing from it is flagged with
"TODO" in the output so new options are easy to spot after a secator release.
"""
import typing
from pathlib import Path

from pydantic import BaseModel

from secator.config import SecatorConfig

HOME = str(Path.home())

SECTIONS = {
	'debug': 'Debug output filtering.',
	'dirs': 'Directories used by secator. Unset directories are created under `dirs.data`.',
	'celery': 'Celery settings used for distributed runs (see [Distributed runs with Celery](../in-depth/distributed-runs-with-celery.md)).',  # noqa: E501
	'cli': 'CLI behaviour.',
	'runners': 'Settings applied to every task, workflow and scan.',
	'http': 'HTTP and proxy settings.',
	'tasks': 'Task settings.',
	'workflows': 'Workflow settings.',
	'scans': 'Scan settings.',
	'payloads': 'Payloads served by `secator u serve`.',
	'wordlists': 'Wordlists used by fuzzing and brute-force tasks.',
	'profiles': 'Profiles (see [Profiles](../in-depth/concepts/profiles.md)).',
	'drivers': 'Drivers (see [Drivers](../in-depth/concepts/drivers.md)).',
	'workspaces': 'Workspaces (see [Workspaces](../in-depth/concepts/workspaces.md)).',
	'addons': 'Addon settings. Install addons with `secator install addons <name>`.',
	'security': 'Security controls.',
	'providers': 'Default enrichment providers.',
	'queries': 'Saved queries for `secator query` (see [Querying results](querying-results.md)).',
	'offline_mode': 'Offline mode.',
}

DESCRIPTIONS = {
	'debug': 'Comma-separated debug components to print (`all` for everything, prefix match, or a regex such as `cve.*`).',  # noqa: E501
	'dirs.bin': 'Where tool binaries are installed.',
	'dirs.share': 'Where shared tool data is installed.',
	'dirs.data': 'Root data folder. `config.yml` is read from this folder, so change it with the `SECATOR_DIRS_DATA` env var.',  # noqa: E501
	'dirs.templates': 'Custom task, workflow, scan and profile templates.',
	'dirs.reports': 'Reports, one subfolder per workspace.',
	'dirs.wordlists': 'Downloaded wordlists.',
	'dirs.cves': 'Cached CVE data.',
	'dirs.payloads': 'Downloaded payloads.',
	'dirs.performance': 'Profiling output (`-pyinstrument`, `-memray`).',
	'dirs.revshells': 'Reverse shells data.',
	'dirs.queries': 'Query data.',
	'dirs.celery': 'Celery data folder.',
	'dirs.celery_data': 'Filesystem broker data.',
	'dirs.celery_results': 'Filesystem result backend data.',
	'celery.broker_url': 'Broker URL (`filesystem://`, `redis://host:6379/0`, `amqp://...`).',
	'celery.broker_pool_limit': 'Max broker connections.',
	'celery.broker_connection_timeout': 'Broker connection timeout (seconds).',
	'celery.broker_visibility_timeout': 'Broker visibility timeout (seconds).',
	'celery.broker_transport_options': 'Broker transport options (JSON string).',
	'celery.override_default_logging': 'Replace Celery logging with secator logging.',
	'celery.result_backend': 'Result backend URL. Empty means `file://<dirs.celery_results>`.',
	'celery.result_backend_transport_options': 'Result backend transport options (JSON string).',
	'celery.result_expires': 'Result TTL (seconds).',
	'celery.redis_backend_health_check_interval': 'Redis result backend health check interval (seconds); `0` disables it. Keep it at `0`: enabling it can abort workflows with a Redis `PubSubError`.',  # noqa: E501
	'celery.task_acks_late': 'Acknowledge tasks after they finish instead of when they start.',
	'celery.task_send_sent_event': 'Emit task-sent events.',
	'celery.task_reject_on_worker_lost': 'Re-queue a task when its worker dies.',
	'celery.task_max_retries': 'Max redeliveries of a task whose worker was lost before it is abandoned; `-1` disables the cap.',  # noqa: E501
	'celery.task_max_timeout': 'Max task duration (seconds); `-1` = unlimited. Per-task override: `tasks.overrides.<task>.max_timeout`.',  # noqa: E501
	'celery.task_memory_limit_mb': 'Max task memory (MB); `-1` = unlimited.',
	'celery.worker_max_tasks_per_child': 'Tasks a worker process runs before it is recycled.',
	'celery.worker_prefetch_multiplier': 'Tasks prefetched per worker process.',
	'celery.worker_send_task_events': 'Workers emit task events.',
	'celery.worker_kill_after_task': 'Stop the worker after each task.',
	'celery.worker_kill_after_idle_seconds': 'Stop the worker after this many idle seconds; `-1` = never.',
	'celery.worker_command_verbose': 'Print the commands run by the worker.',
	'celery.worker_cancel_long_running_tasks_on_connection_loss': 'Cancel in-flight tasks when the worker loses its broker connection (use with `task_acks_late` and `task_reject_on_worker_lost`).',  # noqa: E501
	'cli.github_token': 'GitHub token used to avoid rate limits when installing tools (defaults to `$GITHUB_TOKEN`).',
	'cli.record': 'Record CLI sessions.',
	'cli.stdin_timeout': 'Time to wait for stdin input (ms).',
	'cli.show_http_response_headers': 'Show HTTP response headers in console output.',
	'cli.show_command_output': 'Show raw tool output.',
	'cli.exclude_http_response_headers': 'Response headers hidden from console output.',
	'cli.date_format': 'Date format in CLI output (`%d/%m/%Y` for European format).',
	'runners.input_chunk_size': 'Inputs per chunk when a task is split across workers; `-1` disables chunking.',
	'runners.progress_update_frequency': 'Progress update interval (seconds).',
	'runners.stat_update_frequency': 'Runtime stats update interval (seconds).',
	'runners.monitor_worker': 'Also report the worker process itself in runtime stats (useful with one task per worker).',
	'runners.backend_update_frequency': 'Interval between result pushes to drivers (seconds).',
	'runners.poll_frequency': 'Interval between result polls when running in a worker (seconds).',
	'runners.skip_cve_search': 'Skip CVE lookups.',
	'runners.skip_exploit_search': 'Skip exploit lookups.',
	'runners.skip_cve_low_confidence': 'Skip CVE lookups for low-confidence matches.',
	'runners.remove_duplicates': 'Remove duplicate findings.',
	'runners.threads': 'Default number of threads.',
	'runners.prompt_timeout': 'Timeout for interactive prompts (seconds).',
	'runners.chunk_rate_limit': 'Divide `rate_limit` by the number of chunks when a task is chunked.',
	'http.socks5_proxy': 'SOCKS5 proxy used by `-proxy auto` (e.g. Tor).',
	'http.http_proxy': 'HTTP proxy used by `-proxy auto`.',
	'http.store_responses': 'Store HTTP responses on disk.',
	'http.response_max_size_bytes': 'Max stored response size (bytes).',
	'http.proxychains_command': 'Proxychains binary used by `-proxy proxychains`.',
	'http.freeproxy_timeout': 'Timeout used when testing free proxies (seconds).',
	'http.default_header': 'Default header sent by HTTP tasks.',
	'tasks.exporters': 'Default exporters for tasks.',
	'tasks.overrides': 'Per-task attribute overrides, e.g. `tasks.overrides.nmap.max_timeout: 600` (see [Task overrides](configuration.md#task-overrides)).',  # noqa: E501
	'workflows.exporters': 'Default exporters for workflows.',
	'scans.exporters': 'Default exporters for scans.',
	'payloads.templates': 'Payload name -> URL, `git+https://` repository or local path.',
	'wordlists.defaults': 'Default wordlist per type (`http`, `dns`, `http_params`).',
	'wordlists.templates': 'Wordlist name -> URL or local path.',
	'wordlists.lists': 'Inline wordlists (name -> list of words).',
	'profiles.defaults': 'Profiles applied to every run.',
	'drivers.defaults': 'Drivers applied to every run.',
	'workspaces.current': 'Current workspace (set with `secator ws use <name>`). Empty means `default`.',
	'workspaces.routes': 'Automatic workspace routing: workspace -> list of glob patterns matched against inputs.',
	'workspaces.profiles': 'Default profiles per workspace: workspace -> list of profiles.',
	'addons.gdrive.enabled': 'Enable the Google Drive exporter.',
	'addons.gdrive.drive_parent_folder_id': 'Parent Google Drive folder ID.',
	'addons.gdrive.credentials_path': 'Path to the service account credentials JSON.',
	'addons.gcs.enabled': 'Enable the Google Cloud Storage driver.',
	'addons.gcs.bucket_name': 'Bucket name.',
	'addons.gcs.credentials_path': 'Optional path to credentials JSON (Application Default Credentials are used otherwise).',
	'addons.worker.enabled': 'Enable the worker addon.',
	'addons.mongodb.enabled': 'Enable the MongoDB driver.',
	'addons.mongodb.url': 'MongoDB connection URL.',
	'addons.mongodb.update_frequency': 'Min interval between runner updates (seconds).',
	'addons.mongodb.max_pool_size': 'Max connection pool size.',
	'addons.mongodb.server_selection_timeout_ms': 'Server selection timeout (ms).',
	'addons.mongodb.max_items': 'Max items loaded per query; `-1` = unlimited.',
	'addons.mongodb.duplicate_exclude_types': 'Output types never considered for duplicate tagging.',
	'addons.mongodb.duplicate_main_copy_fields': 'Fields carried over from a previous copy of a finding onto the newly found one (when empty there), e.g. triage status.',
	'addons.sqlite.enabled': 'Enable the SQLite driver.',
	'addons.sqlite.path': 'Database file path. Empty means `<dirs.data>/secator.db`.',
	'addons.sqlite.busy_timeout_ms': 'SQLite busy timeout (ms).',
	'addons.sqlite.max_items': 'Max items loaded per query; `-1` = unlimited.',
	'addons.sqlite.duplicate_main_copy_fields': 'Fields carried over from a previous copy of a finding onto the newly found one (when empty there), e.g. triage status.',
	'addons.vulners.enabled': 'Enable the Vulners CVE provider.',
	'addons.vulners.api_key': 'Vulners API key.',
	'addons.discord.enabled': 'Enable the Discord driver.',
	'addons.discord.webhook_url': 'Discord webhook URL.',
	'addons.discord.bot_token': 'Discord bot token (alternative to the webhook).',
	'addons.discord.send_runner_updates': 'Send runner start / end notifications.',
	'addons.discord.send_findings': 'Send finding notifications.',
	'addons.discord.finding_types': 'Output types to notify.',
	'addons.discord.min_severity': 'Minimum vulnerability severity to notify.',
	'addons.api.enabled': 'Enable the `api` driver.',
	'addons.api.url': 'Base URL of the HTTP API.',
	'addons.api.key': 'API key.',
	'addons.api.header_name': 'Authorization scheme sent before the key.',
	'addons.api.force_ssl': 'Verify TLS certificates.',
	'addons.api.timeout': 'Request timeout (seconds).',
	'addons.api.org_id': 'Organization ID to query (admins only); defaults to the user\'s own.',
	'addons.api.runner_create_endpoint': 'Endpoint path (relative to `url`).',
	'addons.api.runner_get_endpoint': 'Endpoint path (relative to `url`).',
	'addons.api.runner_update_endpoint': 'Endpoint path (relative to `url`).',
	'addons.api.finding_create_endpoint': 'Endpoint path (relative to `url`).',
	'addons.api.finding_update_endpoint': 'Endpoint path (relative to `url`).',
	'addons.api.finding_search_endpoint': 'Endpoint path (relative to `url`).',
	'addons.api.workspace_list_endpoint': 'Endpoint path (relative to `url`).',
	'addons.api.workspace_create_endpoint': 'Endpoint path (relative to `url`).',
	'addons.api.workspace_get_endpoint': 'Endpoint path (relative to `url`).',
	'addons.api.workspace_delete_endpoint': 'Endpoint path (relative to `url`).',
	'addons.api.runners_list_endpoint': 'Endpoint path (relative to `url`).',
	'addons.api.runner_delete_endpoint': 'Endpoint path (relative to `url`).',
	'addons.ai.enabled': 'Enable the `ai` task.',
	'addons.ai.api_key': 'LLM provider API key.',
	'addons.ai.api_base': 'Custom LLM API base URL (e.g. a local OpenAI-compatible server).',
	'addons.ai.custom_disallow_config_token': 'When a caller sets a custom `api_base`, require it to also pass its own API key instead of reusing `api_key`.',  # noqa: E501
	'addons.ai.default_model': 'Default model.',
	'addons.ai.intent_model': 'Lightweight model used for intent detection.',
	'addons.ai.temperature': 'Sampling temperature.',
	'addons.ai.max_tokens': 'Max tokens per response.',
	'addons.ai.max_tokens_total': 'Max tokens kept in the conversation (oldest messages are truncated).',
	'addons.ai.max_results': 'Max results passed to the model.',
	'addons.ai.max_iterations': 'Max agent iterations per run; `-1` (or `<= 0`) disables the cap.',
	'addons.ai.context_window': 'Model context window used when the provider does not report one.',
	'addons.ai.user_response_timeout': 'Time to wait for a user answer (seconds).',
	'addons.ai.encrypt_pii': 'Encrypt sensitive data before sending it to the model.',
	'addons.ai.permissions': 'Permission rules (`allow` / `deny` / `ask`), see [AI task](../in-depth/ai-task.md).',
	'security.allow_local_file_access': 'Allow wordlists / payloads to be loaded from local files outside `dirs.data`.',
	'security.auto_install_commands': 'Install missing tools automatically on first use.',
	'security.force_source_install': 'Build tools from source instead of downloading binaries.',
	'security.prompt_sudo_password': 'Prompt for the sudo password when a task needs it.',
	'security.sudo_password': 'Non-interactive sudo password, for headless workers (prefer the env var).',
	'security.shell_isolated': 'Default for the `ai` task `--isolated` flag (run shell commands in a Docker sandbox).',
	'security.scope_hard_deny': 'Deny out-of-scope AI targets outright instead of asking for approval.',
	'providers.defaults': 'Default provider per data type (`cve`: `circl` or `vulners`, `exploit`: `exploitdb`, `ghsa`: `ghsa`).',  # noqa: E501
	'queries': 'Saved queries: name -> query expression.',
	'offline_mode': 'Disable all network downloads and lookups (wordlists, payloads, tools, CVEs).',
}


def fmt_type(annotation):
	origin = typing.get_origin(annotation)
	if origin is typing.Annotated:
		return fmt_type(typing.get_args(annotation)[0])
	if origin is typing.Union:
		args = [a for a in typing.get_args(annotation) if a is not type(None)]
		return fmt_type(args[0]) if len(args) == 1 else ' | '.join(fmt_type(a) for a in args)
	if origin in (list, typing.List):
		return f'list[{fmt_type(typing.get_args(annotation)[0])}]'
	if origin in (dict, typing.Dict):
		args = typing.get_args(annotation)
		return f'dict[{fmt_type(args[0])}, {fmt_type(args[1])}]' if args else 'dict'
	if annotation is typing.Any:
		return 'any'
	if annotation is dict:
		return 'dict'
	if getattr(annotation, '__name__', None) == 'PosixPath' or annotation is Path:
		return 'path'
	return getattr(annotation, '__name__', str(annotation))


def fmt_default(path, value):
	if path == 'addons.api.url':
		return 'see `secator config default`'
	if isinstance(value, Path):
		value = str(value)
	if isinstance(value, str):
		value = value.replace(HOME, '~')
		if path.startswith('dirs.') and path not in ('dirs.bin', 'dirs.share', 'dirs.data'):
			value = '<dirs.data>/' + path.split('.', 1)[1].replace('_', '/')
		return f'`{value}`' if value else '`""`'
	if value is None:
		return '`null`'
	if isinstance(value, bool):
		return f'`{str(value).lower()}`'
	if isinstance(value, dict):
		if path == 'addons.ai.permissions':
			return 'see [AI task](../in-depth/ai-task.md#permission-engine)'
		if not value:
			return '`{}`'
		if len(str(value)) > 80:
			return ', '.join(f'`{k}`' for k in value)
		return '<br>'.join(f'`{k}: {v}`' for k, v in value.items())
	if isinstance(value, list):
		return '`[' + ', '.join(str(v) for v in value) + ']`' if value else '`[]`'
	return f'`{value}`'


def rows(model, instance, prefix):
	for name, field in model.model_fields.items():
		path = f'{prefix}{name}'
		annotation = field.annotation
		value = getattr(instance, name)
		if isinstance(annotation, type) and issubclass(annotation, BaseModel):
			yield from rows(annotation, value, path + '.')
			continue
		desc = DESCRIPTIONS.get(path, 'TODO: describe')
		yield f'| `{path}` | `{fmt_type(annotation)}` | {fmt_default(path, value)} | `{env_var(path, annotation)}` | {desc} |'


def env_var(path, annotation):
	env = 'SECATOR_' + path.upper().replace('.', '_')
	if path == 'tasks.overrides':
		return env + '_<TASK>_<ATTR>'
	if typing.get_origin(annotation) in (dict, typing.Dict) and path != 'addons.ai.permissions':
		return env + '_<KEY>'
	return env


def main():
	config = SecatorConfig()
	out = [
		'---',
		'description: ... or every configuration option, its default and its env var.',
		'---',
		'',
		'# Configuration reference',
		'',
		'{% hint style="info" %}',
		'This page is generated from secator\'s configuration models by `scripts/generate_config_reference.py`'
		' in the docs repository. To see the defaults of your installed version, run `secator config default`.',
		'{% endhint %}',
		'',
		'Set any key in `~/.secator/config.yml` (or with `secator config set <key> <value>`), or override it with'
		' its environment variable. See [Configuration](configuration.md) for how config files and overrides work.',
		'',
	]
	for name, field in SecatorConfig.model_fields.items():
		out += ['***', '', f'## {name}', '', SECTIONS.get(name, ''), '']
		out += ['| Key | Type | Default | Env var | Description |', '| --- | --- | --- | --- | --- |']
		annotation = field.annotation
		value = getattr(config, name)
		if isinstance(annotation, type) and issubclass(annotation, BaseModel):
			out += list(rows(annotation, value, name + '.'))
		else:
			desc = DESCRIPTIONS.get(name, 'TODO: describe')
			out.append(f'| `{name}` | `{fmt_type(annotation)}` | {fmt_default(name, value)} | `{env_var(name, annotation)}` | {desc} |')  # noqa: E501
		out.append('')
	print('\n'.join(out))


if __name__ == '__main__':
	main()
