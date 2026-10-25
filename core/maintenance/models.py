"""Persistence model for operator maintenance records."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from core.persistence.database import Base


class MaintenanceJournalEntry(Base):
    """A clearly classified manual or verified hardware maintenance event."""

    __tablename__ = "maintenance_journal"

    id = Column(Integer, primary_key=True, autoincrement=True)
    operation = Column(String(40), nullable=False, index=True)
    completion_mode = Column(String(30), nullable=False)
    hardware_performed = Column(Boolean, nullable=False, default=False)
    operator = Column(String(120), nullable=False)
    notes = Column(Text, nullable=False, default="")
    performed_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
    )
