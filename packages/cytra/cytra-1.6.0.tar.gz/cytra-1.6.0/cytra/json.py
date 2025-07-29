# flake8: noqa

try:  # pragma: nocover
    from ujson import *
except ImportError:  # pragma: nocover
    from json import *
