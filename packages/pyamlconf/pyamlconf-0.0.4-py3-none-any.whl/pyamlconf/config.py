import re
from typing import Union, Optional

import yaml

# ${var}
mustache_p = re.compile(r"(\{\{ *[a-zA-Z0-9\.\-_]*? *\}\})")


class PyamlConfig:
    config_file: str
    __config: dict

    def __init__(self, config_file: str, encoding: str = 'utf-8'):
        """
        build a yaml file to pymalconfig object
        :param config_file: a yaml file
        """
        self.__config = {}
        self.config_file = config_file
        with open(config_file, 'r', encoding=encoding) as f:
            self.__config = yaml.safe_load(f)

    @staticmethod
    def __deep_merge(dict1: dict, dict2: dict, merge: bool):
        result = dict1.copy()
        for key, value in dict2.items():
            if not merge and not result.__contains__(key):
                continue
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = PyamlConfig.__deep_merge(result[key], value, merge)
            else:
                result[key] = value
        return result

    def update(self, config: 'PyamlConfig', merge: bool = False):
        """
        update with another config
        :param config: PyamlConfig
        :param merge: True: merge all key; False: update exists key
        """
        self.__config = PyamlConfig.__deep_merge(self.__config, config.__config, merge)

    def get(self, key: str, default_value=None) -> (Union[str, int, float, bool, list, dict]):
        """
        get a value from config
        :param key: get value by this key, like: db.name
        :param default_value: if db.name have no value, then return default_value
        :return: str | int | float | bool | list | dict
        """
        keys = key.split(".")
        i = 0
        c = self.__config
        while i < len(keys) and c is not None:
            c = c.get(keys[i])
            i += 1

        c = c if c is not None else default_value

        if c is not None and isinstance(c, str):
            ss = mustache_p.findall(c)
            if ss is not None:
                for s in ss:
                    k = s[2:-2].strip()
                    if k.startswith('.'):
                        dot_count = 0
                        while k.startswith('.'):
                            k = k[1:]
                            dot_count += 1
                        if dot_count < len(keys):
                            k = ".".join(keys[:- dot_count]) + "." + k
                    v = self.get(k)
                    c = c.replace(s, "" if v is None else str(v))

        return c

    def get_str(self, key: str, default_value: str = None) -> Optional[str]:
        """
        get a str from config
        """
        val = self.get(key)
        return default_value if val is None else str(val)

    def get_int(self, key: str, default_value: int = None) -> Optional[int]:
        """
        get a int from config
        """
        val = self.get(key)
        return default_value if val is None else int(val)

    def get_float(self, key: str, default_value: float = None) -> Optional[float]:
        """
        get a float from config
        """
        val = self.get(key)
        return default_value if val is None else float(val)

    def get_bool(self, key: str, default_value: bool = None) -> Optional[bool]:
        """
        get a bool value from config
        """
        val = self.get(key)
        return default_value if val is None else bool(val)

    def get_list(self, key: str, default_value: list = None) -> Optional[list]:
        """
        get a list from config
        """
        val = self.get(key)
        return default_value if val is None else list(val)

    def get_tuple(self, key: str, default_value: tuple = None) -> Optional[tuple]:
        """
        get a tuple from config
        """
        val = self.get(key)
        return default_value if val is None else tuple(val)

    def get_set(self, key: str, default_value: set = None) -> Optional[set]:
        """
        get a set from config
        """
        val = self.get(key)
        return default_value if val is None else set(val)
