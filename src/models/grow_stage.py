from typing import Union, List, Optional

from pydantic import BaseModel

from src.models.watering_records import WateringRecord


class GrowStage(BaseModel):
    id: str
    type: str  # TODO: create types for weeks
    week: int
    plant_height: float
    light_time: float
    desired_watering: List[WateringRecord]
    actual_watering: Optional[List[WateringRecord]] = None
