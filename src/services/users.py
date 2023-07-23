import bcrypt

from src.repositories.users import UserRepository
from src.schemas.users import UserCreate, UserRead

from .emails import VerificationEmailSender


def make_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def verify_password(hashed_password, password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


class UserService:
    def create(self, schema: UserCreate) -> UserRead:
        values = schema.model_dump(exclude_none=True)
        values["password"] = make_password(values["password"])
        user = UserRepository().create(values)
        VerificationEmailSender(user.email).send_email()
        return user
