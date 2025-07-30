import importlib
import typing as t


def try_import(module: str) -> t.Any | None:
    try:
        return importlib.import_module(module)
    except:
        return None
