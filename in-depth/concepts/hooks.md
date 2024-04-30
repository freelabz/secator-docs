---
description: ... or how to run function on runner lifecycle events.
---

# Hooks

Hooks are methods that be plugged into any runner (`Task`, `Workflow`, `Scan`) lifecycle events:

* `on_init`: executed when the runner initializes.
* `on_start` : executed when the runner has started running.
* `on_iter`: executed when the runner iterates.
* `on_item`: executed when the runner emits an item.
* `on_end` : executed when the runner has finished running.

### Using hooks to save results in db

{% hint style="info" %}
Hooks are currently only useable when using `secator` as a library.
{% endhint %}

You can use hooks to save results in a database. We give a default out-of-the-box hooks for MongoDB that you can use when using `secator` as a library.

A simple example to save task results in MongoDB would be:

```python
from secator.runners import Workflow, Task
from secator.config import TemplateLoader
from secator.hooks import mongodb

config = TemplateLoader(path='/path/to/my/workflow.yaml')
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
from secator.template import TemplateLoader
from secator.hooks.mongodb import update_runner, update_finding

config = TemplateLoader(path='/path/to/my/workflow.yaml')
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
