# Configureout
A lightweight and flexible configuration loader for Python. Supports loading configuration from dicts, JSON/JSONC strings, or files, with namespace-style access.

## Features
- Load config from dict, JSON string, or file
- Automatically converts nested structures to `Config`
- Modify, save, and update configurations easily
- Dictionary-style and attribute-style access

## Installation
You can install configureout via pip:
```bash
pip install configureout
```
Or just `configureout.py` in your project.

## Usage
```python
from configureout import Config

# Load from file
cfg = Config('config.json')
print(cfg.get('debug')) # True

# Or load from dict
cfg = Config({'debug': True, 'db': {'host': 'localhost', 'port': 8000}})
print(cfg.db.host) # localhost

# Or load from JSON string
cfg = Config('{"debug": true, "db": {"host": "localhost", "port": 8000}}')
print(cfg['db']['port']) # 8000
```

## Public Methods
```python
# Converts the internal namespace config to a standard Python dictionary.
to_dict()

# Saves the current configuration to a JSON file. (Attribute "config_path" is required for non-file configs or nested objects.)
save(config_path=None, **kwargs)

# Updates the configuration with new values (from dict or keyword args).
update(other=None, **kwargs) 

# Removes all nested elements from config.
clear()

# Returns a copy of the current configuration.
copy()

# Standard dictionary-style access methods.
keys() / values() / items() / get(key, default=None) / pop(key) / popitem()
```


## Magic Methods
```python
__getitem__(key) / __setitem__(key, value) # Enables dict-style access: cfg['key'].
__delitem__(key) # Deletes a config attribute.
__contains__(key) # Checks if key exists using 'key' in cfg.
__len__() # Returns the number of keys.
__iter__() # Enables iteration over keys.
__str__() # Returns a formatted JSON string of the config.
__repr__() # Developer-friendly representation of the config.
__bool__() # Returns False if the config is empty.
__eq__(other) # Compares config with another Config or dict.
__or__(other) / __ior__(other) # Merge configs using | and |= operators.
__reduce__() # Supports pickling.
```

## Restrictions
Attempting to override public methods will raise an error:
```python
cfg.update = "not allowed"  # Raises LockedMethodError
```

## Python Version
Python 3.9+ is required.

## License
MIT License