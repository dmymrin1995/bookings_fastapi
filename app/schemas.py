from pydantic import BaseModel
from typing import Optional


class AircraftBase(BaseModel):
    aircraft_code: str
    model: str
    range: int


class AircraftCreate(AircraftBase):
    pass


class Aircraft(AircraftBase):
    class Config:
        orm_mode = True
