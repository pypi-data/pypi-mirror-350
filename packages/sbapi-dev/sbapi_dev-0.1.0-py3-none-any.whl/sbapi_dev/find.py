from .bolt import ServeboltBoltAPI
from rich import print_json

class ServeboltFindAPI:
    def __init__(self, session, base_url):
        self.bolt = ServeboltBoltAPI(session, base_url)

    def find_site_and_db(self, site_id, admin=False):
        bolts = self.bolt.get_bolts(admin)
    
        for bolt in bolts:
            environments = bolt.get("relationships", {}).get("environments", [])
            databases = bolt.get("relationships", {}).get("databases", [])
    
            for env in environments:
                env_id = env.get("id")
                env_attrs = env.get("attributes", {})
                internal_name = env_attrs.get("internalName")
                hostname = env_attrs.get("hostname")
    
                if internal_name == site_id:
                    # Found the matching environment — now look for its database
                    for db in databases:
                        db_attrs = db.get("attributes", {})
                        db_name = db_attrs.get("dbName")
                        db_envs = db_attrs.get("environments", [])
    
                        for db_env in db_envs:
                            if str(db_env.get("id")) == str(env_id):
                                return {
                                    "internalName": internal_name,
                                    "dbName": db_name,
                                    "hostname": hostname
                                }
    
        return {}  # Nothing found






