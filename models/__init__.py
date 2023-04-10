from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from settings import (
    POSTGRESQL_USER,
    POSTGRESQL_PASSWORD,
    POSTGRESQL_HOST,
    POSTGRESQL_DATABASE,
    POSTGRESQL_PORT,
)

# Create sqlalchemy session
username = POSTGRESQL_USER
password = POSTGRESQL_PASSWORD
host = POSTGRESQL_HOST
port = POSTGRESQL_PORT
database = POSTGRESQL_DATABASE

engine = create_engine(
    f"postgresql+psycopg://{username}:{password}@{host}:{port}/{database}",
    pool_size=20,
    max_overflow=0,
    pool_timeout=300,
)

Session = sessionmaker(engine, future=True)


def get_db_sync():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# base for model
Base = declarative_base()


from models.log import Logs
from models.user import User


class Migration:
    def __init__(self, engine=engine, Base=Base) -> None:
        self.__engine = engine
        self.__Base = Base

    def create_all_table(self):
        self.__Base.metadata.create_all(self.__engine)

    def delete_all_table(self):
        self.__Base.metadata.drop_all(self.__engine)
