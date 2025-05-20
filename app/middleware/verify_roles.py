from typing import Mapping, Any

from fastapi import HTTPException


def verify_user_role(decoded_token: Mapping[str, Any], allowed_roles: list[str]) -> bool:
    decoded_access_token = decoded_token
    user_allowed_roles = allowed_roles

    if decoded_access_token.get("user_role") in user_allowed_roles:
        return True

    raise HTTPException(status_code=403, detail="Forbidden!")
