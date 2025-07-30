import os
import re
import json
import copy
from types import SimpleNamespace


class RootConfigTypeError(TypeError):
    def __init__(self, obj):
        super().__init__(
            f"Root config must be a dict or string, not {type(obj).__name__}"
        )


class SourcePathError(ValueError):
    def __init__(self):
        super().__init__('Attribute "config_path" is required for non-file configs')


class LockedMethodError(AttributeError):
    def __init__(self, name):
        super().__init__(f"Cannot override locked method: {name}")


_locked_methods = (
    "_meta_",
    "to_dict",
    "keys",
    "values",
    "items",
    "get",
    "pop",
    "popitem",
    "clear",
    "copy",
    "update",
    "save",
)


def _to_config(obj, io_params):
    if isinstance(obj, dict):
        return Config(obj, io_params)
    elif isinstance(obj, list):
        return [_to_config(i, io_params) for i in obj]
    else:
        return obj


def _to_dict(obj):
    if isinstance(obj, Config):
        return {k: _to_dict(v) for k, v in vars(obj).items()}
    elif isinstance(obj, list):
        return [_to_dict(i) for i in obj]
    else:
        return obj


def _jsonc_to_json(jsonc_str):
    jsonc_str = re.sub(r"/\*[\s\S]*?\*/", "", jsonc_str)

    def remove_line_comments(line):
        in_string = False
        result = ""
        i = 0
        while i < len(line):
            if line[i] == '"' and (i == 0 or line[i - 1] != "\\"):
                in_string = not in_string
            if not in_string and line[i : i + 2] == "//":
                break
            result += line[i]
            i += 1
        return result

    return "\n".join(remove_line_comments(line) for line in jsonc_str.splitlines())


class Config(SimpleNamespace):
    __slots__ = ("_meta_",)

    def __init__(self, source=None, io_params={}, loader_params={}):
        super().__init__()

        io_params = {"encoding": "utf-8", **io_params}

        meta = {"io_params": io_params}

        data = {}
        if source:
            if isinstance(source, dict):
                data = source
            elif isinstance(source, str):
                if os.path.isfile(source) and os.path.exists(source):
                    with open(source, "r", **io_params) as f:
                        meta["source_path"] = source
                        source = f.read()
                source = _jsonc_to_json(source)
                data = json.loads(source, **loader_params)
            else:
                raise RootConfigTypeError(source)

        object.__setattr__(self, "_meta_", meta)

        self.update(**data)

    def __contains__(self, key):
        return key in self.__dict__

    def __len__(self):
        return len(self.__dict__)

    def __iter__(self):
        return iter(self.__dict__)

    def __str__(self):
        return json.dumps(self.to_dict(), indent=4, ensure_ascii=False, default=str)

    def __reduce__(self):
        return (self.__class__, (), self.__dict__)

    def __bool__(self):
        return bool(self.__dict__)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __delitem__(self, key):
        del self.__dict__[key]

    def __setitem__(self, key, value):
        if key in _locked_methods:
            raise LockedMethodError(key)
        self.__dict__[key] = _to_config(value, self._meta_["io_params"])

    def __repr__(self):
        string = "<empty>"
        keys = list(self.keys())
        if len(keys) == 1:
            string = f'{{"{keys[0]}": ... }}'
        elif len(keys) > 1:
            string = f'{{"{keys[0]}": ..., ... }}'
        return f"{self.__class__.__name__}({string})"

    def __or__(self, other):
        result = self.copy()
        result.update(other)
        return result

    def __ior__(self, other):
        self.update(other)
        return self

    __setattr__ = __setitem__

    def to_dict(self):
        return _to_dict(self)

    def keys(self):
        return self.__dict__.keys()

    def values(self):
        return self.__dict__.values()

    def items(self):
        return self.__dict__.items()

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def pop(self, key, *args):
        return self.__dict__.pop(key, *args)

    def popitem(self):
        return self.__dict__.popitem()

    def clear(self):
        self.__dict__.clear()

    def copy(self):
        return copy.deepcopy(self)

    def update(self, *args, **kwargs):
        for k, v in dict(args[0] if len(args) else {}, **kwargs).items():
            self[k] = v

    def save(self, source_path=None, **dumper_params):
        if not source_path:
            source_path = self._meta_.get("source_path")
            if not source_path:
                raise SourcePathError()

        dumper_params = {"ensure_ascii": False, **dumper_params}

        with open(source_path, "w", **self._meta_["io_params"]) as f:
            json.dump(self.to_dict(), f, **dumper_params)
