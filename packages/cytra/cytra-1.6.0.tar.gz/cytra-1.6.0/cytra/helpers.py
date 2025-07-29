import re


def to_camel_case(text):
    """Transform snake_case to CamelCase"""
    return re.sub(r"(_\w)", lambda x: x.group(1)[1:].upper(), text)


def dot_object(obj):
    # Limited javascript-like dot-notation access for testing module
    # Python special keywords (for,while,True, etc) not works

    if isinstance(obj, dict):
        return DotDict(obj)

    if isinstance(obj, list):
        return DotList(obj)

    return obj


class DotList(list):
    def __getitem__(self, key):
        return dot_object(super().__getitem__(key))


class DotDict(dict):
    def __getitem__(self, key):
        return dot_object(super().__getitem__(key))

    def get(self, key, default=None):
        return dot_object(super().get(key, default))

    def __getattr__(self, key):
        return self.__getitem__(key)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)


class LazyString(object):
    def __init__(self, func, *args, **kwargs):
        self._func = func
        self._args = args
        self._kwargs = kwargs

    def __getattr__(self, attr):
        if attr == "__setstate__":
            raise AttributeError(attr)

        string = str(self)
        if hasattr(string, attr):
            return getattr(string, attr)

        raise AttributeError(attr)

    def __repr__(self):
        return "l'{0}'".format(str(self))

    def __str__(self):
        return str(self._func(*self._args, **self._kwargs))

    def __len__(self):
        return len(str(self))

    def __getitem__(self, key):
        return str(self)[key]

    def __iter__(self):
        return iter(str(self))

    def __contains__(self, item):
        return item in str(self)

    def __add__(self, other):
        return str(self) + other

    def __radd__(self, other):
        return other + str(self)

    def __mul__(self, other):
        return str(self) * other

    def __rmul__(self, other):
        return other * str(self)

    def __lt__(self, other):
        return str(self) < other

    def __le__(self, other):
        return str(self) <= other

    def __eq__(self, other):
        return str(self) == other

    def __ne__(self, other):
        return str(self) != other

    def __gt__(self, other):
        return str(self) > other

    def __ge__(self, other):
        return str(self) >= other

    def __html__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))

    def __mod__(self, other):
        return str(self) % other

    def __rmod__(self, other):
        return other + str(self)
