"""HTTP client for Allstacks API communication"""

import json
from typing import Dict
import httpx


class AllstacksAPIClient:
    """HTTP client for Allstacks API communication using HTTP Basic Auth"""

    def __init__(self, username: str, password: str, base_url: str):
        self.username = username
        self.password = password
        self.base_url = base_url.rstrip("/")
        self.auth = (username, password)  # HTTP Basic Auth tuple
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

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
                    auth=self.auth,  # HTTP Basic Auth
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
