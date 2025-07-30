from typing import List

from pydantic import BaseModel


class DeleteUserV0(BaseModel):
    password: str


class UpdatePasswordV0(BaseModel):
    old_password: str
    new_password: str


class LogoutAppsV0(BaseModel):
    app_names: List[str]
