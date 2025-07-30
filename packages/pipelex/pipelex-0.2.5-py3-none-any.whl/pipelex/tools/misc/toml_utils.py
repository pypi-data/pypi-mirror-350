from typing import Any, Dict, Optional

import toml

from pipelex.tools.misc.file_utils import path_exists


def load_toml_from_path(path: str) -> Dict[str, Any]:
    with open(path) as file:
        dict_from_toml = toml.load(file)
        return dict_from_toml


def failable_load_toml_from_path(path: str) -> Optional[Dict[str, Any]]:
    if not path_exists(path):
        return None
    return load_toml_from_path(path)
