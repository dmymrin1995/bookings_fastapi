from .db import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    DateTime,
    CheckConstraint,
    UniqueConstraint,
    ForeignKey,
    ForeignKeyConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB


class Aircrafts(Base):
    __tablename__ = "aircrafts"

    aircraft_code = Column(String(3), primary_key=True, index=True)
    model = Column(String, nullable=False)
    range = Column(Integer, nullable=False)

    __table_args__ = (CheckConstraint("range > 0"),)

    flights = relationship("Flights", back_populates="aircrafts")
    seats = relationship("Seats", back_populates="aircrafts", cascade="all, delete")


class Airports(Base):
    __tablename__ = "airports"

    airport_code = Column(String(3), primary_key=True, index=True)
    airport_name = Column(JSONB, nullable=False)
    city = Column(JSONB, nullable=False)
    coordinates = Column(String, nullable=False)
    timezone = Column(String, nullable=False)


class TicketFlights(Base):
    __tablename__ = "ticket_flights"

    ticket_no = Column(
        String(13), ForeignKey("tickets.flight_id"), primary_key=True, index=True
    )
    flight_id = Column(
        Integer, ForeignKey("flights.flight_id"), primary_key=True, index=True
    )
    fare_conditions = Column(Integer, nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)

    ticket = relationship("Ticket", back_populates="flights")
    flight = relationship("Flight", back_populates="tickets")

    __table_args__ = (
        CheckConstraint("amount >= 0"),
        CheckConstraint("fare_conditions IN ('Economy', 'Comfort', 'Business')"),
    )


class Bookings(Base):
    __tablename__ = "bookings"

    book_ref = Column(String(6), primary_key=True)
    book_date = Column(DateTime(timezone=True), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)

    tickets = relationship("Ticket", back_populates="booking")


class Seats(Base):
    __tablename__ = "seats"

    aircraft_code = Column(String(3), primary_key=True)
    seat_no = Column(String(4), primary_key=True)
    fare_conditions = Column(String(10), nullable=False)

    __table_args__ = (
        CheckConstraint("fare_conditions IN ('Economy', 'Comfort', 'Business')"),
    )

    aircrafts = relationship("Aircrafts", back_populates="seats", cascade="all, delete")


class Flights(Base):
    __tablename__ = "flights"

    flight_id = Column(Integer, primary_key=True)
    flight_no = Column(String(6), nullable=False)
    scheduled_departure = Column(DateTime, nullable=False)
    scheduled_arrival = Column(DateTime, nullable=False)
    departure_airport = Column(
        String(3), ForeignKey("airports.airport_code"), nullable=False
    )
    arrival_airport = Column(
        String(3), ForeignKey("airports.airport_code"), nullable=False
    )
    status = Column(String(20), nullable=False)
    aircraft_code = Column(
        String(3), ForeignKey("aircrafts.aircraft_code"), nullable=False
    )
    actual_departure = Column(DateTime)
    actual_arrival = Column(DateTime)

    aircraft = relationship("Aircraft", back_populates="flights")
    departure = relationship("Airport", foreign_keys=[departure_airport])
    arrival = relationship("Airport", foreign_keys=[arrival_airport])
    ticket_flights = relationship("TicketFlights", back_populates="flights")

    __table_args__ = (
        CheckConstraint("scheduled_arrival > scheduled_departure"),
        CheckConstraint(
            "status IN ('On Time', 'Delayed', 'Departed', 'Arrived', 'Scheduled', 'Cancelled')"
        ),
        CheckConstraint(
            "((actual_arrival IS NULL) OR ((actual_departure IS NOT NULL AND actual_arrival IS NOT NULL) AND (actual_arrival > actual_departure)))",
        ),
        UniqueConstraint("flight_no", "scheduled_departure"),
    )


class BoardingPasses(Base):
    __tablename__ = "boarding_passes"

    ticket_no = Column(String(13), primary_key=True)
    flight_id = Column(Integer, primary_key=True)
    boarding_no = Column(Integer, nullable=False)
    seat_no = Column(String(4), nullable=False)

    __table_args__ = (
        UniqueConstraint("flight_id", "boarding_no", name="uq_flight_boarding"),
        UniqueConstraint("flight_id", "seat_no", name="uq_flight_seat"),
        ForeignKeyConstraint(
            ["ticket_no", "flight_id"], ["tickets.ticket_no", "tickets.flight_id"]
        ),
    )


class Ticket(Base):
    __tablename__ = "tickets"

    ticket_no = Column(String(13), primary_key=True)
    book_ref = Column(String(6), ForeignKey("bookings.book_ref"), nullable=False)
    passenger_id = Column(String(20), nullable=False)
    passenger_name = Column(String, nullable=False)
    contact_data = Column(JSONB)

    booking = relationship("Bookings", back_populates="tickets")
    ticket_flights = relationship("TicketFlights", back_populates="ticket")
