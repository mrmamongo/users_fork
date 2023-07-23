import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .settings import (
    DEBUG,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_DB,
)


DATABASE_URL = "postgresql+psycopg2://{user}:{password}@{host}/{db_name}"
DATABASE_URL = DATABASE_URL.format(
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    db_name=POSTGRES_DB,
)

engine = create_engine(DATABASE_URL, echo=DEBUG)


Session = sessionmaker(engine, expire_on_commit=False)


@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
