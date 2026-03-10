from uuid import UUID

from src.core.security import (
    InvalidTokenTypeError,
    TokenError,
    TokenExpiredError,
    create_access_token,
    create_refresh_token,
    decode_access_token,
    decode_refresh_token,
    get_token_ttl_seconds,
    verify_password,
)
from src.models.user import User
from src.repositories.blacklist_repository import BlacklistRepository
from src.repositories.refresh_repository import RefreshRepository
from src.repositories.user_repository import UserRepository


class InvalidCredentialsError(Exception):
    pass


class InactiveUserError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


class AuthService:
    def __init__(
        self,
        user_repository: UserRepository,
        refresh_repository: RefreshRepository,
        blacklist_repository: BlacklistRepository,
    ):
        self.user_repository = user_repository
        self.refresh_repository = refresh_repository
        self.blacklist_repository = blacklist_repository

    async def authenticate_user(self, username: str, password: str) -> User:
        user = await self.user_repository.get_by_username(username)
        if not user:
            raise InvalidCredentialsError("Invalid username or password")

        if not user.is_active:
            raise InactiveUserError("User is inactive")

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError("Invalid username or password")

        return user

    async def login(self, username: str, password: str) -> tuple[str, str, User]:
        user = await self.authenticate_user(username, password)

        access_token = create_access_token(str(user.id))
        refresh_token = create_refresh_token(str(user.id))

        refresh_payload = decode_refresh_token(refresh_token)
        refresh_jti = refresh_payload["jti"]

        await self.refresh_repository.save_refresh_session(
            jti=refresh_jti,
            user_id=user.id,
            username=user.username,
        )

        return access_token, refresh_token, user

    async def get_current_user_by_access_token(self, access_token: str) -> User:
        try:
            payload = decode_access_token(access_token)
        except (TokenError, TokenExpiredError, InvalidTokenTypeError) as exc:
            raise UnauthorizedError("Invalid or expired access token") from exc

        jti = payload.get("jti")
        sub = payload.get("sub")

        if not jti or not sub:
            raise UnauthorizedError("Invalid access token payload")

        is_blacklisted = await self.blacklist_repository.exists(jti)
        if is_blacklisted:
            raise UnauthorizedError("Access token is blacklisted")

        try:
            user_id = UUID(sub)
        except ValueError as exc:
            raise UnauthorizedError("Invalid user id in token") from exc

        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UnauthorizedError("User not found")

        if not user.is_active:
            raise UnauthorizedError("User is inactive")

        return user

    async def refresh_tokens(self, refresh_token: str) -> tuple[str, str]:
        try:
            payload = decode_refresh_token(refresh_token)
        except (TokenError, TokenExpiredError, InvalidTokenTypeError) as exc:
            raise UnauthorizedError("Invalid or expired refresh token") from exc

        refresh_jti = payload.get("jti")
        sub = payload.get("sub")

        if not refresh_jti or not sub:
            raise UnauthorizedError("Invalid refresh token payload")

        session_data = await self.refresh_repository.get_refresh_session(refresh_jti)
        if not session_data:
            raise UnauthorizedError("Refresh token is invalid or already used")

        try:
            user_id = UUID(sub)
        except ValueError as exc:
            raise UnauthorizedError("Invalid user id in refresh token") from exc

        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise UnauthorizedError("User not found")

        if not user.is_active:
            raise UnauthorizedError("User is inactive")

        await self.refresh_repository.delete_refresh_session(
            jti=refresh_jti,
            user_id=user.id,
        )

        new_access_token = create_access_token(str(user.id))
        new_refresh_token = create_refresh_token(str(user.id))

        new_refresh_payload = decode_refresh_token(new_refresh_token)
        new_refresh_jti = new_refresh_payload["jti"]

        await self.refresh_repository.save_refresh_session(
            jti=new_refresh_jti,
            user_id=user.id,
            username=user.username,
        )

        return new_access_token, new_refresh_token

    async def logout(
        self,
        access_token: str | None,
        refresh_token: str | None,
    ) -> None:
        if access_token:
            try:
                access_payload = decode_access_token(access_token)
                access_jti = access_payload.get("jti")
                if access_jti:
                    ttl = get_token_ttl_seconds(access_payload)
                    await self.blacklist_repository.add(access_jti, ttl)
            except (TokenError, TokenExpiredError, InvalidTokenTypeError):
                pass

        if refresh_token:
            try:
                refresh_payload = decode_refresh_token(refresh_token)
                refresh_jti = refresh_payload.get("jti")
                sub = refresh_payload.get("sub")

                if refresh_jti and sub:
                    await self.refresh_repository.delete_refresh_session(
                        jti=refresh_jti,
                        user_id=sub,
                    )
            except (TokenError, TokenExpiredError, InvalidTokenTypeError):
                pass

    async def logout_all(
        self,
        user: User,
        access_token: str | None,
    ) -> None:
        await self.refresh_repository.delete_all_user_sessions(user.id)

        if access_token:
            try:
                access_payload = decode_access_token(access_token)
                access_jti = access_payload.get("jti")
                if access_jti:
                    ttl = get_token_ttl_seconds(access_payload)
                    await self.blacklist_repository.add(access_jti, ttl)
            except (TokenError, TokenExpiredError, InvalidTokenTypeError):
                pass