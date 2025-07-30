import httpx
from typing import Optional, Dict, Any

class Api:
    def __init__(self, api_key: str, base_url: str = "https://open.nestcode.org/"):
        self.api_key = api_key
        self.base_url = base_url
        self.api_version: Optional[int] = None
        self.client = httpx.Client(base_url=self.base_url, timeout=10.0)
        self.async_client = httpx.AsyncClient(base_url=self.base_url, timeout=10.0)

    def version(self, version: int) -> "Api":
        self.api_version = version
        return self

    def _build_url(self, endpoint: str, params: Dict[str, Any]) -> str:
        if not self.api_version:
            raise ValueError("API version not set. Use `.version(<number>)`.")
        query_params = "&".join([f"{k}={v}" for k, v in params.items()])
        api_path = f"apis-{self.api_version}/{endpoint}"
        return f"{api_path}?{query_params}" if query_params else api_path

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        params = params or {}
        params["key"] = self.api_key

        url = self._build_url(endpoint, params)

        try:
            response = self.client.get(url)
            return {
                "status_code": response.status_code,
                "body": response.json(),
            }
        except httpx.HTTPStatusError as e:
            return {
                "status_code": e.response.status_code,
                "body": e.response.text,
                "error": str(e),
            }
        except Exception as e:
            return {
                "status_code": 0,
                "body": None,
                "error": str(e),
            }

    async def aget(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        params = params or {}
        params["key"] = self.api_key

        url = self._build_url(endpoint, params)

        try:
            response = await self.async_client.get(url)
            return {
                "status_code": response.status_code,
                "body": response.json(),
            }
        except httpx.HTTPStatusError as e:
            return {
                "status_code": e.response.status_code,
                "body": e.response.text,
                "error": str(e),
            }
        except Exception as e:
            return {
                "status_code": 0,
                "body": None,
                "error": str(e),
            }

    def close(self):
        self.client.close()

    async def aclose(self):
        await self.async_client.aclose()
