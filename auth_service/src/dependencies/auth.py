from fastapi import Depends

from src.dependencies.common import (
    get_blacklist_repository,
    get_refresh_repository,
    get_user_repository,
)
from src.repositories.blacklist_repository import BlacklistRepository
from src.repositories.refresh_repository import RefreshRepository
from src.repositories.user_repository import UserRepository
from src.services.auth_service import AuthService


def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
    refresh_repository: RefreshRepository = Depends(get_refresh_repository),
    blacklist_repository: BlacklistRepository = Depends(get_blacklist_repository),
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        refresh_repository=refresh_repository,
        blacklist_repository=blacklist_repository,
    )