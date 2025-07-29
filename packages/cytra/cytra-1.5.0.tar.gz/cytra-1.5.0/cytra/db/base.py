from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapper, Query, Session
from sqlalchemy.sql.schema import MetaData

from cytra.db import (
    FilteringMixin,
    OrderingMixin,
    PaginationMixin,
    SerializeMixin,
)


class BaseModel(SerializeMixin):
    __app__ = None

    @classmethod
    def compose_query(cls, query: Query) -> Query:
        if issubclass(cls, FilteringMixin):
            query = cls.filter_by_request(query)

        if issubclass(cls, OrderingMixin):
            query = cls.sort_by_request(query)

        if issubclass(cls, PaginationMixin):
            query = cls.paginate_by_request(query)

        return query


class CytraDBQuery(Query):
    __app__ = None
    _cytra_target: Mapper = None

    def expose(self) -> list:
        return self._cytra_target.dump_query(
            self._cytra_target.compose_query(query=self)
        )

    def __init__(self, entities, session=None):
        firstentity = entities[0]
        if isinstance(firstentity, Mapper):
            self._cytra_target = firstentity.entity

        if hasattr(firstentity, "dump_query"):
            self._cytra_target = firstentity

        super().__init__(entities, session)


class DBSessionProxy(object):
    __cytra_session__ = None

    def __new__(cls) -> Session:
        return super().__new__(cls)

    def __getattr__(self, key):
        return getattr(self.__class__.__cytra_session__, key)

    def __setattr__(self, key, value):
        setattr(self.__class__.__cytra_session__, key, value)

    def __delattr__(self, key):
        delattr(self.__class__.__cytra_session__, key)


metadata = MetaData()
DeclarativeBase: BaseModel = declarative_base(cls=BaseModel, metadata=metadata)
dbsession = DBSessionProxy()
