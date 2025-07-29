from sqlalchemy import desc
from sqlalchemy.orm import Query

from cytra.db.access_control_mixin import AccessControlMixin
from cytra.db.transform_mixin import TransformMixin


class OrderingMixin(TransformMixin, AccessControlMixin):
    """
    Apply ordering to query from string expression

    purposed to use in URL/query-string.

    for example:
    col1,col2,-col3

    equivalent to:
    asc(col1) then asc(col2) then desc(col3)
    """

    @classmethod
    def create_sort_criteria(cls, sort_columns):
        valid_columns = {
            cls.export_column_name(ic.key, ic.info): getattr(cls, ic.key)
            for ic in cls.get_readables()
            if ic.type != "relationships"
        }
        for column_name, column_is_descending in sort_columns:
            if column_name in valid_columns:
                yield (valid_columns[column_name], column_is_descending)

    @classmethod
    def _sort_by_key_value(cls, query, column, descending=False):
        expression = column

        if column.info.get("collation"):
            expression = expression.collate(column.info["collation"])

        if descending:
            expression = desc(expression)

        return query.order_by(expression)

    @classmethod
    def sort_query(cls, query: Query, sort_exp: dict) -> Query:
        sort_columns = [
            (c[1:] if c.startswith("-") else c, c.startswith("-"))
            for c in sort_exp.split(",")
        ]

        criteria = tuple(cls.create_sort_criteria(sort_columns))

        for criterion in criteria:
            query = cls._sort_by_key_value(query, *criterion)

        return query

    @classmethod
    def sort_by_request(cls, query: Query) -> Query:
        return cls.sort_query(query, cls.__app__.request.query.get("sort", ""))
