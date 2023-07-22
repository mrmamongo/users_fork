import os
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .settings import DEBUG

load_dotenv()


DATABASE_URL = "postgresql+psycopg2://{user}:{password}@{host}/{db_name}"
DATABASE_URL = DATABASE_URL.format(
    user=os.environ.get("POSTGRES_USER"),
    password=os.environ.get("POSTGRES_PASSWORD"),
    host=os.environ.get("POSTGRES_HOST"),
    db_name=os.environ.get("POSTGRES_DB"),
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
