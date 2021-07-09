#!/usr/bin/env python3
from column.app.v1.users.controller import create_user

from column.app.v1.users.schemas import UserCreate


def init() -> None:
    """
    Script to generate first superuser
    """
    new_user = {"email": "kshitij.mittal01@gmail.com",
                "first_name": "Kshitij",
                "last_name": "Mittal",
                "password": "password",
                "is_superuser": True}
    create_user(UserCreate(**new_user))


if __name__ == "__main__":
    print("Creating superuser kshitij.mittal01@gmail.com")
    init()
    print("Superuser created")
