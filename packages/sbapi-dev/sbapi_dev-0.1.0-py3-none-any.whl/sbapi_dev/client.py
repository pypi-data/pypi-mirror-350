from requests import Session
from .auth import ServeboltAuthAPI
from .bolt import ServeboltBoltAPI
from .site import ServeboltSiteAPI
from .database import ServeboltDatabaseAPI
from .find import ServeboltFindAPI

class ServeboltClient:
    def __init__(self, base_url = "https://api.servebolt.io/v1"):
        self.session = Session()
        self.base_url = base_url.rstrip("/")

        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

        self.auth = ServeboltAuthAPI(self.session, self.base_url)
        self.bolt = ServeboltBoltAPI(self.session, self.base_url)
        self.site = ServeboltSiteAPI(self.session, self.base_url)
        self.database = ServeboltDatabaseAPI(self.session, self.base_url)
        self.find = ServeboltFindAPI(self.session, self.base_url,)
