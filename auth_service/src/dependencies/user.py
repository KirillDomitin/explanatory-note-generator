from fastapi import Depends

from src.dependencies.common import get_user_repository
from src.repositories.user_repository import UserRepository
from src.services.user_service import UserService


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserService:
    return UserService(user_repository)