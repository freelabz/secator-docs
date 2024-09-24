---
description: ... or how to route live results to a destination.
---

# Drivers

A driver is a set of hooks that constitute a full integration to route live results to certain destination.

Unlike hooks, you can use a driver from the CLI by using the `-driver` option.

***

## MongoDB driver

To export live results to MongoDB database:

<pre class="language-bash"><code class="lang-bash"><strong>secator install addons mongodb
</strong>secator config set addons.mongodb.url mongodb://localhost
secator w host_recon example.com -driver mongodb
</code></pre>

Results will be added to the database in real-time as results come through from the various tools supported by `secator`.&#x20;

A MongoDB collection is created for each [output-types.md](output-types.md "mention") supported by `secator`.

***
