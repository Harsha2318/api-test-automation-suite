import os
from typing import Any, Dict, Optional

import requests


class APIClient:
    """Small reusable wrapper around requests for REST API testing."""

    def __init__(self, base_url: str, timeout: int = 10) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def _url(self, endpoint: str) -> str:
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"
        return f"{self.base_url}{endpoint}"

    def get(self, endpoint: str, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        return self.session.get(
            self._url(endpoint),
            headers=headers,
            timeout=self.timeout,
        )

    def post(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> requests.Response:
        return self.session.post(
            self._url(endpoint),
            json=json,
            headers=headers,
            timeout=self.timeout,
        )


def get_base_url() -> str:
    return os.getenv("BASE_URL", "http://localhost:8080")
