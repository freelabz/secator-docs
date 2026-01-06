---
description: ... or how secator unifies all output into common schemas.
---

# Output types

`secator` uses the notion of output types to uniformize tasks output. A task can output one or multiple output types.

The currently available output types are [#certificate](output-types.md#certificate "mention"), [#domain](output-types.md#domain "mention"), [#exploit](output-types.md#exploit "mention"), [#ip](output-types.md#ip "mention"), [#port](output-types.md#port "mention"), [#record](output-types.md#record "mention"), [#subdomain](output-types.md#subdomain "mention"), [#tag](output-types.md#tag "mention"), [#url](output-types.md#url "mention"), [#useraccount](output-types.md#useraccount "mention"), [#vulnerability](output-types.md#vulnerability "mention").

{% hint style="info" %}
Feel free to request more output types by [opening an issue](https://github.com/freelabz/secator/issues/new/choose) on the GitHub repo.
{% endhint %}

***

## 📜 Certificate

{% code title="secator/output_types/certificate.py" %}
```python
@dataclass
class Certificate(OutputType):
    host: str
    fingerprint_sha256: str = field(default='')
    ip: str = field(default='', compare=False)
    raw_value: str = field(default='', compare=False)
    subject_cn: str = field(default='', compare=False)
    subject_an: list[str] = field(default_factory=list, compare=False)
    not_before: datetime = field(default=None, compare=False)
    not_after: datetime = field(default=None, compare=False)
    issuer_dn: str = field(default='', compare=False)
    issuer_cn: str = field(default='', compare=False)
    issuer: str = field(default='', compare=False)
    self_signed: bool = field(default=True, compare=False)
    trusted: bool = field(default=False, compare=False)
    status: str = field(default=CERTIFICATE_STATUS_UNKNOWN, compare=False)
    keysize: int = field(default=None, compare=False)
    serial_number: str = field(default='', compare=False)
    ciphers: list[str] = field(default_factory=list, compare=False)
```
{% endcode %}

***

## 🪪 Domain

{% code title="secator/output_types/domain.py" %}
```python
@dataclass
class Domain(OutputType):
    domain: str
    registrar: str = ''
    alive: bool = False
    creation_date: str = ''
    expiration_date: str = ''
    registrant: str = ''
    extra_data: dict = field(default_factory=dict, compare=False)
```
{% endcode %}

***

## ⍼  Exploit

{% code title="secator/output_types/exploit.py" %}
```python
@dataclass
class Exploit(OutputType):
    name: str
    provider: str
    id: str
    matched_at: str = ''
    ip: str = ''
    confidence: str = 'low'
    reference: str = field(default='', repr=True, compare=False)
    cves: list = field(default_factory=list, compare=False)
    tags: list = field(default_factory=list, compare=False)
    extra_data: dict = field(default_factory=dict, compare=False)
```
{% endcode %}

***

## 💻 Ip

{% code title="secator/output_types/ip.py" %}
```python
@dataclass
class Ip(OutputType):
    ip: str
    host: str = field(default='', repr=True, compare=False)
    alive: bool = False
    protocol: str = field(default=IpProtocol.IPv4)
    extra_data: dict = field(default_factory=dict, compare=False)
```
{% endcode %}

***

## 🔓 Port

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
    protocol: str = field(default='tcp', repr=True, compare=False)
    extra_data: dict = field(default_factory=dict, compare=False)
    confidence: str = field(default='low', repr=False, compare=False)
```
{% endcode %}

***

## 🎤 Record

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

***

## 🏰 Subdomain

{% code title="secator/output_types/subdomain.py" %}
```python
@dataclass
class Subdomain(OutputType):
    host: str
    domain: str
    verified: bool = field(default=False, compare=False)
    sources: List[str] = field(default_factory=list, compare=False)
    extra_data: dict = field(default_factory=dict, compare=False)
```
{% endcode %}

***

## 🏷️ Tag

{% code title="secator/output_types/tag.py" %}
```python
@dataclass
class Tag(OutputType):
    name: str
    value: str
    match: str
    category: str = field(default='general')
    extra_data: dict = field(default_factory=dict, repr=True, compare=False)
    stored_response_path: str = field(default='', compare=False)
```
{% endcode %}

***

## 🔗 Url

{% code title="secator/output_types/url.py" %}
```python
@dataclass
class Url(OutputType):
    url: str
    host: str = field(default='', compare=False)
    verified: bool = field(default=False, compare=False)
    status_code: int = field(default=0, compare=False)
    title: str = field(default='', compare=False)
    protocol: str = field(default='', compare=False)
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
    confidence: str = field(default='high', compare=False)
    response_headers: dict = field(default_factory=dict, repr=True, compare=False)
    request_headers: dict = field(default_factory=dict, repr=True, compare=False)
    extra_data: dict = field(default_factory=dict, compare=False)
    is_directory: bool = field(default=False, compare=False)
    is_root: bool = field(default=False, compare=False)
    is_redirect: bool = field(default=False, compare=False)
```
{% endcode %}

***

## 👤 UserAccount

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

***

## 🚨 Vulnerability

{% code title="secator/output_types/vulnerability.py" %}
```python
@dataclass
class Vulnerability(OutputType):
    name: str
    provider: str = ''
    id: str = ''
    matched_at: str = ''
    ip: str = field(default='', compare=False)
    confidence: str = 'low'
    severity: str = 'unknown'
    cvss_score: float = 0
    cvss_vec: str = ''
    epss_score: float = 0
    tags: List[str] = field(default_factory=list, compare=False)
    extra_data: dict = field(default_factory=dict, compare=False)
    description: str = field(default='', compare=False)
    references: List[str] = field(default_factory=list, compare=False)
    reference: str = field(default='', compare=False)
    confidence_nb: int = 0
    severity_nb: int = 0
```
{% endcode %}

***
