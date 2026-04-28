# Table of contents

## GETTING STARTED

* [Introduction](README.md)
* [Installation](getting-started/installation.md)
* [CLI Usage](getting-started/cli-usage.md)
* [Library usage](getting-started/library-usage.md)
* [Configuration](getting-started/configuration.md)
* [Examples](getting-started/examples/README.md)
  * [5 minutes secator session](getting-started/examples/5-minutes-secator-session.md)

## RUNNER OPTIONS

* [Global options](runner-options/task-options.md)
* [Meta options](runner-options/meta-options.md)
* [Input formats](runner-options/input-formats.md)
* [Output options](runner-options/output-options.md)

## IN-DEPTH

* [Philosophy & design](in-depth/philosophy-and-design.md)
* [Distributed runs with Celery](in-depth/distributed-runs-with-celery.md)
* [Concepts](in-depth/concepts/README.md)
  * [Output types](in-depth/concepts/output-types.md)
  * [Proxies](in-depth/concepts/proxies.md)
  * [Exporters](in-depth/concepts/exporters.md)
  * [Runners](in-depth/concepts/runners.md)
  * [Drivers](in-depth/concepts/drivers.md)
  * [Profiles](in-depth/concepts/profiles.md)
* [Deployment](in-depth/deployment.md)

## UI guide

* [Overview](ui/README.md)
* Quickstart
  * [First run in 5 minutes](ui/quickstart.md)
  * [Sign in & first login](ui/sign-in.md)
  * [Global interface](ui/global-interface.md)
  * [Dashboard](ui/dashboard.md)
  * [Workspaces](ui/workspaces.md)
  * [Targets](ui/targets.md)
  * [Runners](ui/runners.md)
  * [Findings](ui/findings.md)
  * [Reports](ui/reports.md)
* Attacks
  * [Attack capabilities](ui/attack-capabilities.md)
  * [Available scans](ui/available-scans.md)
  * [Available workflows](ui/available-workflows.md)
  * [Meta options](ui/meta-options.md)
  * [Attack patterns](ui/attack-patterns.md)
* Concepts
  * [Platform overview](ui/platform-overview.md)
  * [Glossary](ui/glossary.md)
* Power features
  * [AI suggestions](ui/ai-suggestions.md)
  * [Chores & owner features](ui/chores.md)
* Account & API
  * [Profile, organization, billing](ui/profile-billing.md)
  * [API tokens](ui/api-tokens.md)
* [Quick reference](ui/quick-reference.md)

## For developers

* [Development setup](for-developers/development-setup.md)
* [Writing tasks](for-developers/writing-tasks/README.md)
  * [Integrating an external command](for-developers/writing-tasks/integrating-an-external-command/README.md)
    * [Parsing JSON lines](for-developers/writing-tasks/integrating-an-external-command/parsing-json-lines.md)
    * [Parsing raw standard output](for-developers/writing-tasks/integrating-an-external-command/parsing-raw-standard-output.md)
    * [Parsing output files](for-developers/writing-tasks/integrating-an-external-command/parsing-output-files.md)
    * [Example: integrating ls](for-developers/writing-tasks/integrating-an-external-command/example-integrating-ls.md)
    * [Example: cat hunters](for-developers/writing-tasks/integrating-an-external-command/example-cat-hunters.md)
  * [Integrate custom Python code \[WIP\]](for-developers/writing-tasks/integrate-custom-python-code-wip.md)
  * [Advanced options](for-developers/writing-tasks/advanced-options.md)
* [Writing workflows](for-developers/writing-workflows.md)
* [Writing scans \[WIP\]](for-developers/writing-scans-wip.md)
