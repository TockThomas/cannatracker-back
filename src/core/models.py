from __future__ import annotations
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


# User #
class CreateUser(BaseModel):
    email: str
    first_name: str
    last_name: str
    username: str
    password: str


class User(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    username: str
    plants: List[Plant]
    created_at: datetime
    updated_at: datetime
    disabled: bool


class UserInDB(User):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Plant #
class CreatePlant(BaseModel):
    name: str
    collaboration: List[User]
    grow_stages: List[GrowStage]
    start_date: datetime


class Plant(BaseModel):
    id: str
    name: str
    #owner: User
    collaboration: List[User]
    grow_stages: List[GrowStage]
    start_date: datetime
    end_date: datetime
    created_at: datetime
    updated_at: datetime


class GrowStage(BaseModel):
    id: str
    type: str  # TODO: create types for weeks
    week: int
    plant_height: float
    light_time: float
    desired_watering: List[WateringRecord]
    actual_watering: Optional[List[WateringRecord]] = None


class WateringRecord(BaseModel):
    actor: User
    watering: list[Watering]
    created_at: datetime
    # FEATURE: photo


class Watering(BaseModel):
    fertilizer: Fertilizer
    amount: float


class Fertilizer(BaseModel):
    name: str
    color: str
