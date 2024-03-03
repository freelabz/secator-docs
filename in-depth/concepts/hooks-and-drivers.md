# Hooks & Drivers

## Hooks

Hooks are methods that be plugged into any runner (`Task`, `Workflow`, `Scan`) lifecycle events:

* `on_init`: executed when the runner initializes.
* `on_start` : executed when the runner has started running.
* `on_iter`: executed when the runner emits a result.
* `on_end` : executed when the runner has finished running.

### Using hooks to save results in db

{% hint style="info" %}
Hooks are currently only useable when using `secator` as a library.
{% endhint %}

You can use hooks to save results in a database. We give a default out-of-the-box hooks for MongoDB that you can use when using `secator` as a library.

A simple example to save task results in MongoDB would be:

```python
from secator.runners import Workflow, Task
from secator.config import ConfigLoader
from secator.hooks import mongodb

config = ConfigLoader(path='/path/to/my/workflow.yaml')
workflow = Workflow(
    config,
    hooks={
        Task: {
            'on_item': [mongodb.save_finding],
        }
    })
workflow.run()
```

If you wish to also save runner information in the database, you can use the `on_init`, `on_start`, `on_iter` hooks as well. Behave using `on_iter` will considerably increase the number of db calls made. Here is a more advanced example:

```python
from secator.runners import Workflow, Task
from secator.config import ConfigLoader
from secator.hooks.mongodb import update_runner, update_finding

config = ConfigLoader(path='/path/to/my/workflow.yaml')
workflow = Workflow(
    config,
    hooks={
       Workflow: {
            'on_init': [update_runner],
            'on_start': [update_runner],
            'on_iter': [update_runner],
            'on_end': [update_runner]
        },
        Task: {
            'on_init': [update_runner],
            'on_item': [update_finding],
            'on_duplicate': [update_finding],
            'on_iter': [update_runner],
            'on_end': [update_runner]
        }
    })
workflow.run()
```

{% hint style="info" %}
Feel free to ask for more out-of-the-box db integrations by opening an issue on the GitHub repository.
{% endhint %}

## Drivers

A driver is a set of hooks that constitute an integration to route live results to certain destination.

You can use a driver from the CLI by using the `-driver` option.

Currently available drivers are:

* &#x20;`mongodb` - Export live results to a MongoDB database. Environment variables are used to configure the MongoDB details:
  * `MONGODB_URL` - Full URL (with credentials) of the MongoDB database, e.g: `mongodb://localhost`
  * &#x20;\[optional] `MONGODB_UPDATE_FREQUENCY`- Update frequency (in seconds).&#x20;

**Example:**

```bash
export MONGODB_URL=mongodb://localhost
secator w host_recon example.com -driver mongodb
```

Results will be added to the database in real-time as results come through from the various tools supported by `secator`.&#x20;

A collection is created for each [output-types.md](output-types.md "mention") supported by `secator`.
