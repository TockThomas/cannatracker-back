from __future__ import annotations

import dataclasses
import json
from datetime import datetime
from typing import List, Optional, Literal, Any

from pydantic import BaseModel
from pydantic.dataclasses import dataclass
from pydantic.main import IncEx


# User #
class CreateUser(BaseModel):
    email: str
    first_name: str
    last_name: str
    username: str
    password: str


class PublicUserInDB(BaseModel):
    id: str


class PublicUser(PublicUserInDB):
    username: str


class User(PublicUser):
    email: str
    first_name: str
    last_name: str
    plants: List[str]
    collaborated_plants: List[str]
    schedule_templates: List[str]
    created_at: datetime
    updated_at: datetime
    disabled: bool


class UserInDB(User):
    password: str

    def to_user_model(self) -> User:
        model = self.model_dump()
        model.pop("password", None)
        return User.model_validate(model)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Plant #
class CreatePlant(BaseModel):
    name: str
    set_watering_period: Optional[int]
    set_watering_amount: Optional[float | int]
    collaboration: List[str]
    schedules: List[Schedule]
    start_date: datetime


class AbstractPlant(BaseModel):
    id: str
    name: str
    set_watering_period: Optional[int]
    set_watering_amount: Optional[float]
    schedules: List[Schedule]
    watering_records: List[WateringRecord]
    start_date: datetime
    end_date: datetime
    created_at: datetime
    updated_at: datetime
    active: bool


class PlantInDB(AbstractPlant):
    owner: str
    collaboration: List[str]


class Plant(AbstractPlant):
    owner: PublicUser
    collaboration: List[PublicUser]

    def to_db_model(self) -> PlantInDB:
        model = self.model_dump()
        # owner
        model.update({"owner": self.owner.id})
        # collaborator
        collaborators = model.get("collaborators", [])
        collaborator_ids = {co.get("id") for co in collaborators}
        model.update({"collaborators": collaborator_ids})
        return PlantInDB.model_validate(model)


class Schedule(BaseModel):
    name: str
    fertilizers: List[Fertilizer]


class WateringRecord(BaseModel):
    actor: PublicUser
    created_at: datetime


class Fertilizer(BaseModel):
    name: str
    color: str
    amount_by_liter: float


class CreateScheduleTemplate(BaseModel):
    grow_stages: List[Schedule]


class ScheduleTemplate(CreateScheduleTemplate):
    id: str
