from pydantic import BaseModel


class UserBase(BaseModel):
    user_email: str
    user_name: str
    role: str
