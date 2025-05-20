import os
from typing import Mapping, Any

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
ALGORITHM = os.getenv("ALGORITHM")


def verify_access_token(token: str) -> Mapping[str, Any]:
    access_token = token
    try:
        decoded_access_token = jwt.decode(
            access_token,
            ACCESS_TOKEN_SECRET,
            algorithms=ALGORITHM,
            verify=True
        )
        return decoded_access_token
    except Exception as e:
        raise HTTPException(status_code=403, detail="Forbidden!")
