import asyncio

from src.core.database import AsyncSessionLocal
from src.core.config import settings
from src.schemas.user import UserCreate
from src.services.user_service import UserAlreadyExistsError, UserService
from src.repositories.user_repository import UserRepository
from src.utils.enums import UserRole


async def create_admin() -> None:
    async with AsyncSessionLocal() as session:
        user_repository = UserRepository(session)
        user_service = UserService(user_repository)

        try:
            user = await user_service.create_user(
                UserCreate(
                    username=settings.ADMIN_USERNAME,
                    password=settings.ADMIN_PASSWORD,
                    role=UserRole.ADMIN,
                    is_active=True,
                )
            )
            await session.commit()
            print(f"Admin user created: {user.username}")
        except UserAlreadyExistsError:
            await session.rollback()
            print(f"Admin user '{settings.ADMIN_USERNAME}' already exists")


if __name__ == "__main__":
    asyncio.run(create_admin())