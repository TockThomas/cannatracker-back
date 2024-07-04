from datetime import datetime

from pydantic import BaseModel

from src.models.user import User
from src.models.watering import Watering


class WateringRecord(BaseModel):
    actor: User
    watering: list[Watering]
    created_at: datetime
    # FEATURE: photo
