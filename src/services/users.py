from src.repositories.users import UserRepository
from src.schemas.users import UserCreate


class UserService:
    def create(self, schema: UserCreate) -> int:
        values = schema.model_dump(exclude_none=True)
        return UserRepository().create(values)
