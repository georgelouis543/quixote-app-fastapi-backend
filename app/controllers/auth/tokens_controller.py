import datetime
import jwt
from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
REFRESH_TOKEN_SECRET = os.getenv("REFRESH_TOKEN_SECRET")
ALGORITHM = os.getenv("ALGORITHM")


# These functions are responsible for creating Access and Refresh tokens
def create_refresh_token(user_email: str, user_name: str):
    try:
        found_user_email = user_email
        found_user_name = user_name
        payload = {
            'user_email': found_user_email,
            'username': found_user_name,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expiration time
        }
        refresh_token = jwt.encode(payload, REFRESH_TOKEN_SECRET, algorithm=ALGORITHM)
        print(refresh_token)
        return refresh_token

    except Exception as e:
        print(f"Exited with Exception: {e}")
        return None


def create_access_token(user_email: str, user_name: str):
    try:
        user_email = user_email
        user_name = user_name
        print(user_email)
        payload = {
            'user_email': user_email,
            'username': user_name,
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=10)  # Token expiration time
        }
        access_token = jwt.encode(payload, ACCESS_TOKEN_SECRET, algorithm=ALGORITHM)
        print(access_token)
        return access_token

    except Exception as e:
        print(f'Exited with Exception: {e}')
        return None
