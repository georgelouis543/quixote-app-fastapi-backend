from fastapi import HTTPException
from google.auth.transport import requests
from google.oauth2 import id_token
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")


# Declaring Middleware for login Route to handle Google Token
def verify_google_token(token: str) -> dict:
    print(token)
    if not token:
        raise HTTPException(status_code=401, detail="Could not authorize User!")

    try:
        id_info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        id_info_domain = dict(id_info).get("hd", "None")
    except Exception as e:
        print(f"Exited with Exception {e}")
        raise HTTPException(status_code=401, detail="Could not authorize User!")

    if id_info_domain == "meltwater.com":
        id_email = dict(id_info).get("email", "None")
        return {
            "status_code": 200,
            "email": id_email,
            "message": "Success"
        }

    else:
        raise HTTPException(status_code=403, detail="Person must be a Meltwater User")
