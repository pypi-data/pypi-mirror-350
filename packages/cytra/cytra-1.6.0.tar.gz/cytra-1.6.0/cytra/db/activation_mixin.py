from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.hybrid import hybrid_property


class ActivationMixin:
    activated_at = Column(DateTime, nullable=True)

    @hybrid_property
    def is_active(self):
        return self.activated_at is not None

    @is_active.setter
    def is_active(self, value):
        self.activated_at = datetime.utcnow() if value else None

    @is_active.expression
    def is_active(self):
        return self.activated_at.isnot(None)

    @classmethod
    def filter_activated(cls, query=None):
        return (query or cls.query).filter(cls.is_active)
