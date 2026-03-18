import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.dialects.postgresql import ENUM, UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class RequestStatus(str, enum.Enum):
    SUCCESS = "success"
    FAILED = "failed"


class UserRequest(Base):
    __tablename__ = "user_requests"

    __table_args__ = (
        Index("ix_user_requests_user_id_created_at", "user_id", "created_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        # ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    inn: Mapped[str] = mapped_column(
        String(12),
        nullable=False,
    )
    name: Mapped[str | None] = mapped_column(
        String(512),
        nullable=True,
    )
    status: Mapped[RequestStatus] = mapped_column(
        ENUM(
            RequestStatus,
            name="request_status_enum",
            values_callable=lambda enum_cls: [item.value for item in enum_cls],
            create_type=True,
        ),
        nullable=False,
    )
    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
        server_default=func.now(),
    )