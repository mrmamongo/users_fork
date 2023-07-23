from sqlalchemy import update

from src.models.users import User

from .base import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User

    def change_password(self, id: int, password: str):
        with self.session() as session:
            stmt = (
                update(self.model).where(self.model.id == id).values(password=password)
            )
            result = session.execute(stmt)
        return result
