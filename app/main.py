from fastapi import FastAPI, Depends
from typing import List
from sqlalchemy.orm import Session

from .database.db import SessionLocal, engine
from .database import crud
from . import schemas


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get("/aircrafts/", response_model=List[schemas.Aircraft])
def read_aircrafts(skip: int = 0, limit: int = 0, db: Session = Depends(get_db)):
    aircrafts = crud.get_aircrafts(db=db, skip=skip, limit=limit)
    return aircrafts


@app.get("/flights/")
def read_flights(skip: int = 0, limit: int = 0, db: Session = Depends(get_db)):
    flights = crud.get_flights(db=db, skip=skip, limit=limit)
    return flights


@app.get("/flight/{departure_airport}")
def get_flight(departure_airport: str, db: Session = Depends(get_db)):
    flights_by_id = crud.get_flight_by_id(db=db, departure_airport=departure_airport)
    return flights_by_id
