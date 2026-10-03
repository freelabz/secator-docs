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

## GCS driver

To upload files (screenshots and stored responses) from URL results to Google Cloud Storage:

<pre class="language-bash"><code class="lang-bash"><strong>secator install addons gcs
</strong>secator config set addons.gcs.bucket_name my-bucket-name
secator w host_recon example.com -driver gcs
</code></pre>

Files will be uploaded to Google Cloud Storage in real-time as results come through. The local file paths (`screenshot_path`, `stored_response_path`) in URL results will be replaced with GCS URLs (`gs://bucket-name/blob-name`).

{% hint style="info" %}
**Authentication**: The GCS driver uses the Google Cloud Storage client library which automatically detects credentials. You can authenticate using one of the following methods:

- Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to your credentials JSON file
- Use Application Default Credentials if running on Google Cloud Platform
- The client library will automatically detect credentials from your environment

The `addons.gcs.credentials_path` config option is available but optional, as the client library handles credential detection automatically.
{% endhint %}

***

## API driver

To send live runners and findings to a remote HTTP API — in particular to get
an externally-run scan to show up on the Secator platform (Secator Cloud or a
self-hosted deployment):

```bash
secator config set addons.api.url https://app.secator.cloud/api
secator config set addons.api.key <API_TOKEN>
secator w host_recon example.com -driver api -ws my-workspace
```

See [Running internal scans and getting results on the platform](../running-internal-scans-on-the-platform.md) for the full walkthrough, including the network/proxy requirement and how to route specific scans to dedicated workers.

***
