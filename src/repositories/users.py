from src.models.users import User

from .base import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    model = User
