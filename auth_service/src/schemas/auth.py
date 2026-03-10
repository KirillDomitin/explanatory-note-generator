from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.utils.enums import UserRole


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1, max_length=128)


class MessageResponse(BaseModel):
    message: str


class MeResponse(BaseModel):
    id: UUID
    username: str
    role: UserRole
    is_active: bool

    model_config = ConfigDict(from_attributes=True)