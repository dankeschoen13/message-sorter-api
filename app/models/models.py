from sqlalchemy import String, Text, DateTime, Boolean, Enum, func
from sqlalchemy.orm import Mapped, mapped_column
from app.extensions import db
from datetime import datetime, timezone
import enum

class TicketStatus(str, enum.Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"

class Message(db.Model):
    __tablename__ = 'messages'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(250),
        nullable=False
    )
    content: Mapped[str|None] = mapped_column(
        Text,
        nullable=True
    )
    category: Mapped[str|None] = mapped_column(
        String(250),
        nullable=True
    )
    status: Mapped[TicketStatus] = mapped_column(
        Enum(TicketStatus, name="ticket_status_enum", create_constraint=True),
        default=TicketStatus.PENDING,
        server_default="PENDING",
        nullable=False
    )
    ai_processed: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default="true",
        nullable=False
    )
    date_added: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        nullable=False
    )
    date_updated: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        nullable=False
    )