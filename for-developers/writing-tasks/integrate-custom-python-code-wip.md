---
description: How to create custom tasks using pure Python code without external commands.
---

# Integrate custom Python code

The `PythonRunner` class allows you to create custom Secator tasks using pure Python code, without needing to integrate external command-line tools. This is useful when you want to:

- Process data using Python libraries
- Implement custom logic that doesn't require external commands
- Create lightweight tasks that perform transformations or analysis
- Build tasks that interact with APIs or databases

***

## Overview

To create a custom Python task, you need to:

1. Create a Python file in `~/.secator/templates/` (for user tasks) or `secator/tasks/` (for development)
2. Inherit from the `PythonRunner` class
3. Decorate your class with the `@task()` decorator
4. Define `input_types` and `output_types`
5. Implement the `yielder()` method to yield results

***

## Basic structure

Here's the minimal structure of a Python task:

{% code title="~/.secator/templates/mytask.py" %}
```python
from secator.decorators import task
from secator.definitions import HOST
from secator.output_types import Tag, Url
from secator.runners import PythonRunner


@task()
class mytask(PythonRunner):
    """Description of what this task does."""
    input_types = [HOST]
    output_types = [Tag, Url]

    def yielder(self):
        for target in self.inputs:
            yield Url(url=f"http://{target}")
            yield Tag(name="scanned", match=target)
```
{% endcode %}

**Important notes:**

- The class name must match the filename (without `.py`)
- The `@task()` decorator is required
- You must inherit from `PythonRunner`
- The `yielder()` method is where your task logic goes
- Use `yield` to return results as output types

***

## Available input types

You can specify which input types your task accepts using `input_types`. Available input types include:

- `HOST` - Hostnames or domains
- `URL` - URLs
- `IP` - IP addresses
- `CIDR_RANGE` - CIDR ranges
- `EMAIL` - Email addresses
- `PATH` - File paths
- `STRING` - Generic strings
- `None` - Accept any input type

Example:

```python
from secator.definitions import URL, IP, HOST

@task()
class mytask(PythonRunner):
    # Accept multiple input types
    input_types = [URL, IP, HOST]
    # ...
```

***

## Available output types

Your task can yield various output types. Common ones include:

- `Info` - Informational messages
- `Url` - URLs
- `Ip` - IP addresses
- `Port` - Network ports
- `Subdomain` - Subdomains
- `Vulnerability` - Security vulnerabilities
- `Tag` - Tags/metadata
- `Domain` - Domains
- `Record` - DNS records
- `Certificate` - SSL certificates
- `UserAccount` - User accounts
- `Warning` - Warning messages
- `Error` - Error messages

Example:

```python
from secator.output_types import Url, Vulnerability, Tag, Info

@task()
class mytask(PythonRunner):
    output_types = [Url, Vulnerability, Tag, Info]
    # ...
```

***

## Example: Simple URL processor

This example processes URLs and extracts information:

{% code title="~/.secator/templates/urlprocessor.py" %}
```python
from urllib.parse import urlparse

from secator.decorators import task
from secator.definitions import URL
from secator.output_types import Tag, Url
from secator.runners import PythonRunner


@task()
class urlprocessor(PythonRunner):
    """Extract components from URLs."""
    input_types = [URL]
    output_types = [Tag, Url]
    tags = ['url', 'parsing']

    def yielder(self):
        for url in self.inputs:
            parsed = urlparse(url)
            
            # Yield the original URL
            yield Url(url=url)
            
            # Yield tags with extracted information
            yield Tag(
                name='url_scheme',
                value=parsed.scheme,
                match=url,
                category='info'
            )
            yield Tag(
                name='url_domain',
                value=parsed.netloc,
                match=url,
                category='info'
            )
            yield Tag(
                name='url_path',
                value=parsed.path,
                match=url,
                category='info'
            )
```
{% endcode %}

Usage:

```bash
secator x urlprocessor https://example.com/path?query=1
```

***

## Example: Vulnerability scanner

This example demonstrates yielding vulnerabilities:

{% code title="~/.secator/templates/customscanner.py" %}
```python
import requests

from secator.decorators import task
from secator.definitions import URL
from secator.output_types import Vulnerability, Info, Warning
from secator.runners import PythonRunner


@task()
class customscanner(PythonRunner):
    """Custom vulnerability scanner."""
    input_types = [URL]
    output_types = [Vulnerability, Info, Warning]
    tags = ['vuln', 'web']

    def yielder(self):
        yield Info(message="Starting custom scan")
        
        for url in self.inputs:
            try:
                response = requests.get(url, timeout=5)
                
                # Check for security headers
                if 'X-Frame-Options' not in response.headers:
                    yield Vulnerability(
                        name="Missing X-Frame-Options header",
                        severity="medium",
                        confidence="high",
                        matched_at=url,
                        provider="customscanner"
                    )
                
                # Check for exposed server information
                if 'Server' in response.headers:
                    server = response.headers['Server']
                    yield Warning(
                        message=f"Server header exposed: {server}",
                        matched_at=url
                    )
                    
            except requests.RequestException as e:
                yield Warning(
                    message=f"Failed to scan {url}: {str(e)}",
                    matched_at=url
                )
        
        yield Info(message="Scan complete")
```
{% endcode %}

***

## Example: Task with custom options

You can define custom options that users can pass to your task:

{% code title="~/.secator/templates/tagger.py" %}
```python
from secator.decorators import task
from secator.definitions import HOST
from secator.output_types import Tag
from secator.runners import PythonRunner


@task()
class tagger(PythonRunner):
    """Tag hosts with custom metadata."""
    input_types = [HOST]
    output_types = [Tag]
    tags = ['tagging']
    
    opts = {
        'tag_name': {
            'type': str,
            'default': 'custom_tag',
            'help': 'Name of the tag to apply'
        },
        'tag_value': {
            'type': str,
            'default': 'scanned',
            'help': 'Value for the tag'
        },
        'category': {
            'type': str,
            'default': 'info',
            'help': 'Tag category'
        }
    }

    def yielder(self):
        tag_name = self.run_opts.get('tag_name', 'custom_tag')
        tag_value = self.run_opts.get('tag_value', 'scanned')
        category = self.run_opts.get('category', 'info')
        
        for host in self.inputs:
            yield Tag(
                name=tag_name,
                value=tag_value,
                match=host,
                category=category
            )
```
{% endcode %}

Usage:

```bash
secator x tagger example.com --tag-name "environment" --tag-value "production"
```

***

## Example: Task without inputs

Some tasks don't require inputs. Use `default_inputs` to make inputs optional:

{% code title="~/.secator/templates/netdetect.py" %}
```python
import ifaddr
import ipaddress

from secator.decorators import task
from secator.output_types import Tag, Ip
from secator.runners import PythonRunner


@task()
class netdetect(PythonRunner):
    """Detect local network CIDR ranges."""
    output_types = [Tag, Ip]
    tags = ['network', 'recon']
    default_inputs = ''  # No inputs required
    input_flag = None

    def yielder(self):
        adapters = ifaddr.get_adapters()
        for adapter in adapters:
            if adapter.name == 'lo' or adapter.name.lower().startswith('loopback'):
                continue
                
            yield Tag(
                name='net_interface',
                match='localhost',
                value=adapter.nice_name,
                category='info',
            )
            
            for ip in adapter.ips:
                if ip.is_IPv4:
                    try:
                        network = ipaddress.IPv4Network(
                            f"{ip.ip}/{ip.network_prefix}",
                            strict=False
                        )
                        yield Ip(
                            ip=ip.ip,
                            host='localhost',
                            alive=True,
                        )
                        yield Tag(
                            name='net_cidr',
                            match='localhost',
                            value=str(network),
                            category='info',
                        )
                    except ValueError:
                        continue
```
{% endcode %}

Usage:

```bash
secator x netdetect
```

***

## Accessing runner properties

In your `yielder()` method, you have access to several useful properties:

- `self.inputs` - List of input values
- `self.run_opts` - Dictionary of run options (including custom `opts`)
- `self.name` - Task name
- `self.config` - Task configuration
- `self.context` - Runner context

Example:

```python
def yielder(self):
    yield Info(message=f"Task name: {self.name}")
    yield Info(message=f"Processing {len(self.inputs)} inputs")
    
    # Access custom options
    timeout = self.run_opts.get('timeout', 10)
    
    for input in self.inputs:
        # Process each input
        pass
```

***

## Advanced: Multiple output types

You can yield different output types based on your logic:

{% code title="~/.secator/templates/multiplexer.py" %}
```python
from secator.decorators import task
from secator.definitions import HOST
from secator.output_types import Url, Vulnerability, Tag, Info
from secator.runners import PythonRunner


@task()
class multiplexer(PythonRunner):
    """Process hosts and yield different output types."""
    input_types = [HOST]
    output_types = [Url, Vulnerability, Tag, Info]

    def yielder(self):
        yield Info(message="Starting multiplex scan")
        
        for host in self.inputs:
            # Always yield a URL
            yield Url(url=f"https://{host}")
            
            # Conditionally yield vulnerabilities
            if "test" in host.lower():
                yield Vulnerability(
                    name="Test environment detected",
                    severity="low",
                    confidence="high",
                    matched_at=host,
                    provider="multiplexer"
                )
            
            # Yield tags
            yield Tag(
                name="scanned_host",
                value=host,
                match=host,
                category="info"
            )
        
        yield Info(message="Scan complete")
```
{% endcode %}

***

## Task discovery

Secator automatically discovers tasks from:

- **User tasks**: `~/.secator/templates/*.py`
- **Development tasks**: `secator/tasks/*.py` (when developing Secator itself)

The task class name must match the filename (case-sensitive). For example:
- File: `~/.secator/templates/mytask.py` → Class: `mytask`
- File: `secator/tasks/urlparser.py` → Class: `urlparser`

After creating your task file, Secator will automatically discover it on the next run.

***

## Best practices

1. **Use descriptive class names**: Choose names that clearly indicate what the task does
2. **Add docstrings**: Document what your task does in the class docstring
3. **Set appropriate tags**: Use `tags` to categorize your task for better discoverability
4. **Handle errors gracefully**: Use `Warning` or `Error` output types for error conditions
5. **Yield progress information**: Use `Info` messages to provide feedback during long-running tasks
6. **Validate inputs**: Check input validity before processing
7. **Use appropriate output types**: Choose the most specific output type for your results

***

## Testing your task

You can test your task from the command line:

```bash
# Run the task
secator x mytask example.com

# Get help
secator x mytask --help

# Run with JSON output
secator x mytask example.com --json

# Run with custom options
secator x mytask example.com --option1 value1
```

Or use it programmatically:

```python
from secator.tasks import mytask

# Run the task
results = mytask('example.com').run()

# Access results
for result in results:
    print(f"{result._type}: {result}")
```

***

## Common patterns

### Pattern: Processing with external libraries

```python
import some_library

@task()
class mytask(PythonRunner):
    def yielder(self):
        for input in self.inputs:
            result = some_library.process(input)
            yield Tag(name="result", value=result, match=input)
```

### Pattern: API integration

```python
import requests

@task()
class apitask(PythonRunner):
    def yielder(self):
        for input in self.inputs:
            response = requests.get(f"https://api.example.com/{input}")
            data = response.json()
            yield Tag(name="api_data", value=str(data), match=input)
```

### Pattern: Data transformation

```python
@task()
class transform(PythonRunner):
    def yielder(self):
        for input in self.inputs:
            # Transform the input
            transformed = input.upper().replace("-", "_")
            yield Tag(name="transformed", value=transformed, match=input)
```

***

## Troubleshooting

### Task not discovered

- Ensure the filename matches the class name exactly
- Check that the file is in `~/.secator/templates/` or `secator/tasks/`
- Verify the `@task()` decorator is present
- Make sure the class inherits from `PythonRunner`

### Validation errors

- If you get "Input is empty" errors, set `default_inputs = ''` for tasks that don't need inputs
- For tasks that accept multiple inputs, ensure you're running with a worker (multiple inputs aren't supported in non-worker mode)

### Import errors

- Ensure all required Python packages are installed
- Check that imports are correct and available in your environment
