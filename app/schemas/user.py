from enum import Enum
from pydantic import BaseModel, Field, field_validator


class UserRole(str, Enum):
    admin = "admin"
    user = "user"  # default


class UserBase(BaseModel):
    user_email: str = Field(..., min_length=13, example="firstname.lastname@meltwater.com")
    user_name: str = Field(..., min_length=1, example="firstname.lastname")
    role: UserRole = Field(default=UserRole.user)

    @field_validator("user_email")
    def email_must_be_meltwater(cls, v: str):
        if not v.endswith("@meltwater.com"):
            raise ValueError("Email must be a meltwater.com address")
        return v


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True

