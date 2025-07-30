import requests
import json
from typing import Union, Optional

class GDBrowser:
    def __init__(self) -> None:
        self.api: str = "https://gdbrowser.com/api"
        self.headers: dict[str, str] = {
            "server": "nginx/1.14.0 (Ubuntu)",
            "content-type": "application/json; charset=utf-8",
            "connection": "keep-alive"
        }

    def print_json(self, data: Union[dict, list]) -> None:
        print(json.dumps(data, indent=2, ensure_ascii=False))

    def print_readable(self, data: Union[dict, list]) -> None:
        if isinstance(data, list):
            for i, item in enumerate(data, 1):
                print(f"#{i}")
                self.print_readable(item)
                print("-" * 30)
            return

        if not isinstance(data, dict):
            print(data)
            return

        for key, value in data.items():
            if isinstance(value, (dict, list)):
                continue
            print(f"{key}: {value}")

    def _get(self, endpoint: str) -> Union[dict, list, str]:
        response = requests.get(f"{self.api}/{endpoint}", headers=self.headers)
        try:
            return response.json()
        except ValueError:
            return response.text

    def get_level(self, level_id: int, download: bool = False) -> Union[dict, list, str]:
        url = f"level/{level_id}"
        if download:
            url += "?download"
        return self._get(url)

    def get_user_profile(self, username: str) -> Union[dict, list, str]:
        return self._get(f"profile/{username}")

    def search(
        self,
        query: str,
        count: int = 10,
        demon_filter: Optional[int] = None,
        page: int = 0,
        gauntlet: Optional[int] = None,
        type: str = "trending"
    ) -> Union[dict, list, str]:
        params = [f"count={count}", f"type={type}"]
        if demon_filter is not None:
            params.append(f"demonFilter={demon_filter}")
        if page:
            params.append(f"page={page}")
        if gauntlet is not None:
            params.append(f"gauntlet={gauntlet}")
        return self._get(f"search/{query}?" + "&".join(params))

    def get_leaderboard(self, count: int = 100, is_creator: bool = False) -> Union[dict, list, str]:
        url = f"leaderboard?count={count}"
        if is_creator:
            url += "&creator"
        return self._get(url)

    def get_map_packs(self) -> Union[dict, list, str]:
        return self._get("mappacks")

    def get_gauntlets_list(self) -> Union[dict, list, str]:
        return self._get("gauntlets")

    def get_level_leaderboard(self, level_id: int, count: int = 100) -> Union[dict, list, str]:
        return self._get(f"leaderboardLevel/{level_id}?count={count}")

    def get_user_posts(self, user_id: int, page: int = 0, count: int = 10, type: str = "profile") -> Union[dict, list, str]:
        return self._get(f"comments/{user_id}?page={page}&count={count}&type={type}")

    def get_user_comments(self, user_id: int, page: int = 0, count: int = 10, type: str = "commentHistory") -> Union[dict, list, str]:
        return self._get(f"comments/{user_id}?page={page}&count={count}&type={type}")

    def get_level_comments(self, level_id: int, page: int = 0, is_top: bool = False, count: int = 10, type: str = "commentHistory") -> Union[dict, list, str]:
        url = f"comments/{level_id}?page={page}&count={count}&type={type}"
        if is_top:
            url += "&top"
        return self._get(url)

    def check_song_verification(self, song_id: int) -> Union[dict, list, str]:
        return self._get(f"song/{song_id}")

    def analyze_level(self, level_id: int) -> Union[dict, list, str]:
        return self._get(f"analyze/{level_id}")

    def get_user_icon(self, username: str, form: str = "cube", size: str = "auto") -> Union[dict, list, str]:
        return self._get(f"icon/{username}?form={form}&size={size}")
