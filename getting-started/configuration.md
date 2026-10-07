---
description: ... how to configure every aspect of how secator operates.
---

# Configuration

***

## Default configuration

`secator` is configured using a YAML config file. Every option has a default value, so the config file only needs the keys you want to change.

To print the full default configuration of your installed version, run:

```bash
secator config default
```

{% hint style="info" %}
Every key, its type, its default value and its environment variable are listed in the [configuration-reference.md](configuration-reference.md "mention").
{% endhint %}

***

## Custom configuration

It is possible to override `secator`'s default configuration using a **user configuration file** located at `~/.secator/config.yml` .

The default user configuration is empty.

{% hint style="info" %}
The config file lives in the data folder (`~/.secator` by default). To use another data folder, and therefore another config file, set the `SECATOR_DIRS_DATA` environment variable.
{% endhint %}

### Get config

```bash
secator config get                         # get full config (with defaults)
secator config get --user                  # get user config (non-default values only)
secator config get wordlists.defaults.http # get a single key
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

For instance, to print debug messages for the `celery` component:

```bash
secator config set debug celery
```

... or to set the `mongodb` addon URL:

```bash
secator config set addons.mongodb.url mongodb://mymongodbhost
```

List fields can be replaced, appended to, or have a single item removed:

```bash
secator config set drivers.defaults mongodb           # replace the list
secator config set drivers.defaults json --append     # append to the list
secator config unset drivers.defaults json            # remove one item from the list
```

Dict fields accept sub-keys:

```bash
secator config set wordlists.defaults.http mylist                # set a dict sub-key
secator config set workspaces.profiles.my_ws aggressive,passive  # set the default profiles of a workspace
secator config unset wordlists.defaults.http                     # remove a dict sub-key
```

#### Resetting config keys

To reset a key to its default value, use `secator config unset`:

```bash
secator config unset debug
```

### Env overrides

Values in the `secator` config can be overriden using environment variables. Environment variables are prefixed with `SECATOR_`, upper-cased, and use the dotted path of the key with dots replaced by underscores.

For instance, to override `debug`, run:

```bash
export SECATOR_DEBUG=celery
```

To override the default HTTP wordlist (`wordlists.defaults.http`):

```bash
export SECATOR_WORDLISTS_DEFAULTS_HTTP=/path/to/wordlist.txt
```

To use Redis as a Celery broker (`celery.broker_url`):

```bash
export SECATOR_CELERY_BROKER_URL=redis://localhost:6379/0
```

and so on. Environment variables take precedence over the config file. Unknown keys are ignored with a warning.

***

## Task overrides

`tasks.overrides` changes attributes of a specific task without touching its code. Keys are task names, values are the task attributes to override. Common attributes are:

| Attribute          | Description                                                                                                               |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------- |
| `max_timeout`      | Max execution time of the task in seconds (overrides `celery.task_max_timeout` for this task).                            |
| `input_chunk_size` | Number of inputs per chunk when the task runs on workers (`-1` disables chunking).                                        |
| `profile`          | Worker queue the task is sent to (`small`, `medium`, `large`, `extra_large`), see [distributed-runs-with-celery.md](../in-depth/distributed-runs-with-celery.md "mention"). |

{% tabs %}
{% tab title="CLI" %}
```bash
secator config set tasks.overrides.nmap.max_timeout 3600
secator config set tasks.overrides.search_vulns.profile large
```
{% endtab %}

{% tab title="YAML" %}
```yaml
tasks:
  overrides:
    nmap:
      max_timeout: 3600
    search_vulns:
      profile: large
```
{% endtab %}

{% tab title="Env vars" %}
Use `SECATOR_TASKS_OVERRIDES_<TASK>_<ATTRIBUTE>`. Task names containing underscores are supported:

```bash
export SECATOR_TASKS_OVERRIDES_NMAP_MAX_TIMEOUT=3600
export SECATOR_TASKS_OVERRIDES_SEARCH_VULNS_PROFILE=large
```
{% endtab %}
{% endtabs %}

{% hint style="info" %}
A `profile` override only applies to tasks with a static queue. Tasks that pick their queue dynamically (for instance `katana` in headless mode) keep their own routing.
{% endhint %}

***

## Debugging

The `debug` key prints internal debug messages for selected components. It accepts a comma-separated list of component names (prefix match), regexes, or `all`:

```bash
secator config set debug all            # everything
secator x httpx example.com             # ... run something
SECATOR_DEBUG=celery,hooks secator w host_recon example.com  # only for one run
SECATOR_DEBUG='cve.*' secator x nmap example.com             # regex
```

***
