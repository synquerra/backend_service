import httpx
from app.net.exceptions import ExternalAPIError

class HTTPClient:
    def __init__(self, timeout: int = 10):
        self.client = httpx.AsyncClient(timeout=timeout)

    async def get(self, url: str, headers: dict = None, params: dict = None):
        try:
            response = await self.client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise ExternalAPIError(f"GET {url} failed: {e.response.text}")
        except httpx.RequestError as e:
            raise ExternalAPIError(f"GET {url} failed: {str(e)}")

    async def post(self, url: str, headers: dict = None, data: dict = None, json: dict = None):
        try:
            response = await self.client.post(url, headers=headers, data=data, json=json)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise ExternalAPIError(f"POST {url} failed: {e.response.text}")
        except httpx.RequestError as e:
            raise ExternalAPIError(f"POST {url} failed: {str(e)}")

    async def close(self):
        await self.client.aclose()
