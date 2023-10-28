import httpx


async def make_async_httpx_request(request_url: str) -> dict | None:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(request_url)
            data = response.json()
            return data
        except httpx.RequestError as e:
            """Implement some logging here"""
            return
