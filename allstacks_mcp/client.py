"""HTTP client for Allstacks API communication"""

from typing import Dict, Optional, Tuple
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
    ):
        if token and (username or password):
            raise ValueError("Provide either token OR username+password, not both")
        if not token and not (username and password):
            raise ValueError("Must provide token, or both username and password")

        self.username = username
        self.password = password
        self.token = token
        self.base_url = base_url.rstrip("/")

        self.auth: Optional[Tuple[str, str]] = (username, password) if token is None else None
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
    ) -> Dict:
        """Make an async HTTP request to the Allstacks API"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"

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
                if expect_json:
                    return response.json()
                return {"raw_body": response.text}
            except httpx.HTTPStatusError as e:
                return {
                    "error": True,
                    "status_code": e.response.status_code,
                    "message": f"HTTP error: {e.response.text}",
                }
            except Exception as e:
                return {"error": True, "message": f"Request failed: {str(e)}"}
