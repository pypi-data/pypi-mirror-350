from sqlalchemy import inspect

from cytra.db.access_control_mixin import InspectionMixin
from cytra.db.transform_mixin import TransformMixin


class AttrStateMixin(TransformMixin, InspectionMixin):
    def get_attr_changes(self) -> dict:
        state = inspect(self)
        changes = {}

        for attr in state.attrs:
            hist = state.get_history(attr.key, True)

            if not hist.has_changes():
                continue

            old_value = hist.deleted[0] if hist.deleted else None
            new_value = hist.added[0] if hist.added else None
            changes[attr.key] = (old_value, new_value)

        return changes

    def export_attr_changes(self) -> dict:
        res = {}
        inspections = self.get_inspections()["all_by_key"]
        for k, v in self.get_attr_changes().items():
            ic = inspections[k]
            res[self.export_column_name(k, ic.info)] = (
                self.export_value(ic.column, v[0]),
                self.export_value(ic.column, v[1]),
            )
        return res
