from typing import List

from sqlalchemy.orm import Query

from cytra.db.access_control_mixin import AccessControlMixin
from cytra.db.transform_mixin import TransformMixin


class SerializeMixin(TransformMixin, AccessControlMixin):

    def to_dict(self) -> dict:
        result = dict()
        for ic in self.__class__.get_readables(self):
            key = self.get_column_key(ic.column)
            result.setdefault(
                self.export_column_name(key, ic.info),
                self.export_value(ic.column, getattr(self, key)),
            )
        return result

    def update_from_dict(self, data: dict) -> None:
        datakeys = data.keys()
        for ic in self.__class__.get_writables(self):
            key = self.get_column_key(ic.column)
            key_ = self.export_column_name(key, ic.info)
            if key_ not in datakeys:
                continue

            setattr(self, key, self.import_value(ic.column, data[key_]))

    def update_from_request(self) -> None:
        self.update_from_dict(self.__app__.request.form)

    @classmethod
    def to_dict_columns(cls, columns, values):
        result = dict()
        inspections = cls.get_inspections()
        excludes = set(
            map(cls.get_column_key, cls.get_excludes("read", model=None))
        )

        for c, v in zip(columns, values):
            key = cls.get_column_key(c)
            ic = inspections["all_by_key"][key]
            if ic.key in excludes:
                continue

            result.setdefault(
                cls.export_column_name(key, ic.info),
                cls.export_value(ic.column, v),
            )

        return result

    @classmethod
    def dump_query(cls, query: Query, columns: tuple = None) -> List[dict]:
        """
        Dump query results in a list of model dictionaries.
        :param query:
        :return:
        """
        if columns:
            return [cls.to_dict_columns(columns, values) for values in query]

        return [o.to_dict() for o in query]
