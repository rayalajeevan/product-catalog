from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings.base import *

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}".format(**DATABASE_CONFIG.get("Catalog"))
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



