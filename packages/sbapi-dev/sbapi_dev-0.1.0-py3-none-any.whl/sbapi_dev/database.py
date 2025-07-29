from .bolt import ServeboltBoltAPI
from rich import print_json

class ServeboltDatabaseAPI:
    def __init__(self, session, base_url):
        self.bolt = ServeboltBoltAPI(session, base_url)

    def get_dbs(self, admin = False):
        bolts = self.bolt.get_bolts(admin)
        dbs = [db for bolt in bolts for db in bolt['relationships']['databases']]
        return dbs

    def list_dbs(self, admin = False):
        print_json(data=self.get_dbs(admin))

    def find_db(self, database_name, admin = False):
        databases = self.get_dbs(admin)
        db = [db for db in databases if db['attributes']['dbName'] == database_name]
        return db
