import httpx
import json


class Http:
    def __init__(self):
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async def post(
        self, url: str, body: dict, headers: dict, timeout: int = 10
    ):
        """
        POST so‘rovini asinxron yuborish.
        """
        headers = self.headers | headers
        async with httpx.AsyncClient() as client:
            result = await client.post(
                url,
                headers=headers,
                content=json.dumps(body),
                timeout=timeout
            )
            result.raise_for_status()
            return result.json()
