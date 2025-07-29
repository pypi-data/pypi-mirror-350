from requests import Session

class ServeboltBaseAPI:
    def __init__(self, session: Session, base_url: str):
        self.session = session
        self.base_url = base_url.rstrip("/")

    def get(self, path, **kwargs):
        return self.session.get(self.base_url + path, **kwargs)

    def post(self, path, **kwargs):
        return self.session.post(self.base_url + path, **kwargs)

    def put(self, path, **kwargs):
        return self.session.put(self.base_url + path, **kwargs)

    def patch(self, path, **kwargs):
        return self.session.patch(self.base_url + path, **kwargs)

    def delete(self, path, **kwargs):
        return self.session.delete(self.base_url + path, **kwargs)
