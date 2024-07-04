from pydantic import BaseModel


class Fertilizer(BaseModel):
    name: str
    color: str
