# gd_browser/http.py 

import requests
from typing import Union

class HTTPClient:
    def __init__(self, base_url: str):
        self.api = base_url
        self.headers = {
            "server": "nginx/1.14.0 (Ubuntu)",
            "content-type": "application/json; charset=utf-8",
            "connection": "keep-alive"
        }

    def get(self, endpoint: str) -> Union[dict, list, str]:
        response = requests.get(f"{self.api}/{endpoint}", headers=self.headers)
        try:
            return response.json()
        except ValueError:
            return response.text
