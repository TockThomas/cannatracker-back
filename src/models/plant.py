from datetime import datetime
from typing import List

from pydantic import BaseModel

from src.models.grow_stage import GrowStage
from src.models.user import User
from src.models.watering_records import WateringRecord


class Plant(BaseModel):
    id: str
    name: str
    collaboration: List[User]
    grow_stages: List[GrowStage]
    start_date: datetime
    end_date: datetime
    created_at: datetime
    updated_at: datetime
