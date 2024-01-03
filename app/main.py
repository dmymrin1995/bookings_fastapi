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
