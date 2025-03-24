from pydantic import BaseModel


class UserBase(BaseModel):
    user_email: str = "firstname.lastname@meltwater.com"
    user_name: str = "firstname.lastname"
    role: str = "user"


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True

