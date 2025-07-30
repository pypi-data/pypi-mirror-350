# gd_browser/format.py

import json
from typing import Union

def print_json(data: Union[dict, list]) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))

def print_readable(data: Union[dict, list]) -> None:
    if isinstance(data, list):
        for i, item in enumerate(data, 1):
            print(f"#{i}")
            print_readable(item)
            print("-" * 30)
        return

    if not isinstance(data, dict):
        print(data)
        return

    for key, value in data.items():
        if isinstance(value, (dict, list)):
            continue
        print(f"{key}: {value}")
