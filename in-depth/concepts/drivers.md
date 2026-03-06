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

The API driver sends runner and finding data to an external REST API in real-time. This is useful for integrating `secator` with external platforms, dashboards, or security orchestration tools.

### Setup

```bash
# Configure the API endpoint
secator config set addons.api.url https://your-api.example.com
secator config set addons.api.key your-api-key

# Run with the API driver
secator w host_recon example.com -driver api -ws my-workspace-id
```

{% hint style="warning" %}
The API driver requires a valid workspace ID (not `default`). Use `-ws <workspace_id>` to specify one.
{% endhint %}

### Configuration Options

| Config Key | Default | Description |
|------------|---------|-------------|
| `addons.api.enabled` | `false` | Enable/disable the API driver |
| `addons.api.url` | `''` | Base URL of the external API |
| `addons.api.key` | `''` | API key for authentication |
| `addons.api.header_name` | `Bearer` | Authorization header prefix |
| `addons.api.force_ssl` | `true` | Enable SSL certificate verification |
| `addons.api.timeout` | `30` | Request timeout in seconds |
| `addons.api.runner_create_endpoint` | `/runners` | Endpoint for creating runners |
| `addons.api.runner_update_endpoint` | `/runners/{runner_id}` | Endpoint for updating runners |
| `addons.api.finding_create_endpoint` | `/findings` | Endpoint for creating findings |
| `addons.api.finding_update_endpoint` | `/findings/{finding_id}` | Endpoint for updating findings |
| `addons.api.workspace_get_endpoint` | `/workspaces/{workspace_id}` | Endpoint for getting workspace info |

### API Endpoints

The API driver expects your external API to implement the following endpoints:

#### Runner Endpoints

**POST** `{runner_create_endpoint}` - Create a new runner
- Request body: Runner data (JSON)
- Response: `{ "id": "<runner_id>" }`

**PUT** `{runner_update_endpoint}` - Update an existing runner
- URL parameter: `{runner_id}`
- Request body: Runner update data (JSON)

#### Finding Endpoints

**POST** `{finding_create_endpoint}` - Create a new finding
- Request body: Finding data (JSON)
- Response: `{ "id": "<finding_id>" }`

**PUT** `{finding_update_endpoint}` - Update an existing finding
- URL parameter: `{finding_id}`
- Request body: Finding update data (JSON)

#### Workspace Endpoint

**GET** `{workspace_get_endpoint}` - Get workspace information
- URL parameter: `{workspace_id}`
- Response: `{ "name": "<workspace_name>" }`

### Example Usage

{% tabs %}
{% tab title="CLI" %}
```bash
# Configure API settings
secator config set addons.api.url https://api.securityplatform.com
secator config set addons.api.key sk-your-api-key-here

# Run a workflow with API integration
secator w host_recon example.com -driver api -ws project-123

# Combine with other drivers
secator w host_recon example.com -driver mongodb,api -ws project-123
```
{% endtab %}

{% tab title="Library" %}
```python
from secator.workflows import host_recon

# Run with API driver
results = host_recon(
    'example.com',
    drivers=['api'],
    context={'workspace_id': 'project-123'}
).run()
```
{% endtab %}
{% endtabs %}

### Authentication

The API driver sends authentication headers with each request:

```
Authorization: {header_name} {api_key}
Content-Type: application/json
```

By default, this results in:
```
Authorization: Bearer your-api-key
```

You can customize the header prefix:
```bash
secator config set addons.api.header_name "X-API-Key"
# Results in: X-API-Key your-api-key
```

***
