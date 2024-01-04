from app.config import settings
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(settings.DATABASE_URL_psycopg)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

meta = MetaData(schema="bookings")
Base = declarative_base(metadata=meta)
