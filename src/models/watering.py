from typing import Union

from pydantic import BaseModel

from src.models.fertilizer import Fertilizer


class Watering(BaseModel):
    fertilizer: Fertilizer
    amount: float
