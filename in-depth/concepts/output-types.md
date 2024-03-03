# Output types

`secator` uses the notion of output types to uniformize tasks output. A task can output one or multiple output types.

The currently available output types are [#exploit](output-types.md#exploit "mention"), [#ip](output-types.md#ip "mention"), [#port](output-types.md#port "mention"), [#record](output-types.md#record "mention"),[#subdomain](output-types.md#subdomain "mention"), [#tag](output-types.md#tag "mention"), [#url](output-types.md#url "mention"), [#useraccount](output-types.md#useraccount "mention"), [#vulnerability](output-types.md#vulnerability "mention").

{% hint style="info" %}
Feel free to request more output types by opening an issue on the GitHub repo.
{% endhint %}

### ⍼ Exploit

<pre class="language-python"><code class="lang-python"><strong>@dataclass
</strong>class Exploit(OutputType):
    name: str
    id: str
    provider: str
    matched_at: str = ''
    ip: str = ''
    reference: str = ''
    cves: list = field(default_factory=list, compare=False)
    tags: list = field(default_factory=list, compare=False)
    extra_data: dict = field(default_factory=dict, compare=False)
</code></pre>

### 💻 Ip

{% code title="secator/output_types/ip.py" %}
```python
@dataclass
class Ip(OutputType):
    ip: str
    host: str = ''
    alive: bool = False
```
{% endcode %}

### 🔓 Port

{% code title="secator/output_types/port.py" %}
```python
@dataclass
class Port(OutputType):
    port: int
    ip: str
    state: str = 'UNKNOWN'
    service_name: str = field(default='', compare=False)
    cpes: list = field(default_factory=list, compare=False)
    host: str = field(default='', repr=True, compare=False)
    extra_data: dict = field(default_factory=dict, compare=False)
```
{% endcode %}

### 🎤 Record

{% code title="secator/output_types/record.py" %}
```python
@dataclass
class Record(OutputType):
    name: str
    type: str
    host: str = ''
    extra_data: dict = field(default_factory=dict, compare=False)
```
{% endcode %}

### 🏰 Subdomain

{% code title="secator/output_types/subdomain.py" %}
```python
@dataclass
class Subdomain(OutputType):
    host: str
    domain: str
    sources: List[str] = field(default_factory=list, compare=False)
```
{% endcode %}

### 🏷️ Tag

{% code title="secator/output_types/tag.py" %}
```python
@dataclass
class Tag(OutputType):
    name: str
    match: str
    extra_data: dict = field(default_factory=dict, repr=True, compare=False)
```
{% endcode %}

### 🔗 Url

{% code title="secator/output_types/url.py" %}
```python
@dataclass
class Url(OutputType):
    url: str
    host: str = field(default='', compare=False)
    status_code: int = field(default=0, compare=False)
    title: str = field(default='', compare=False)
    webserver: str = field(default='', compare=False)
    tech: list = field(default_factory=list, compare=False)
    content_type: str = field(default='', compare=False)
    content_length: int = field(default=0, compare=False)
    time: str = field(default='', compare=False)
    method: str = field(default='', compare=False)
    words: int = field(default=0, compare=False)
    lines: int = field(default=0, compare=False)
    screenshot_path: str = field(default='', compare=False)
    stored_response_path: str = field(default='', compare=False)
```
{% endcode %}

### 👤 UserAccount

{% code title="secator/output_types/user_account.py" %}
```python
@dataclass
class UserAccount(OutputType):
    username: str
    url: str = ''
    email: str = ''
    site_name: str = ''
    extra_data: dict = field(default_factory=dict, compare=False)
```
{% endcode %}

### 🚨 Vulnerability

{% code title="secator/output_types/vulnerability.py" %}
```python
@dataclass
class Vulnerability(OutputType):
    name: str
    provider: str = ''
    id: str = ''
    matched_at: str = ''
    ip: str = field(default='', compare=False)
    confidence: int = 'low'
    severity: str = 'unknown'
    cvss_score: float = 0
    tags: List[str] = field(default_factory=list)
    extra_data: dict = field(default_factory=dict, compare=False)
    description: str = field(default='', compare=False)
    references: List[str] = field(default_factory=list, compare=False)
    reference: str = field(default='', compare=False)
    confidence_nb: int = 0
    severity_nb: int = 0
```
{% endcode %}

