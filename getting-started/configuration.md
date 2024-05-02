---
description: ... how to configure every aspect of how secator operates.
---

# Configuration

## Default configuration

`secator` is configured using a YAML config file.

The default configuration is as follow:

```yaml
dirs:
  bin: ~/.local/bin
  data: ~/.secator
  templates: ~/.secator/templates
  reports: ~/.secator/reports
  wordlists: ~/.secator/wordlists
  cves: ~/.secator/cves
  payloads: ~/.secator/payloads
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
  override_default_logging: true
  result_backend: file://~/.secator/celery/results

cli:
  github_token: ''
  record: false
  stdin_timeout: 1000

runners:
  input_chunk_size: 1000
  progress_update_frequency: 60
  skip_cve_search: false
  skip_cve_low_confidence: true

http:
  socks5_proxy: socks5://127.0.0.1:9050
  http_proxy: https://127.0.0.1:9080
  store_responses: false
  proxychains_command: proxychains
  freeproxy_timeout: 1

tasks:
  exporters:
  - json
  - csv

workflows:
  exporters:
  - json
  - csv

scans:
  exporters:
  - json
  - csv

payloads:
  templates:
    lse: https://github.com/diego-treitos/linux-smart-enumeration/releases/latest/download/lse.sh
    linpeas: https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh
    sudo_killer: https://github.com/TH3xACE/SUDO_KILLER/archive/refs/heads/V3.zip

wordlists:
  defaults:
    http: https://raw.githubusercontent.com/Bo0oM/fuzz.txt/master/fuzz.txt
    dns: https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/combined_subdomains.txt
  templates:
    bo0m_fuzz: https://raw.githubusercontent.com/Bo0oM/fuzz.txt/master/fuzz.txt
    combined_subdomains: https://raw.githubusercontent.com/danielmiessler/SecLists/master/Discovery/DNS/combined_subdomains.txt
  lists: {}

addons:
  google:
    enabled: false
    drive_parent_folder_id: ''
    credentials_path: ''
  worker:
    enabled: false
  mongodb:
    enabled: false
    url: mongodb://localhost
    update_frequency: 60

offline_mode: false
```

To get `secator`'s default configuration, run:

```bash
secator config default
```

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

For instance, to set the debug level to 3:

```bash
secator config set debug.level 3
```

### Env overrides

Values  in the `secator` config can be overriden using environment variables. Environment variables are prefixed with `SECATOR_`and use dotted path notation.

For instance, to override `debug.level`, run:

```bash
export SECATOR_DEBUG_LEVEL=2
```

To override the default HTTP wordlist:

```bash
export SECATOR_WORDLISTS_DEFAULT_HTTP=/path/to/wordlist.txt
```

and so on.
