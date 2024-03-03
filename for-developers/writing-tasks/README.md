# Writing tasks

If you wish to integrate a new command with `secator`, you can define a new class inherited from `secator.runners.Command`.

***

## Basic command integration

To write an integration for the command `mytask`, add a task definition Python file named `mytask.py` in the `secator/tasks` folder.

Here is a basic integration of `mytask`:

{% code title="secator/tasks/mytask.py" %}
```python
from secator.runners import Command
from secator.decorators import task

@task
class mytask(Command):
    cmd = 'mytask'
    json_flag = '-json'  # or whatever the flag for JSON lines is
    input_flag = '-site' # or whatever the flag to take a single input is
    file_flag = '-list'  # or whatever the flag to take a file input is
```
{% endcode %}

***

## Mapping input options

The next step is to map the command input options that are mutual to other tasks of the same category:

```python
...
from secator.definitions import RATE_LIMIT, DELAY

@task
class mytask(Command):
    ...
    opt_key_map = {
        RATE_LIMIT: 'rate_limit', # or whatever the rate limit option is
        DELAY: 'delay'            # or whatever the delay option is
    }
```

Sometimes the options values have to be modified to comply with the mutualized option format. For instance, the `rate_limit` option of `mytask` could be the number of requests / minutes (instead of requests / second):

```python
@task
class mytask(Command):
    ...
    opt_value_map = {
        RATE_LIMIT: lambda x: x * 60 # convert the rate limit to seconds
    }
```

***

## Mapping output types

The next step is to map the output format of the command you integrate with standard `secator` [output-types.md](../../in-depth/concepts/output-types.md "mention").

\
If our task is outputting URLs in the format `{'url': 'http://mydomain.com', 'code': 200, 'length': 100}`, then we will need to convert this dict to the `Url` output type format:

```python
...
from secator.definitions import RATE_LIMIT, DELAY, URL, STATUS_CODE, CONTENT_LENGTH
from secator.output_types import Url

@task
class mytask(Command):
    ...
    output_types = [Url]
    output_map = {
        Url: {
            URL: 'url'
            STATUS_CODE: 'code',
            CONTENT_LENGTH: 'length',
        }
    }
```

A task can also have multiple output types, in which case we will define a mapping for each output type specified in the `output_types` key.

***

## Adding unit tests \[WIP]

***

## Adding integration tests \[WIP]

***
