---
description: Instructions to develop on secator.
---

# Development setup

## Install a development build

To install `secator` in development mode, first make sure `pip` and `virtualenv` are installed, and run the following steps:

```
git clone https://github.com/freelabz/secator  # clone the repository
cd secator                                     # go to the repository folder
virtualenv .venv                               # create a virtualenv
source .venv/bin/activate                      # load the virtualenv
pip install -e .[dev]                          # install secator and dev dependencies
```

You can now run `secator health` to verify your installation. You can install addons / tools using the `secator install` command (choose what to install based on what you want to dev on).
