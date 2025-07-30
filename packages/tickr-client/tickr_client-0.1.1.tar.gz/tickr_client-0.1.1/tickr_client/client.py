import requests
from typing import Optional, Any, Dict, List, TypedDict


class CounterDict(TypedDict, total=False):
    slug: str
    name: str
    current_value: int
    initial_value: int
    is_private: bool
    is_readonly: bool
    owner_id: str
    created_at: str
    updated_at: str
    # Add any other fields your API returns for counters here


class TickrClient:
    def __init__(self, base_url: str = "https://tickr.cc", api_key: Optional[str] = None):
        """
        Create a TickrClient instance.
        :param base_url: Base URL for the Tickr API (default: https://tickr.cc)
        :param api_key: Tickr API key for authenticated endpoints (optional)
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def create_counter(
        self, name: str, initial_value: int = 0, is_private: Optional[bool] = None, is_readonly: Optional[bool] = None
    ) -> CounterDict:
        """Create a new counter (authenticated). Example: client = TickrClient(api_key="..."); client.create_counter(name="My Counter", is_private=True, is_readonly=False)"""
        url = f"{self.base_url}/api/counters"
        data = {"name": name, "initial_value": initial_value}
        if is_private is not None:
            data["is_private"] = is_private
        if is_readonly is not None:
            data["is_readonly"] = is_readonly
        resp = requests.post(url, json=data, headers=self._headers())
        resp.raise_for_status()
        return self._ensure_flags(resp.json())

    def get_counter(self, slug: str) -> CounterDict:
        """Fetch a public counter by slug. Example: client = TickrClient(); client.get_counter(slug="abc123xyz")"""
        url = f"{self.base_url}/api/counters/{slug}"
        resp = requests.get(url, headers=self._headers())
        resp.raise_for_status()
        return self._ensure_flags(resp.json())

    def get_counters(self) -> List[CounterDict]:
        """Fetch all counters for the authenticated user. Example: client = TickrClient(api_key="..."); client.get_counters()"""
        url = f"{self.base_url}/api/counters"
        resp = requests.get(url, headers=self._headers())
        resp.raise_for_status()
        counters = resp.json()
        if isinstance(counters, list):
            return [self._ensure_flags(c) for c in counters]
        # If API returns a single counter, wrap it in a list
        return [self._ensure_flags(counters)]

    def increment_counter(self, slug: str, increment_by: int = 1) -> CounterDict:
        """Increment a counter by a given value (public or private). Example: client = TickrClient(); client.increment_counter(slug="abc123xyz", increment_by=2)"""
        url = f"{self.base_url}/api/counters/{slug}/increment"
        data = {"increment_by": increment_by}
        resp = requests.post(url, json=data, headers=self._headers())
        resp.raise_for_status()
        return self._ensure_flags(resp.json())

    def update_counter(
        self,
        slug: str,
        name: Optional[str] = None,
        current_value: Optional[int] = None,
        is_private: Optional[bool] = None,
        is_readonly: Optional[bool] = None,
    ) -> CounterDict:
        """Update a counter's name, value, privacy, or readonly status (authenticated, owner only). Example: client = TickrClient(); client.update_counter(slug="abc123xyz", name="Renamed", is_private=True)"""
        url = f"{self.base_url}/api/counters/{slug}"
        data = {}
        if name is not None:
            data["name"] = name
        if current_value is not None:
            data["current_value"] = current_value
        if is_private is not None:
            data["is_private"] = is_private
        if is_readonly is not None:
            data["is_readonly"] = is_readonly
        if not data:
            raise ValueError(
                "At least one of 'name', 'current_value', 'is_private', or 'is_readonly' must be provided."
            )
        resp = requests.put(url, json=data, headers=self._headers())
        resp.raise_for_status()
        return self._ensure_flags(resp.json())

    def delete_counter(self, slug: str) -> None:
        """Delete a counter (authenticated, owner only). Example: client = TickrClient(); client.delete_counter(slug="abc123xyz")"""
        url = f"{self.base_url}/api/counters/{slug}"
        resp = requests.delete(url, headers=self._headers())
        resp.raise_for_status()

    @staticmethod
    def _ensure_flags(counter: Any) -> CounterDict:
        """Ensure is_private and is_readonly are always present in counter dicts."""
        if isinstance(counter, dict):
            counter.setdefault("is_private", False)
            counter.setdefault("is_readonly", False)
            return counter  # type: ignore
        # If not a dict, return an empty CounterDict
        return CounterDict(is_private=False, is_readonly=False)
