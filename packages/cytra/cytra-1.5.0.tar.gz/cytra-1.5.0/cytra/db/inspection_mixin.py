from typing import Any, NamedTuple

from sqlalchemy import Column, inspect
from sqlalchemy.ext.associationproxy import ASSOCIATION_PROXY
from sqlalchemy.ext.hybrid import HYBRID_PROPERTY


class InspectedColumn(NamedTuple):
    type: str
    key: str
    info: dict
    column: Any


class InspectionMixin:
    __abstract__ = True
    __cytra_inspections__: dict = None
    __cytra_inspections_key__: str = None

    @classmethod
    def _update_inspections(cls):
        res = dict(
            all=[],
            all_by_key={},
            hybrid_properties=[],
            relationships=[],
            composites=[],
            synonyms=[],
            columns=[],
            proxies=[],
        )
        mapper = inspect(cls)
        for k, c in mapper.all_orm_descriptors.items():

            if k == "__mapper__":  # pragma:nocover
                continue

            if c.extension_type == ASSOCIATION_PROXY:
                cc_type = "proxies"

            elif c.extension_type == HYBRID_PROPERTY:
                cc_type = "hybrid_properties"

            elif k in mapper.relationships:
                cc_type = "relationships"

            elif k in mapper.synonyms:
                cc_type = "synonyms"

            elif k in mapper.composites:
                cc_type = "composites"

            else:
                cc_type = "columns"

            ic = InspectedColumn(
                type=cc_type,
                key=cls.get_column_key(c),
                info=cls.get_column_info(c),
                column=c,
            )
            res[cc_type].append(ic)
            res["all"].append(ic)
            res["all_by_key"][ic.key] = ic
        return res

    @classmethod
    def get_inspections(cls):
        key = cls.__name__
        if cls.__cytra_inspections__ is None or (
            cls.__cytra_inspections_key__ != key
        ):
            cls.__cytra_inspections__ = cls._update_inspections()
            cls.__cytra_inspections_key__ = key

        return cls.__cytra_inspections__

    @classmethod
    def get_column_info(cls, column: Column) -> dict:
        # Use original property for proxies
        if hasattr(column, "original_property") and column.original_property:
            info = column.info.copy()
            info.update(column.original_property.info)
            return info

        return column.info

    @classmethod
    def get_column_key(cls, column: Column) -> str:
        if hasattr(column, "key"):
            return column.key

        # `hybrid_method`
        if hasattr(column, "func"):
            return column.func.__name__

        # `hybrid_property`
        return column.__name__
