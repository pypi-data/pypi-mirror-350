from typing import Any, Iterable

from cytra.db import InspectedColumn, InspectionMixin


class AccessControlMixin(InspectionMixin):
    """
    Controls access to properties

    Note: All mixins must respect to this mixin while intracting with
    outside of the model.
    """

    @classmethod
    def get_readables(cls, model: Any = None) -> Iterable[InspectedColumn]:
        inspections = cls.get_inspections()
        excludes = set(
            map(cls.get_column_key, cls.get_excludes("read", model=model))
        )
        for ic in inspections["all"]:
            if (
                ic.type == "proxies"
                or ic.info.get("protected")
                or ic.key in excludes
            ):
                continue

            yield ic

    @classmethod
    def get_writables(cls, model: Any = None) -> Iterable[InspectedColumn]:
        inspections = cls.get_inspections()
        excludes = set(
            map(cls.get_column_key, cls.get_excludes("write", model=model))
        )
        for ic in inspections["all"]:
            if (
                ic.type == "relationships"
                or ic.info.get("readonly")
                or ic.key in excludes
            ):
                continue

            yield ic

    @classmethod
    def get_excludes(cls, mode: str, model: Any = None):
        if mode == "read":
            yield from cls.get_read_excludes(model)

        elif mode == "write":
            yield from cls.get_write_excludes(model)

    @classmethod
    def get_read_excludes(cls, model: Any = None):  # pragma: nocover
        return
        yield

    @classmethod
    def get_write_excludes(cls, model: Any = None):  # pragma: nocover
        return
        yield
