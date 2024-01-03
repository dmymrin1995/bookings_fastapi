from app.config import PostgresConfig
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

pc = PostgresConfig()

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{pc.POSTGRES_USER}:{pc.POSTGRES_PASSWORD}@{pc.POSTGRES_HOST}:{pc.POSTGRES_PORT}/{pc.POSTGRES_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

meta = MetaData(schema="bookings")
Base = declarative_base(metadata=meta)
