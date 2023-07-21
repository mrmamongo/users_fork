from datetime import datetime

from fastapi import status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, validator


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
    last_login: datetime | None


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    re_password: str

    @validator("re_password")
    def passwords_match(cls, password, values):
        if password != values["password"]:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Пароли не совпадают",
            )
