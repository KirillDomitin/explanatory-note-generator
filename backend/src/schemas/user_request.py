import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.db.models import RequestStatus


class UserRequestRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    inn: str
    name: str | None
    status: RequestStatus
    error_message: str | None
    created_at: datetime
    updated_at: datetime


class UserRequestListResponse(BaseModel):
    items: list[UserRequestRead]
    total: int
    limit: int
    offset: int