# gd_browser/__init__.py

from .http import HTTPClient
from .format import print_json, print_readable
from .ext.songs import SongsAPI
from .ext.players import PlayersAPI
from .ext.levels import LevelsAPI
from .ext.search import SearchAPI

class GDBrowser:
    def __init__(self):
        self.client = HTTPClient("https://gdbrowser.com/api")
        self.songs = SongsAPI(self.client)
        self.players = PlayersAPI(self.client)
        self.levels = LevelsAPI(self.client)
        self.search = SearchAPI(self.client)

    print_json = staticmethod(print_json)
    print_readable = staticmethod(print_readable)
