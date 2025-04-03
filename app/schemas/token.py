from pydantic import BaseModel


class TokenBase(BaseModel):
    access_token: str
    token_type: str
    user_email: str
    user_role: str


class TokenResponse(TokenBase):
    pass


class TokenRead(TokenBase):
    pass
