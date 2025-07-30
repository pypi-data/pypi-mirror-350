__version__ = "0.0.5"
from database import Database

class envypy:
    def __init__(self, api_url, api_key=None):
        self.database = Database(api_url, api_key)
