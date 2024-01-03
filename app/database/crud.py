from sqlalchemy.orm import Session

from . import models


def get_aircrafts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Aircrafts).offset(skip).limit(limit).all()
