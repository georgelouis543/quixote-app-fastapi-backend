from enum import Enum
from typing import Optional

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


class UserUpdate(BaseModel):
    user_email: Optional[str] = Field(None, min_length=13)
    user_name: Optional[str] = Field(None, min_length=1)
    role: Optional[UserRole] = Field(None)

    @field_validator("user_email")
    def email_must_be_meltwater(cls, v: str):
        if v is not None and not v.endswith("@meltwater.com"):
            raise ValueError("Email must be a meltwater.com address")
        return v


class UpdatedUserResponse(BaseModel):
    id: int
    user_email: str
    user_name: str
    role: UserRole

    class Config:
        from_attributes = True


