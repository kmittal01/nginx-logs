import typing as t
from pydantic import BaseModel
from typing import Optional
from ..custom_base_schemas import CustomBaseModel, CustomIdModel


class UserNoDate(BaseModel):
    email: str
    is_active: bool = True
    is_superuser: bool = False
    first_name: str = None
    last_name: str = None
    user_type: str = 'general'
    old_id: Optional[int] = None
    username: Optional[str] = None
    profile_pic: Optional[str] = None
    org_id: Optional[str] = None


class UserBase(CustomBaseModel, UserNoDate):
    pass


class UserCreate(UserNoDate):
    password: Optional[str]

    class Config:
        orm_mode = True


class User(UserBase, CustomIdModel):
    pass