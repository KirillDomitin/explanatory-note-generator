from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.utils.enums import UserRole


class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=8, max_length=128)
    role: UserRole = UserRole.USER
    is_active: bool = True


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=1, max_length=50)
    password: str | None = Field(default=None, min_length=8, max_length=128)
    role: UserRole | None = None
    is_active: bool | None = None


class UserResponse(BaseModel):
    id: UUID
    username: str
    role: UserRole
    is_active: bool

    model_config = ConfigDict(from_attributes=True)