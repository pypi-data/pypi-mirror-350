from sqlalchemy import Column, between
from sqlalchemy.orm import Query

from cytra.db.access_control_mixin import AccessControlMixin
from cytra.db.inspection_mixin import InspectionMixin
from cytra.db.transform_mixin import TransformMixin
from cytra.exceptions import InvalidParamError


class FilteringMixin(TransformMixin, AccessControlMixin, InspectionMixin):
    """
    Filter a Sqlalchemy query by a `dict`

    Operators:

    - `=`      Exact string compare, escape the operators described below.
    - `!`      Not
    - `null`   Is null
    - `!null`  Is not null
    - `true`   Is True
    - `false`  Is False
    - `>=`     Greater than or Equal
    - `<=`     Less than or Equal
    - `>`      Greater than
    - `<`      Less than
    - `%~`     Case insensitive Like
    - `%`      Like
    - `^`      In, e.g: ^1,2,3
    - `!^`     Not In, e.g: !^1,2,3
    - `~`      Between,
               e.g: ~2018-05-29T11:23:16+04:30,2018-07-30T11:23:16+04:30

    Note: Without any operator means to Equal with keyword.
    Note: `LIKE` is case-insensitive by default in Sqlite

    Examples:

    where `name` is equal to `John`
    dict(name="John")

    where `age` is between `1` and `18`
    dict(age='~1,18')
    """  # noqa: E501

    @classmethod
    def _get_boolean_expr(cls, column):
        if hasattr(column, "is_"):
            return column

        if hasattr(column, "expr"):
            return column.expr(cls)

    @classmethod
    def filter_by_dict(cls, query: Query, criteria: dict) -> Query:
        for ic in cls.get_readables():
            if ic.type == "relationships":
                continue
            json_name = cls.export_column_name(
                col_key=ic.key, col_info=ic.info
            )
            if json_name in criteria:
                value = criteria[json_name]
                query = cls._filter_by_column_value(query, ic.column, value)

        return query

    @classmethod
    def filter_by_request(cls, query: Query) -> Query:
        return cls.filter_by_dict(query, cls.__app__.request.form)

    @classmethod
    def _filter_by_column_value(
        cls, query: Query, column: Column, value: str
    ) -> Query:
        import_value = getattr(cls, "import_value")
        if not isinstance(value, str):
            raise InvalidParamError

        if value.startswith("="):
            expr = column == import_value(column, value[1:])

        elif value.startswith("^") or value.startswith("!^"):
            value = value.split(",")
            not_ = value[0].startswith("!^")
            # flake8:noqa
            first_item = value[0][2 if not_ else 1 :]
            items = [first_item] + value[1:]
            items = [i for i in items if i.strip()]
            if not len(items):
                raise InvalidParamError("Invalid query string: %s" % value)
            expr = column.in_([import_value(column, j) for j in items])
            if not_:
                expr = ~expr

        elif value.startswith("~"):
            values = value[1:].split(",")
            start, end = [import_value(column, v) for v in values]
            expr = between(column, start, end)

        elif value == "null":
            expr = column.is_(None)
        elif value == "!null":
            expr = column.isnot(None)
        elif value == "!true":
            expr = column.isnot(True)
        elif value == "!false":
            expr = column.isnot(False)
        elif value.startswith("!"):
            expr = column != import_value(column, value[1:])
        elif value.startswith(">="):
            expr = column >= import_value(column, value[2:])
        elif value.startswith(">"):
            expr = column > import_value(column, value[1:])
        elif value.startswith("<="):
            expr = column <= import_value(column, value[2:])
        elif value.startswith("<"):
            expr = column < import_value(column, value[1:])
        elif value.startswith("%~"):
            expr = column.ilike("%%%s%%" % import_value(column, value[2:]))
        elif value.startswith("%"):
            expr = column.like("%%%s%%" % import_value(column, value[1:]))
        else:
            value = import_value(column, value)

            if value is True or value == "true":
                expr = cls._get_boolean_expr(column).is_(True)

            elif value is False or value == "false":
                expr = cls._get_boolean_expr(column).is_(False)

            else:
                expr = column == value

        return query.filter(expr)
