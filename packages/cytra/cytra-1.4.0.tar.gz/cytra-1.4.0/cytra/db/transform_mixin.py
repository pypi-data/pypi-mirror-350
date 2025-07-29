from datetime import date, datetime, time
from decimal import Decimal
from typing import Any, Union, get_type_hints

import pytz
from sqlalchemy import BigInteger, Column
from sqlalchemy.ext.hybrid import HYBRID_METHOD, HYBRID_PROPERTY
from sqlalchemy.orm import CompositeProperty
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.relationships import RelationshipProperty

from cytra.constants import (
    ISO_DATE_FORMAT,
    ISO_DATETIME_FORMAT,
    ISO_DATETIME_PATTERN,
    ISO_TIME_FORMAT,
)
from cytra.helpers import to_camel_case


class Transformer:
    """Model transformer abstract class"""

    @classmethod
    def export_column_name(cls, name):
        """
        Export column name
        :param name:
        :return:
        """
        raise NotImplementedError  # pragma: no cover

    @classmethod
    def export_datetime(cls, value: datetime):
        """
        Export python datetime
        :param value:
        :return:
        """
        raise NotImplementedError  # pragma: no cover

    @classmethod
    def export_date(cls, value: date):
        """
        Export python date
        :param value:
        :return:
        """
        raise NotImplementedError  # pragma: no cover

    @classmethod
    def export_time(cls, value: time):
        """
        Export python time
        :param value:
        :return:
        """
        raise NotImplementedError  # pragma: no cover

    @classmethod
    def import_datetime(cls, value: Union[str, int]) -> datetime:
        """
        Import datetime field
        :param value:
        :return:
        """
        raise NotImplementedError  # pragma: no cover

    @classmethod
    def import_date(cls, value: Union[str, int]) -> date:
        """
        Import date
        :param value:
        :return:
        """
        raise NotImplementedError  # pragma: no cover

    @classmethod
    def import_time(cls, value: Union[str, int]) -> time:
        """
        Import time
        :param value:
        :return:
        """
        raise NotImplementedError  # pragma: no cover


class DefaultTransformer(Transformer):
    @classmethod
    def export_column_name(cls, key):
        return to_camel_case(key)

    @classmethod
    def export_datetime(cls, value):
        return value.isoformat()

    @classmethod
    def export_date(cls, value):
        return value.isoformat()

    @classmethod
    def export_time(cls, value):
        return value.isoformat()

    @classmethod
    def import_datetime(cls, value):
        match = ISO_DATETIME_PATTERN.match(value)
        if not match:
            raise ValueError("Invalid datetime format")

        res = datetime.strptime(match.group(1), ISO_DATETIME_FORMAT)
        if match.group(2) and len(match.group(2)) > 0:
            res = res.replace(microsecond=int(match.group(2)))

        return res

    @classmethod
    def import_date(cls, value):
        try:
            return datetime.strptime(value, ISO_DATE_FORMAT).date()
        except ValueError:
            raise ValueError("Invalid date format")

    @classmethod
    def import_time(cls, value):
        try:
            return datetime.strptime(value, ISO_TIME_FORMAT).time()
        except ValueError:
            raise ValueError("Invalid date format")


class DefaultTransformerUTC(DefaultTransformer):
    @classmethod
    def export_datetime(cls, value):
        value = value.replace(tzinfo=pytz.utc)
        return super().export_datetime(value)

    @classmethod
    def export_time(cls, value):
        value = value.replace(tzinfo=pytz.utc)
        return super().export_time(value)


class TransformMixin:
    """
    Transform columns

    Note: All mixins must respect to this mixin while intracting with
    outside of the model.
    """

    __transformer__ = DefaultTransformerUTC

    @classmethod
    def import_value(cls, c: Column, v: Union[None, str]) -> Any:
        """
        Import value for a column.
        :param column:
        :param v:
        :return:
        """
        if v is None:
            return v

        if isinstance(c, Column) or isinstance(c, InstrumentedAttribute):
            try:
                type_ = c.type.python_type
            except NotImplementedError:
                type_ = None

        elif hasattr(c, "descriptor"):
            # using type annotation for hybrid_property
            cd = c.descriptor
            if (
                hasattr(cd, "extension_type")
                and cd.extension_type == HYBRID_PROPERTY
            ):
                type_ = get_type_hints(cd.fget).get("return")
            else:
                type_ = None

        elif (
            hasattr(c, "extension_type")
            and c.extension_type == HYBRID_PROPERTY
        ):
            type_ = get_type_hints(c.fget).get("return")

        else:  # pragma: nocover
            type_ = None

        if type_ is bool and not isinstance(v, bool):
            return str(v).lower() == "true"

        if type_ == datetime:
            return cls.__transformer__.import_datetime(v)

        if type_ == date:
            return cls.__transformer__.import_date(v)

        if type_ == time:
            return cls.__transformer__.import_time(v)

        return v

    @classmethod
    def export_value(cls, c: Column, v: Any) -> tuple:
        """
        Prepare column value to export.
        :param c:
        :param v:
        :return:
        """
        if (
            hasattr(c, "property")
            and isinstance(c.property, RelationshipProperty)
            and c.property.uselist
        ):
            return [c.to_dict() for c in v]

        if hasattr(c, "property") and isinstance(
            c.property, CompositeProperty
        ):
            return v.__composite_values__()

        if v is None:
            return v

        if isinstance(v, datetime):
            return cls.__transformer__.export_datetime(v)

        if isinstance(v, date):
            return cls.__transformer__.export_date(v)

        if isinstance(v, time):
            return cls.__transformer__.export_time(v)

        if hasattr(v, "to_dict"):
            return v.to_dict()

        if isinstance(v, Decimal):
            return str(v)

        if hasattr(c, "type") and isinstance(c.type, BigInteger):
            return None if v is None else str(v)

        if c.extension_type == HYBRID_METHOD:
            return v(cls)

        return v

    @classmethod
    def export_column_name(cls, col_key: str, col_info: dict) -> str:
        return cls.__transformer__.export_column_name(
            col_info.get("dict_key", col_key)
        )
