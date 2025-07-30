"""General utility for reading/parsing config files"""

import os
import platform


from dataclasses import dataclass, field
from typing import Any, TypeVar

from platformdirs import user_config_dir

from jbutils.utils import utils

T = TypeVar("T")

sample_files_1 = {
    "common/tools/test.json": {"a": 5, "b": "b", "c": {"c1": 1, "c2": False}},
    "common/tools/test.yaml": {"a": 10, "b": "B", "c": [{"c1": 2, "c2": True}]},
    "init.yaml": {"a": 15, "b": "test", "c": {"c1": 3, "c2": "true"}},
}

sample_files_2 = {
    "common": {
        "tools": {
            "test.json": {"a": 5, "b": "b", "c": {"c1": 1, "c2": False}},
            "test.yaml": {"a": 10, "b": "B", "c": [{"c1": 2, "c2": True}]},
        }
    },
    "init.yaml": {"a": 15, "b": "test", "c": {"c1": 3, "c2": "true"}},
}


@dataclass
class Configurator:
    app_name: str = ""
    cfg_dir: str = ""
    author: str = ""
    version: str = ""

    platform: str = platform.platform()
    sep: str = "/"

    files: list[str] | dict[str, str] = field(default_factory=list)

    roaming: bool = False
    ensure_exists: bool = True
    use_default_path: bool = True
    trim_key_exts: bool = True
    reset_cfgs: bool = False

    _data: dict = field(default_factory=dict)
    _path_map: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.cfg_dir = self.cfg_dir or self._get_cfg_dir()
        if self.reset_cfgs:
            self.clear_cfgs()

        if self.platform == "Windows":
            self.sep = "\\"

        if not os.path.exists(self.cfg_dir):
            # TODO add better error logging/handling here
            print(f"[Warning]: {self.cfg_dir} does not exist")
            return

        if isinstance(self.files, list):
            for file_name in self.files:
                fpath = os.path.join(self.cfg_dir, file_name)
                self._set_file_data(fpath, {})
                # self._data[file_name] = utils.read_file(fpath)
        elif isinstance(self.files, dict):
            for key, value in self.files.items():
                self._get_files_dict(key, value)

    def get(self, key: list[str] | str, default: Any = None) -> Any:
        if isinstance(key, str) and not self.trim_key_exts:
            key = key.split(".")
            if len(key) >= 2:
                ext = key.pop()
                fname = key.pop()
                key.append(f"{fname}{ext}")
        return utils.get_nested(self._data, key, default_val=default)

    def set(self, key: str | list[str], value: Any) -> None:
        utils.set_nested(self._data, key, value)

        key_path = self.get_path_from_key(key)
        if key_path:
            filepath = self._path_map[tuple(key_path)]
            data = self.get(key_path)
            utils.write_file(filepath, data)

    def get_path_from_key(self, key: str | list[str]) -> list[str]:
        path = key.split(".") if isinstance(key, str) else key
        while path:
            if tuple(path) in self._path_map:
                return path
            path.pop()
        return []

    def get_as_class(
        self, cls: type[T], path: str | list[str], default: Any = None
    ) -> T:
        default = default or {}
        data = self.get(path, default)
        return cls(**data)

    def clear_cfgs(self) -> None:
        self._data = {}
        self._path_map = {}
        if os.path.exists(self.cfg_dir):
            os.removedirs(self.cfg_dir)

    def _set_file_data(self, path: str, default: dict = None) -> None:
        default = default or {}
        # root_path = os.path.join(root_path, filename)

        if not os.path.exists(path) and self.ensure_exists:
            utils.write_file(path, default)
            data = default
        else:
            data = utils.read_file(path, default_val=default)

        root = os.path.commonpath([path, self.cfg_dir])

        data_path = utils.split_path(
            path.replace(root, ""), keep_ext=not self.trim_key_exts
        )
        self._path_map[tuple(data_path)] = path
        utils.set_nested(self._data, data_path, data)

    def _get_files_dict(self, prop_key: str, prop: Any, path: list[str] = None):
        path = path + [prop_key] if path else [prop_key]
        path_str = os.path.join(self.cfg_dir, self.sep.join(path))

        if not utils.get_ext(prop_key):
            os.makedirs(path_str, exist_ok=True)
            if isinstance(prop, dict):
                for key, value in prop.items():
                    self._get_files_dict(key, value, path)
            elif isinstance(prop, list):
                for item in prop:
                    self._set_file_data(path_str, item)
        else:
            self._set_file_data(path_str, prop)

    def _get_cfg_dir(self) -> str:
        return user_config_dir(
            self.app_name,
            self.author,
            self.version,
            self.roaming,
            self.ensure_exists,
        )
