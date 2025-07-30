"""Collection of common utils functions for personal repeated use"""

import csv
import json
import os
import shlex
import subprocess
import traceback

from platform import platform

from ruamel.yaml import YAML
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Literal

from ruamel.yaml.comments import CommentedMap, CommentedSeq

yaml = YAML()
yaml.indent = 2


class Consts:
    encoding: str = "UTF-8"


SubReturn = Literal["out", "err", "both"]
""" String literal type representing the output choices for cmdx """


# pylint: disable=C0103
@dataclass
class SubReturns:
    """Enum class for SubReturn values"""

    OUT: SubReturn = "out"
    ERR: SubReturn = "err"
    BOTH: SubReturn = "both"


# pylint: enable=C0103


def set_encoding(enc: str) -> None:
    Consts.encoding = enc


def set_yaml_indent(indent: int) -> None:
    yaml.indent = 2


def read_file(
    path: str,
    mode: str = "r",
    encoding: str = Consts.encoding,
    as_lines: bool = False,
    default_val: Any = None,
    as_dicts: bool = False,
) -> str | dict | list:
    """Read data from a file

    Args:
        path (str): The path to the file
        mode (str, optional): IO mode to use. Defaults to "r".
        encoding (str, optional): Encoding format to use.
            Defaults to "latin-1".
        as_lines (bool, optional): If reading a regular text file,
            True will return the value of readlines() instead of read().
            Defaults to False.
        default_val (Any, optional): Value to return if the file is not found.
            Defaults to None.

    Returns:
        str | dict | list: The data read from the file. If the file is
            not found, returns an empty dict
    """

    default_val = default_val or {}

    if not os.path.exists(path):
        print(f"Warning: Path '{path}' does not exist")
        return default_val

    _, ext = os.path.splitext(path)

    with open(path, mode, encoding=encoding) as fs:
        match ext.lower():
            case ".yaml" | ".yml":
                return yaml.load(stream=fs)
            case ".json":
                return json.load(fs)
            case ".csv":
                data = list(csv.reader(fs))
                if as_dicts:
                    if not data:
                        return []

                    cols = data.pop(0)

                    if not data:
                        return []

                    return [dict(zip(cols, vals)) for vals in data]
                return data
            case _:
                if as_lines:
                    return fs.readlines()
                else:
                    return fs.read()


def write_file(
    path: str,
    data: Any,
    mode: str = "w",
    encoding: str = Consts.encoding,
    indent: int = 4,
) -> None:
    """Write text to a file

    Args:
        path (str): The path to the file
        data (Any): The data to write
        mode (str, optional): Read/write mode. Defaults to "w".
        encoding (str, optional): Encoding to write with. Defaults to ENCODING.
        indent (int, optional): Indent to apply if JSON. Defaults to 4.
        sort_keys (bool, optional): Whether to sort the output keys for YAML.
            Defaults to False.
    """

    _, ext = os.path.splitext(path)

    with open(path, mode, encoding=encoding) as fs:
        match ext.lower():
            case ".yml" | ".yaml":
                yaml.dump(data, fs)
            case ".json":
                json.dump(data, fs, indent=indent)
            case _:
                if isinstance(data, list):
                    fs.writelines(data)
                else:
                    fs.write(data)


def get_ext(path: str) -> str:
    """Get the file extension from a path

    Args:
        path (str): The path to the file

    Returns:
        str: The file extension including the dot, or an empty string if no extension exists
    """

    return os.path.splitext(path)[1]


def strip_ext(path: str) -> str:
    """Get the file name without the extension from a path

    Args:
        path (str): The path to the file

    Returns:
        str: The file name without the extension, or an empty string if no name exists
    """

    return os.path.splitext(os.path.basename(path))[0]


def get_os_sep() -> str:
    if platform() == "Windows":
        return "\\"
    else:
        return "/"


def split_path(path: str, keep_ext: bool = True) -> list[str]:
    path_split = []
    head, tail = os.path.split(path)
    if not tail:
        return [head.replace(get_os_sep(), "")]

    if not keep_ext:
        tail = strip_ext(tail)

    path_split.append(tail)
    max_depth = 32
    count = 0
    while tail and count < max_depth:
        head, tail = os.path.split(head)
        if tail:
            path_split.insert(0, tail)
        count += 1
    return path_split


def find(items: list, value: Any) -> int:
    """A 'not in list' safe version of list.index()

    Args:
        items (list): List to search
        value (Any): Value to search for

    Returns:
        int: Index of the first instance of value, or -1 if not found
    """

    try:
        return items.index(value)
    except ValueError:
        return -1


def update_list_values(
    items: list[Any],
    new_items: list[Any],
    sort: bool = False,
    sort_func: Callable[[Any], bool] = None,
    reverse: bool = False,
) -> list[Any]:
    """Add new items to a list and sort it

    Args:
        items (list[Any]): Items to add to
        new_items (list[Any]): Items to add
        sort (Callable[[Any], bool], optional): Custom sort function. Defaults to None.
        reverse (bool, optional): If true, sort order is reversed. Defaults to False.

    Returns:
        list[Any]: The updated list
    """

    for item in new_items:
        if item not in items:
            items.append(item)

    if sort:
        if sort_func:
            items.sort(key=sort_func, reverse=reverse)
        else:
            items.sort(reverse=reverse)

    return items


def remove_list_values(
    items: list[Any],
    del_items: list[Any],
    sort: bool = False,
    sort_func: Callable[[Any], bool] = None,
    reverse: bool = False,
) -> list[Any]:
    """Remove items from a list and sort it

    Args:
        items (list[Any]): Items to remove from
        del_items (list[Any]): Items to remove
        sort (Callable[[Any], bool], optional): Custom sort function. Defaults to None.
        reverse (bool, optional): If true, sort order is reversed. Defaults to False.

    Returns:
        list[Any]: The updated list
    """

    for item in del_items:
        if item in items:
            items.remove(item)
    if sort:
        if sort_func:
            items.sort(key=sort_func, reverse=reverse)
        else:
            items.sort(reverse=reverse)

    return items


def _get_nested(obj: dict, path: str | list, default=None):
    """
    Retrieves a nested property from a dictionary.

    Args:
        dict (dict): The dictionary instance to retrieve the property from.
        path (str | list[str]): The path to the desired property. Can be a dot-separated string or a list of strings.
        default (any, optional): The value to return if the property cannot be found. Defaults to None.

    Returns:
        any: The value at the specified path, or the default value if not found.
    """
    # Convert the path to a list if it's a string
    if isinstance(path, str):
        path = path.split(".")

    current_value = obj

    for key in path:
        try:
            current_value = current_value[key]
        except (KeyError, TypeError):
            return default

    return current_value


def _set_nested(obj: dict, path: str | list[str], value: Any):
    """Sets a nested property in a dictionary.

    Args:
        obj (dict): The dictionary instance to update.
        path (str or list of str): The path to the desired property. Can be a dot-separated string or a list of strings.
        value: The value to set at the specified path.

    Returns:
        None
    """
    # Convert the path to a list if it's a string
    if isinstance(path, str):
        path = path.split(".")

    current_value = obj

    for key in path[:-1]:
        try:
            current_value = current_value[key]
        except KeyError:
            current_value[key] = {}
            current_value = current_value[key]

    # Set the final value
    current_value[path[-1]] = value


def print_stack_trace():
    # Get the current stack frame
    stack = traceback.format_stack()

    print("\n".join(stack[:-2]))


def copy_to_clipboard(text):
    process = subprocess.Popen(
        ["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE
    )
    process.communicate(input=text.encode("utf-8"))


def dedupe_list(items: list) -> list:
    new_list = []
    for item in items:
        if item not in new_list:
            new_list.append(item)
    return new_list


def dedupe_in_place(items: list) -> list:
    uniques = []
    dupes = []

    for item in items:
        if item not in uniques:
            uniques.append(item)
        else:
            dupes.append(item)

    for item in dupes:
        items.remove(item)

    return dupes


def get_keys(obj: dict, keys: list[str] = None) -> Any:
    if not isinstance(obj, dict):
        return keys

    keys = keys or []
    keys.extend(obj.keys())
    for value in obj.values():
        get_keys(value, keys)

    return keys


def get_nested(
    obj: dict | list, path: list[str] | str, default_val: Any = None
) -> Any:
    """Get a nested value from a dictionary or list

    Args:
        obj (dict | list): The object to get the value from
        path (list[str] | str): The path to the value
        default_val (Any, optional): The default value to return if the path is not found.
            Defaults to None.

    Returns:
        Any: The value at the path or the default value
    """

    if isinstance(path, str):
        path = path.split(".")

    if len(path) == 1:
        result = None
        if isinstance(obj, dict):
            result = obj.get(path[0], default_val)

        elif isinstance(obj, list) and path[0].isdigit():
            idx = int(path[0])
            item = None
            if idx < len(obj):
                item = obj[idx]
            if item is None:
                item = default_val

            result = item
        return result

    key = path.pop(0)
    if isinstance(obj, list) and key.isdigit():
        if int(key) < len(obj):
            return get_nested(obj[int(key)], path, default_val)
        return default_val
    if key not in obj:
        return default_val
    return get_nested(obj[key], path, default_val)


def delete_nested(obj: dict | list, path: list[str] | str) -> None:
    """Delete a nested value from a dictionary or list

    Args:
        obj (dict | list): The object to delete the value from
        path (list[str] | str): The path to the value
    """

    if isinstance(path, str):
        path = path.split(".")

    if len(path) == 1:
        print(obj)
        if isinstance(obj, (dict, CommentedMap)):
            obj.pop(path[0], None)
        elif isinstance(obj, (list, CommentedSeq)):
            if path[0].isdigit():
                idx = int(path[0])
                if idx < len(obj):
                    obj.pop(idx)
            elif path[0] in obj:
                print("removing", path[0])
                obj.remove(path[0])
    else:
        key = path.pop(0)
        if isinstance(obj, list) and key.isdigit():
            if int(key) < len(obj):
                delete_nested(obj[int(key)], path)
        elif key in obj:
            delete_nested(obj[key], path)


def debug_print(*args):
    """Print debug statements with a newline before and after"""

    strings = list(args)
    strings.insert(0, "\n")
    strings.append("\n")
    print(*strings)


def pretty_print(obj: any) -> None:
    """Prints a JSON serializable object with indentation"""

    print(json.dumps(obj, indent=4))


@dataclass
class SetNestedOptions:
    """Options for the set_nested function"""

    def __init__(self, debug: bool = False, create_lists: bool = False) -> None:

        self.debug: bool = debug
        self.create_lists: bool = create_lists


def _set_next_append(
    obj: list,
    path: list[str],
    key: str | int,
    value: Any,
    debug: bool = False,
    create_lists: bool = True,
) -> None:
    """Set a value in a nested object when the index is out of bounds

    Args:
        obj (list): Object to set the value in
        path (list[str]): Path to the value
        key (str | int): Key to set the value at
        value (Any): Value to set
        debug (bool, optional): Flag to enable debug statements. Defaults to False.
        create_lists (bool, optional): Flag to set whether to create a list or. Defaults to True.
    """
    if debug:
        debug_print("out of bounds", "inserting new value", f"path[0] = {path[0]}")

    if path[0].isdigit() and create_lists:
        obj.insert(int(key), [])
    else:
        obj.insert(int(key), {})

    if debug:
        debug_print("blank inserted", obj)

    set_nested(
        obj=obj[-1], path=path, value=value, debug=debug, create_lists=create_lists
    )


def _set_next_list_item(
    obj: list,
    path: list[str],
    key: str | int,
    value: Any,
    debug: bool = False,
    create_lists: bool = True,
) -> None:
    """Iterate through the next item in a list or dictionary

    Args:
        obj (list): Object to set the value in
        path (list[str]): Path to the value
        key (str | int): Key to set the value at
        value (Any): Value to set
        debug (bool, optional): Flag to enable debug statements. Defaults to False.
        create_lists (bool, optional): Flag to set whether to create a list or. Defaults to True.
    """

    sub = obj[int(key)]
    if not sub or not isinstance(sub, (dict, list)):
        if debug:
            debug_print("sub is None or not an object", "creating new sub")

        if path[0].isdigit() and create_lists:
            obj[int(key)] = []
        else:
            obj[int(key)] = {}

    set_nested(
        obj=obj[int(key)],
        path=path,
        value=value,
        debug=debug,
        create_lists=create_lists,
    )


def _set_final_prop(obj: dict | list, path: list[str], value: Any) -> None:
    """Set a value in a nested object at the final path

    Args:
        obj (dict | list): Object to set the value in
        path (list[str]): Path to the value
        value (Any): Value to set
    """

    if isinstance(obj, dict):
        obj[path[0]] = value
    elif isinstance(obj, list) and path[0].isdigit():
        if int(path[0]) < len(obj):
            obj[int(path[0])] = value
        else:
            obj.append(value)


def _set_next_nested(
    obj: dict | list,
    path: list[str],
    value: Any,
    key: str | int,
    debug: bool = False,
    create_lists: bool = True,
) -> None:
    """Set a value in a nested object

    Args:
        obj (dict | list): Object to set the value in
        path (list[str]): Path to the value
        value (Any): Value to set
        key (str | int): Key to set the value at
        debug (bool, optional): Flag to enable debug statements. Defaults to False.
        create_lists (bool, optional): Flag to set whether to create a list or. Defaults to True.
    """

    sub = obj.get(key)

    if debug:
        debug_print("obj is dict", "sub:", sub)

    if not sub or not isinstance(sub, (dict, list)):
        if debug:
            debug_print("sub is None or not an object", "creating new sub")

        if path[0].isdigit() and create_lists:
            obj[key] = []
        else:
            obj[key] = {}

        if debug:
            debug_print("new sub created", obj)

    set_nested(
        obj=obj.get(key),
        path=path,
        value=value,
        debug=debug,
        create_lists=create_lists,
    )


def set_nested(
    obj: dict | list,
    path: list[str] | str,
    value: Any,
    debug: bool = False,
    create_lists: bool = True,
) -> None:
    """Set a nested value in a dictionary or list

    Args:
        obj (dict | list): The object to set the value in
        path (list[str] | str): The path to the value
        value (Any): The value to set
        debug (bool, optional): Flag to enable debug statements. Defaults to False.
        create_lists (bool, optional): Flag to set whether to create a list or
            a dict when the path fragment is a number. Defaults to True.
    """

    if isinstance(path, str):
        path = path.split(".")

    if debug:
        print_stack_trace()
        debug_print("starting function")
        pretty_print({"obj": obj, "path": path, "value": value})

    if len(path) == 1:
        _set_final_prop(obj, path, value)
    else:
        key = path.pop(0)

        if debug:
            debug_print("key", key)

        if isinstance(obj, list) and key.isdigit():  # true
            if debug:
                debug_print("obj is list", "key < len", int(key) < len(obj))

            if int(key) < len(obj):
                _set_next_list_item(
                    obj=obj,
                    path=path,
                    key=key,
                    value=value,
                    debug=debug,
                    create_lists=create_lists,
                )
            else:
                _set_next_append(
                    obj=obj,
                    path=path,
                    key=key,
                    value=value,
                    debug=debug,
                    create_lists=create_lists,
                )
        elif isinstance(obj, dict):
            _set_next_nested(
                obj=obj,
                path=path,
                value=value,
                key=key,
                debug=debug,
                create_lists=create_lists,
            )


def cmdx(
    cmd: list[str] | str, rtrn: SubReturn = "out", print_out: bool = True
) -> str | tuple[str, str]:
    """Executes a command and returns the output or error

    Args:
        cmd (list[str] | str): - A list of strings that make up the command or a string
            that will be split by spaces
        rtrn (SubReturn, optional): What outputs to return. If both, it will return a
            tuple of (stdout, stderr)Defaults to 'out'.

    Returns:
        str | tuple[str, str]: The output of the command or a tuple of (stdout, stderr)
    """

    if isinstance(cmd, str):
        cmd = shlex.split(cmd)

    try:
        process = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            check=True,
        )
    except subprocess.CalledProcessError as e:
        # Print and handle the errors here if needed
        process = e

    stdout = process.stdout
    stderr = process.stderr
    if print_out:
        if stdout:
            print(stdout)
        if stderr:
            print("\nERROR:\n", stderr)

    if rtrn == "out":
        return process.stdout
    if rtrn == "err":
        return process.stderr

    return process.stdout, process.stderr
