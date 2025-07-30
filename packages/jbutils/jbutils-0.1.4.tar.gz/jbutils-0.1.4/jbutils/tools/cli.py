"""CLI Testing tool for checking local functionality"""

import json
import os

from ptpython import embed

from jbutils.utils.config import Configurator
from jbutils import jbutils

# from .config import Configurator
sample_files_2 = {
    "common": {
        "tools": {
            "test1.json": {"a": 5, "b": "b", "c": {"c1": 1, "c2": False}},
            "test2.yaml": {"a": 10, "b": "B", "c": [{"c1": 2, "c2": True}]},
        }
    },
    "init.yaml": {"a": 15, "b": "test", "c": {"c1": 3, "c2": "true"}},
}


def main() -> None:
    embed(
        globals=globals(), locals=locals(), history_filename="jbutils_cli.history"
    )


if __name__ == "__main__":
    main()
