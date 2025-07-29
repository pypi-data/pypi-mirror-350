import requests
from typing import Optional, Any, Dict


class TickrClient:
    def __init__(self, base_url: str = "https://tickr.cc", jwt: Optional[str] = None):
        """
        Create a TickrClient instance.
        :param base_url: Base URL for the Tickr API (default: https://tickr.cc)
        :param jwt: Supabase JWT for authenticated endpoints (optional)
        """
        self.base_url = base_url.rstrip("/")
        self.jwt = jwt

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.jwt:
            headers["Authorization"] = f"Bearer {self.jwt}"
        return headers

    def get_counters(self) -> Any:
        """Fetch all counters for the authenticated user. Example: client = TickrClient(); client.get_counters()"""
        url = f"{self.base_url}/api/counters"
        resp = requests.get(url, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def create_counter(self, name: str, initial_value: int = 0) -> Any:
        """Create a new counter (authenticated). Example: client = TickrClient(); client.create_counter(name="My Counter")"""
        url = f"{self.base_url}/api/counters"
        data = {"name": name, "initial_value": initial_value}
        resp = requests.post(url, json=data, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def get_counter(self, slug: str) -> Any:
        """Fetch a public counter by slug. Example: client = TickrClient(); client.get_counter(slug="abc123xyz")"""
        url = f"{self.base_url}/api/counters/{slug}"
        resp = requests.get(url, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def increment_counter(self, slug: str, increment_by: int = 1) -> Any:
        """Increment a counter by a given value (public or private). Example: client = TickrClient(); client.increment_counter(slug="abc123xyz", increment_by=2)"""
        url = f"{self.base_url}/api/counters/{slug}/increment"
        data = {"increment_by": increment_by}
        resp = requests.post(url, json=data, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def update_counter(self, slug: str, name: Optional[str] = None, current_value: Optional[int] = None) -> Any:
        """Update a counter's name or value (authenticated, owner only). Example: client = TickrClient(); client.update_counter(slug="abc123xyz", name="Renamed")"""
        url = f"{self.base_url}/api/counters/{slug}"
        data = {}
        if name is not None:
            data["name"] = name
        if current_value is not None:
            data["current_value"] = current_value
        if not data:
            raise ValueError("At least one of 'name' or 'current_value' must be provided.")
        resp = requests.put(url, json=data, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def delete_counter(self, slug: str) -> None:
        """Delete a counter (authenticated, owner only). Example: client = TickrClient(); client.delete_counter(slug="abc123xyz")"""
        url = f"{self.base_url}/api/counters/{slug}"
        resp = requests.delete(url, headers=self._headers())
        resp.raise_for_status()
