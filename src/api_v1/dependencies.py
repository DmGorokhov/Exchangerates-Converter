import pycountry
from fastapi.exceptions import HTTPException


async def get_currency_codes(from_base: str, to_target: str):
    base = pycountry.currencies.get(alpha_3=from_base.upper())
    if not base:
        raise HTTPException(status_code=400,
                            detail=f"{from_base} is incorrect currency code")

    target = pycountry.currencies.get(alpha_3=to_target.upper())
    if not target:
        raise HTTPException(status_code=400,
                            detail=f"{to_target} is incorrect currency code")
    return {"from_base": base.alpha_3, "to_target": target.alpha_3}
