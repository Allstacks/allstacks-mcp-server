"""HTTP client for Allstacks API communication"""

import json
from typing import Any, Dict, Optional, Tuple

import httpx


class AllstacksAPIClient:
    """HTTP client for Allstacks API communication.

    Supports two authentication modes:
    - HTTP Basic with username + password (local account credentials only;
      SSO-only users do not have a working password and must use a token)
    - Bearer token (Personal Access Token / API Token from the Allstacks UI)

    Pass either (username, password) OR token — not both.
    """

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        base_url: str = "https://app.allstacks.com/api/v1/",
        token: Optional[str] = None,
        openapi_schema_url: Optional[str] = None,
    ):
        """Initialize the Allstacks API client with authentication credentials.

        Args:
            username: Username for HTTP Basic auth (requires password).
            password: Password for HTTP Basic auth (requires username).
            base_url: Base URL for the Allstacks API.
            token: Personal Access Token for Bearer auth (mutually exclusive with username/password).
            openapi_schema_url: Absolute URL for the published OpenAPI schema.

        Raises:
            ValueError: If both auth modes are provided or neither is provided.
        """
        if token and (username or password):
            raise ValueError("Provide either token OR username+password, not both")
        if not token and not (username and password):
            raise ValueError("Must provide token, or both username and password")

        self.username = username
        self.password = password
        self.token = token
        self.base_url = base_url.rstrip("/")
        self.openapi_schema_url = openapi_schema_url or f"{self.base_url}/schema/"

        self.auth: Optional[Tuple[str, str]] = (
            (username, password) if token is None else None
        )
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if token is not None:
            self.headers["Authorization"] = f"Bearer {token}"

    async def request(
        self,
        method: str,
        endpoint: str,
        params: Dict = None,
        data: Dict = None,
        timeout_seconds: float = 30.0,
        expect_json: bool = True,
    ) -> Any:
        """Make an async HTTP request to the Allstacks API"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        return await self.request_url(
            method,
            url,
            params=params,
            data=data,
            timeout_seconds=timeout_seconds,
            expect_json=expect_json,
        )

    async def request_url(
        self,
        method: str,
        url: str,
        params: Dict = None,
        data: Dict = None,
        timeout_seconds: float = 30.0,
        expect_json: bool = True,
    ) -> Any:
        """Make an async HTTP request to an absolute Allstacks API URL"""
        async with httpx.AsyncClient(timeout=timeout_seconds) as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    auth=self.auth,
                    headers=self.headers,
                    params=params,
                    json=data,
                )
                response.raise_for_status()
                if not expect_json:
                    return {"raw_body": response.text}
                # Some 2xx responses (e.g. proxy / SSO interstitials) are not JSON.
                # Surface the body verbatim with the status code rather than crashing.
                try:
                    return response.json()
                except json.JSONDecodeError as e:
                    return {
                        "error": True,
                        "status_code": response.status_code,
                        "message": f"Expected JSON but failed to decode: {e}",
                        "raw_body": response.text,
                    }
            except httpx.HTTPStatusError as e:
                return {
                    "error": True,
                    "status_code": e.response.status_code,
                    "message": f"HTTP error: {e.response.text}",
                }
            except httpx.RequestError as e:
                return {
                    "error": True,
                    "status_code": None,
                    "message": f"Request failed: {str(e)}",
                }

    async def get_openapi_schema(self) -> Any:
        """Fetch the published OpenAPI schema with the configured authentication."""
        return await self.request_url("GET", self.openapi_schema_url)
