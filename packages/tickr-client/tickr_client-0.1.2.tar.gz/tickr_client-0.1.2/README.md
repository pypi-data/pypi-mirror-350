# Tickr Python Client

<p align="center">
  <img width="64" height="64" src="https://tickr.cc/favicon.svg" alt="Tickr favicon" />
</p>

<p align="center">
  <b>Simple, Shareable, Powerful Counters for Anything.</b>
</p>

<p align="center">
  <img alt="PyPI" src="https://img.shields.io/pypi/v/tickr-client?color=4f46e5&label=PyPI&logo=python&logoColor=white">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-8b5cf6">
  <img alt="API Key Auth" src="https://img.shields.io/badge/Auth-API%20Key%20Only-purple?logo=keybase&logoColor=white">
  <img alt="Private Counters" src="https://img.shields.io/badge/Private%20Counters-Supported-4f46e5">
  <img alt="Read Only" src="https://img.shields.io/badge/Read%20Only%20Counters-Supported-8b5cf6">
  <img alt="Made with Love" src="https://img.shields.io/badge/Made%20with-%E2%9D%A4-purple">
</p>

A Python client library for interacting with the Tickr API (counters service).

---

## Features
- Fetch all your counters (requires authentication)
- Create a new counter (requires authentication)
- Fetch a public counter by slug
- Increment a counter (public or private, depending on API config)
- Update a counter (requires authentication and ownership)
- Delete a counter (requires authentication and ownership)
- Supports API key authentication (recommended; JWT is deprecated)
- Supports `is_private` and `is_readonly` counter properties

## Installation

```bash
pip install -e .
```

## Usage

```python
from tickr_client import TickrClient

# Create a client instance (API key is recommended for authenticated endpoints)
# You can get your API key from the Tickr API docs page: https://tickr.cc/api-docs
client = TickrClient(api_key="YOUR_API_KEY")

# Fetch all counters (authenticated)
counters = client.get_counters()

# Create a new counter (authenticated, with privacy/read-only options)
new_counter = client.create_counter(name="My Counter", initial_value=10, is_private=True, is_readonly=False)

# Fetch a public counter by slug
public_counter = client.get_counter(slug="abc123xyz")

# Increment a counter (public or private)
updated_counter = client.increment_counter(slug="abc123xyz", increment_by=2)

# Update a counter (authenticated, owner only)
updated = client.update_counter(slug="abc123xyz", name="Renamed", current_value=42, is_private=False)

# Delete a counter (authenticated, owner only)
client.delete_counter(slug="abc123xyz")
```

## Authentication
For authenticated endpoints, obtain an API key from your Tickr dashboard and pass it to the client as `api_key`. Public endpoints do not require authentication.

> **Note:** JWT authentication is deprecated. Use API keys for all new integrations.

## Counter Properties
- `is_private`: If `True`, only authorized users can increment the counter.
- `is_readonly`: If `True`, the counter cannot be incremented by anyone.

These properties are always included in returned counter objects.

## License
MIT
