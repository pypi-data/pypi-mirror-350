from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.event import listen

from cytra.db.created_mixin import CreatedMixin


class ModifiedMixin(CreatedMixin):
    modified_at = Column(DateTime, nullable=True)

    @property
    def last_modification_time(self):
        return self.modified_at or self.created_at

    @staticmethod
    def before_update(mapper, connection, target):
        target.modified_at = datetime.utcnow()

    @classmethod
    def __declare_last__(cls):
        listen(cls, "before_update", cls.before_update)
