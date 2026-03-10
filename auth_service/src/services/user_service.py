from uuid import UUID

from src.core.security import hash_password
from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.schemas.user import UserCreate, UserUpdate


class UserAlreadyExistsError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, data: UserCreate) -> User:
        existing_user = await self.user_repository.get_by_username(data.username)
        if existing_user:
            raise UserAlreadyExistsError(
                f"User with username '{data.username}' already exists"
            )

        password_hash = hash_password(data.password)

        user = await self.user_repository.create(
            username=data.username,
            password_hash=password_hash,
            role=data.role,
            is_active=data.is_active,
        )
        return user

    async def list_users(self) -> list[User]:
        return await self.user_repository.get_all()

    async def update_user(self, user_id: UUID, data: UserUpdate) -> User:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")

        if data.username is not None and data.username != user.username:
            existing_user = await self.user_repository.get_by_username(data.username)
            if existing_user and existing_user.id != user.id:
                raise UserAlreadyExistsError(
                    f"User with username '{data.username}' already exists"
                )
            user.username = data.username

        if data.password is not None:
            user.password_hash = hash_password(data.password)

        if data.role is not None:
            user.role = data.role

        if data.is_active is not None:
            user.is_active = data.is_active

        return await self.user_repository.update(user)

    async def delete_user(self, user_id: UUID) -> User:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError("User not found")

        user.is_active = False
        return await self.user_repository.update(user)