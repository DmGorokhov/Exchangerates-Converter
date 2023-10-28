from redis.asyncio import Redis
from typing import Optional

redis_client: Redis = None  # type: ignore


async def set_by_hkey(hkey: str, *args) -> Optional[int]:
    return await redis_client.hset(hkey, *args)


async def get_by_hkey(hkey: str, key: str) -> Optional[float]:
    return await redis_client.hget(hkey, key)


async def delete_hkey(hkey: str) -> None:
    await redis_client.delete(hkey)
    return
