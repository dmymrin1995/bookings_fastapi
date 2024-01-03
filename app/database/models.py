from .db import Base
from sqlalchemy import Column, CheckConstraint, CHAR, TEXT, Integer, String


class Aircrafts(Base):
    __tablename__ = "aircrafts"

    aircraft_code = Column(String, primary_key=True, index=True)
    model = Column(String, nullable=False)
    range = Column(Integer, nullable=False)

    __table_args__ = (CheckConstraint("range > 0"),)
