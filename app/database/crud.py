from sqlalchemy.orm import Session

from . import models


def get_aircrafts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Aircrafts).offset(skip).limit(limit).all()


def get_flights(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Flights).offset(skip).limit(limit).all()


def get_flight_by_id(db: Session, departure_airport: str):
    return (
        db.query(models.Flights)
        .filter(models.Flights.departure_airport == departure_airport)
        .all()
    )
