# Tickr Python Client

A Python client library for interacting with the Tickr API (counters service).

## Features
- Fetch all your counters (requires authentication)
- Create a new counter (requires authentication)
- Fetch a public counter by slug
- Increment a counter (public or private, depending on API config)
- Update a counter (requires authentication and ownership)
- Delete a counter (requires authentication and ownership)

## Installation

```bash
pip install -e .
```

## Usage

```python
from tickr_client import TickrClient

# Create a client instance (JWT is optional, for authenticated endpoints)
# You can get your API JWT from the Tickr API docs page: https://tickr.cc/api-docs
client = TickrClient(jwt="YOUR_API_JWT")

# Fetch all counters (authenticated)
counters = client.get_counters()

# Create a new counter (authenticated)
new_counter = client.create_counter(name="My Counter", initial_value=10)

# Fetch a public counter by slug
public_counter = client.get_counter(slug="abc123xyz")

# Increment a counter (public or private)
updated_counter = client.increment_counter(slug="abc123xyz", increment_by=2)

# Update a counter (authenticated, owner only)
updated = client.update_counter(slug="abc123xyz", name="Renamed", current_value=42)

# Delete a counter (authenticated, owner only)
client.delete_counter(slug="abc123xyz")
```

## Authentication
For authenticated endpoints, obtain a API JWT and pass it to the client. Public endpoints do not require authentication.

## License
MIT
