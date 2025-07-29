from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    ColumnProperty,
    InstrumentedAttribute,
    Mapper,
    Query,
    Session,
)
from sqlalchemy.sql.schema import MetaData

from cytra.db import (
    FilteringMixin,
    OrderingMixin,
    PaginationMixin,
    SerializeMixin,
)


class BaseModel(SerializeMixin):
    __app__ = None
    _cytra_query_columns: tuple = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cytra_query_columns = None

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
    _cytra_target_cols: tuple = None
    _is_column_query: bool = False

    def expose(self) -> list:
        return self._cytra_target.dump_query(
            self._cytra_target.compose_query(query=self),
            columns=self._cytra_target_cols,
        )

    def __init__(self, entities, session=None):
        firstentity = entities[0]

        # Handle model query_property (Model.query)
        if isinstance(firstentity, Mapper):
            self._cytra_target = firstentity.entity

        # Handle session query (db_session.query(Model))
        if hasattr(firstentity, "dump_query"):
            self._cytra_target = firstentity

        # Handle column queries (Model.field1, Model.field2)
        if all(
            isinstance(e, (InstrumentedAttribute, ColumnProperty))
            for e in entities
        ):
            first_attr = entities[0]
            if hasattr(first_attr, "class_") and hasattr(
                first_attr.class_, "dump_query"
            ):
                self._cytra_target = first_attr.class_
                self._cytra_target_cols = entities
                self._is_column_query = True

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
