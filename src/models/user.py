from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from src.models.plant import Plant


"""class User(BaseModel):
    id: str
    email: str
    password: str
    first_name: str
    last_name: str
    username: str
    plants: List[Plant]
    created_at: datetime
    updated_at: datetime"""


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str
