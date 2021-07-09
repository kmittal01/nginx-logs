import typing as t

from column.app.v1.core.security import get_password_hash
from fastapi import HTTPException, status, UploadFile

from . import models as user_models, schemas


def get_user(user_id: str) -> user_models.User:
    """
    Gets user object by id.
    """
    user = user_models.User.objects.get(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def create_user(new_user: schemas.UserCreate) -> user_models.User:
    """
    Creates New User
    """
    new_user_dict = new_user.dict(exclude_unset=True)
    if "password" in new_user_dict and new_user_dict["password"]:
        hashed_password = get_password_hash(new_user_dict["password"])
        new_user_dict["hashed_password"] = hashed_password
    new_user_dict.pop("password")
    new_user = user_models.User(**new_user_dict).save()
    return new_user


def get_user_by_email(email: str) -> user_models.User:
    """
    Gets user by email.
    """
    return user_models.User.objects(email=email).first()
