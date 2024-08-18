import json
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.testclient import TestClient

from ..core.models import CreatePlant, Plant
from ..main import app

client = TestClient(app)

plant = {
    "name": "Amnezia Haze",
    "set_watering_period": 0,
    "set_watering_amount": 0,
    "collaboration": [],
    "grow_stages": [],
    "start_date": datetime.now(timezone.utc),
}


def test_read_main():
    create_plant = CreatePlant.model_validate(plant)
    response = client.post("/plants", content=create_plant.model_dump_json())
    content = response.json()
    created_plant = Plant.model_validate(content)
    assert create_plant.name == created_plant.name
    assert create_plant.collaboration == created_plant.collaboration
    assert create_plant.schedules == created_plant.schedules
    assert create_plant.start_date == created_plant.start_date
