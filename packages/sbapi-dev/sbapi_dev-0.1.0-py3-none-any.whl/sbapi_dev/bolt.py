from .base import ServeboltBaseAPI
from .exceptions import ServeboltAPIError
from concurrent.futures import ThreadPoolExecutor
from rich import print_json

class ServeboltBoltAPI(ServeboltBaseAPI):
    def _get_bolt_page(self, page, admin = False):
        admin_url = '/admin' if admin else ''
        resp = self.get(f'{admin_url}/bolts?page={page}')
        if not resp.ok:
            raise ServeboltAPIError(f"Coudn't fetch Bolt page={page}: {resp.text}")

        data = resp.json()
        return data

    def __get_last_bolt_page(self, admin = False):
        admin_url = '/admin' if admin else ''
        resp = self.get(admin_url + '/bolts')

        if not resp.ok:
            raise ServeboltAPIError(f"Coudn't fetch last Bolt page: {resp.text}")

        return resp.json()['meta']['last_page']

    def get_bolts(self, admin = False):
        last_page = self.__get_last_bolt_page(admin)

        with ThreadPoolExecutor() as executor:
            pages = executor.map(lambda page: self._get_bolt_page(page, admin), range(1, last_page + 1))

        bolts = [bolt for page in pages for bolt in page['data']]
        return bolts

    def list_bolts(self, admin = False):
        print_json(data=self.get_bolts(admin))
