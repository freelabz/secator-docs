---
description: ... how to configure every aspect of how secator operates.
---

# Configuration

***

## Default configuration

`secator` is configured using a YAML config file.

The default configuration is as follow:

```yaml
dirs:
  bin: ~/.local/bin
  share: ~/.local/share
  data: ~/.secator
  templates: ~/.secator/templates
  reports: ~/.secator/reports
  wordlists: ~/.secator/wordlists
  cves: ~/.secator/cves
  payloads: ~/.secator/payloads
  performance: ~/.secator/performance
  revshells: ~/.secator/revshells
  celery: ~/.secator/celery
  celery_data: ~/.secator/celery/data
  celery_results: ~/.secator/celery/results

debug:
  level: 0
  component: ''

celery:
  broker_url: filesystem://
  broker_pool_limit: 10
  broker_connection_timeout: 4.0
  broker_visibility_timeout: 3600
  broker_transport_options: ''
  override_default_logging: true
  result_backend: file://~/.secator/celery/results
  result_backend_transport_options: ''
  result_expires: 86400
  task_acks_late: false
  task_send_sent_event: false
  task_reject_on_worker_lost: false
  task_max_timeout: -1
  task_memory_limit_mb: -1
  worker_max_tasks_per_child: 20
  worker_prefetch_multiplier: 1
  worker_send_task_events: false
  worker_kill_after_task: false
  worker_kill_after_idle_seconds: -1
  worker_command_verbose: false

cli:
  github_token: ''
  record: false
  stdin_timeout: 1000
  show_http_response_headers: false
  show_command_output: false
  exclude_http_response_headers:
    - connection
    - content_type
    - content_length
    - date
    - server

runners:
  input_chunk_size: 100
  progress_update_frequency: 20
  stat_update_frequency: 20
  backend_update_frequency: 5
  poll_frequency: 5
  skip_cve_search: false
  skip_exploit_search: false
  skip_cve_low_confidence: false
  remove_duplicates: false
  threads: 50
  prompt_timeout: 20

http:
  socks5_proxy: socks5://127.0.0.1:9050
  http_proxy: https://127.0.0.1:9080
  store_responses: true
  response_max_size_bytes: 100000
  proxychains_command: proxychains
  freeproxy_timeout: 1
  default_header: User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36

tasks:
  exporters:
  - json
  - csv
  - txt

workflows:
  exporters:
  - json
  - csv
  - txt

scans:
  exporters:
  - json
  - csv
  - txt

payloads:
  templates:
    lse: https://github.com/diego-treitos/linux-smart-enumeration/releases/latest/download/lse.sh
    linpeas: https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh
    sudo_killer: https://github.com/TH3xACE/SUDO_KILLER/archive/refs/heads/V3.zip

wordlists:
  defaults:
    http: bo0m_fuzz
    dns: combined_subdomains
    http_params: burp-parameter-names
  templates:
    bo0m_fuzz: https://raw.githubusercontent.com/Bo0oM/fuzz.txt/master/fuzz.txt
    combined_subdomains: https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/combined_subdomains.txt
    directory_list_small: https://gist.githubusercontent.com/sl4v/c087e36164e74233514b/raw/c51a811c70bbdd87f4725521420cc30e7232b36d/directory-list-2.3-small.txt
    burp-parameter-names: https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/Web-Content/burp-parameter-names.txt
  lists: {}

addons:
  gdrive:
    enabled: false
    drive_parent_folder_id: ''
    credentials_path: ''
  gcs:
    enabled: false
    bucket_name: ''
    credentials_path: ''
  worker:
    enabled: false
  mongodb:
    enabled: false
    url: mongodb://localhost
    update_frequency: 60
    max_pool_size: 10
    server_selection_timeout_ms: 5000
    max_items: null
    duplicate_main_copy_fields:
      - screenshot_path
      - stored_response_path
      - is_false_positive
      - is_acknowledged
      - verified
  vulners:
    enabled: false
    api_key: ''

profiles:
  defaults: []

drivers:
  defaults: []

providers:
  defaults:
    cve: circl
    exploit: exploitdb
    ghsa: ghsa

security:
  allow_local_file_access: true
  auto_install_commands: true
  force_source_install: false

offline_mode: false
```

To get `secator`'s default configuration, run:

```bash
secator config default
```

***

## Custom configuration

It is possible to override `secator`'s default configuration using a **user configuration file** located at `~/.secator/config.yml` .

The default user configuration is empty.

### Get config

To get `secator`'s user config, run:

```bash
secator config get
```

### Edit config

#### Editing whole config

To modify `secator`'s user config, run:

```bash
secator config edit
```

This will open the YAML config in your default editor (using the`$EDITOR` env variable).

Upon saving your changes, the config will be validated by `pydantic` and saved to disk if it's valid.&#x20;

{% hint style="warning" %}
If validation errors occur (for instance a wrong key, or wrong value type), you will get an error message such as:

```bash
❌ 1 validation error for SecatorConfig
  offline_test
    Extra inputs are not permitted 
      For further information visit https://errors.pydantic.dev/2.7/v/extra_forbidden
Hint: Run "secator config edit --resume" to edit your patch and fix issues.
```

The invalid patch will not be saved in the user config. This ensures the actual user config is always valid. Run `secator config edit --resume` to resume the edit to fix the issues, or skip the `--resume` flag to start over.
{% endhint %}

#### Editing specific config keys

To edit specific keys, use:

```bash
secator config set <path.to.config.key> <VALUE>
```

For instance, to set the debug component to `celery`:

```bash
secator config set debug.component celery
```

... or to set the `mongodb` addon URL:

```bash
secator config set addons.mongodb.url mongodb://mymongodbhost
```

### Env overrides

Values  in the `secator` config can be overriden using environment variables. Environment variables are prefixed with `SECATOR_`and use dotted path notation.

For instance, to override `debug.component`, run:

```bash
export SECATOR_DEBUG_COMPONENT=celery
```

To override the default HTTP wordlist:

```bash
export SECATOR_WORDLISTS_DEFAULTS_HTTP=/path/to/wordlist.txt
```

and so on.

***

