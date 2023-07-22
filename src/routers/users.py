from fastapi import APIRouter, status

from src.repositories.users import UserRepository
from src.schemas.users import UserCreate, UserRead
from src.services.users import UserService

router = APIRouter()


@router.get("/")
def get_users() -> list[UserRead]:
    return UserRepository().get_all()


@router.get("/{id}")
def get_user(id: int) -> UserRead:
    return UserRepository().get_by_id(id)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate) -> UserRead:
    return UserService().create(user)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int) -> None:
    UserRepository().delete(id)
