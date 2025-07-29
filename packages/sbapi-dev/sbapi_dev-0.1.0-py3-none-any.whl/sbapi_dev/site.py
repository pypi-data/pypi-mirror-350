from .bolt import ServeboltBoltAPI
from rich import print_json

class ServeboltSiteAPI:
    def __init__(self, session, base_url):
        self.bolt = ServeboltBoltAPI(session, base_url)

    def get_sites(self, admin = False):
        bolts = self.bolt.get_bolts(admin)
        sites = [site for bolt in bolts for site in bolt['relationships']['environments']]
        return sites

    def list_sites(self, admin = False):
        print_json(data=self.get_sites(admin))

    def find_site(self, site_id, admin = False):
        sites = self.get_sites(admin)

        site = [site for site in sites if site['attributes']['internalName'] == site_id]
        return site
