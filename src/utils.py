import httpx
from typing import Callable
from functools import wraps
from .redis import get_by_hkey, set_by_hkey, delete_hkey


async def make_async_httpx_request(request_url: str) -> dict | None:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(request_url)
            data = response.json()
            return data
        except httpx.RequestError as e:
            """Implement some logging here"""
            return


def cache_currency_pair_rates(get_pair_rate_func: Callable) -> Callable:
    @wraps(get_pair_rate_func)
    async def caching(*args, **kwargs):
        pair_key = f"{kwargs.get('from_base')}{kwargs.get('to_target')}"
        cache_currency = await get_by_hkey("pair_rates", pair_key)
        if cache_currency:
            return float(cache_currency)
        pair_rate = await get_pair_rate_func(*args, **kwargs)
        reverse_pair_key = f"{kwargs.get('to_target')}{kwargs.get('from_base')}"
        reverse_pair_rate = 1 / pair_rate
        await set_by_hkey("pair_rates", pair_key, pair_rate)
        await set_by_hkey("pair_rates", reverse_pair_key, reverse_pair_rate)
        return pair_rate

    return caching


def clear_pair_rates_cache(update_rates_func: Callable) -> Callable:
    @wraps(update_rates_func)
    async def clear_pair_rates(*args, **kwargs):
        await delete_hkey("pair_rates")
        result = await update_rates_func(*args, **kwargs)
        return result

    return clear_pair_rates
