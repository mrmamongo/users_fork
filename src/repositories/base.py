from abc import ABC, abstractmethod

from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.config.database import get_session
from src.exceptions.base import HTTPNotFound, UniqueConstraintError


class BaseRepository(ABC):
    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_by_id(self, id: int):
        pass

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass


class SQLAlchemyRepository(BaseRepository):
    model = None

    def __init__(self):
        self.session = get_session

    def get_all(self):
        with self.session() as session:
            query = select(self.model)
            result = session.scalars(query).all()

        return result

    def get_by_id(self, id: int):
        with self.session() as session:
            return self.get_object_or_404(session, id)

    def create(self, values: dict[str, str | int | bool]):
        with self.session() as session:
            try:
                stmt = insert(self.model).values(values).returning(self.model)
                result = session.execute(stmt).one()[0]
            except IntegrityError as error:
                table_name = error.orig.diag.table_name
                column_name = error.orig.diag.constraint_name[len(table_name) + 1 : -4]
                raise UniqueConstraintError(column_name)
        return result

    def update(self, id: int, values: dict[str, str | int | bool]):
        with self.session() as session:
            self.get_object_or_404(session, id)
            try:
                stmt = update(self.model).where(id == id).values(values)
                result = session.execute(stmt).one()[0]
            except IntegrityError as error:
                table_name = error.orig.diag.table_name
                column_name = error.orig.diag.constraint_name[len(table_name) + 1 : -4]
                raise UniqueConstraintError(column_name)
        return result

    def delete(self, id: int):
        with self.session() as session:
            instance = self.get_object_or_404(session, id)
            session.delete(instance)

    def get_object_or_404(self, session: Session, id: int):
        instance = session.get(self.model, id)
        if not instance:
            raise HTTPNotFound
        return instance
