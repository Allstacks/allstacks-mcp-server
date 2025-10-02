"""HTTP client for Allstacks API communication"""

from typing import Dict, Optional
import httpx


class AllstacksAPIClient:
    """HTTP client for Allstacks API communication using HTTP Basic Auth"""
    
    def __init__(self, username: str, password: str, base_url: str):
        self.username = username
        self.password = password
        self.base_url = base_url.rstrip('/')
        self.auth = (username, password)  # HTTP Basic Auth tuple
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    
    async def request(self, method: str, endpoint: str, params: Dict = None, data: Dict = None) -> Dict:
        """Make an async HTTP request to the Allstacks API"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.request(
                    method=method,
                    url=url,
                    auth=self.auth,  # HTTP Basic Auth
                    headers=self.headers,
                    params=params,
                    json=data
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                return {
                    "error": True,
                    "status_code": e.response.status_code,
                    "message": f"HTTP error: {e.response.text}"
                }
            except Exception as e:
                return {
                    "error": True,
                    "message": f"Request failed: {str(e)}"
                }

