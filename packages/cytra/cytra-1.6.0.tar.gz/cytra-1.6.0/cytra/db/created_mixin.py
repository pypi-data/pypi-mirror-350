from datetime import datetime

from sqlalchemy import Column, DateTime


class CreatedMixin:
    created_at = Column(
        DateTime,
        default=lambda: datetime.utcnow(),
        nullable=False,
    )
