from .base import ServeboltBaseAPI
from .exceptions import ServeboltAPIError

class ServeboltAuthAPI(ServeboltBaseAPI):
    def login(self, username, password, otp = None, otp_check = False):
        resp = self.post("/auth/login", json={"username": username, "password": password})
        data = resp.json()

        if not resp.ok:
            if data.get('error') == 'mfa_required':
                mfa_token = data.get('mfa_token')

                if otp is None and otp_check:
                    otp = input("Please provide your OTP code: ")
                else:
                    raise ServeboltAPIError("MFA required and no OTP code provided")

                data = self._mfa_challenge(mfa_token, otp)
            else:
                raise ServeboltAPIError(resp.json().get("message", "Login failed"))

        self.auth_info = data.get('data')
        token = data.get('data').get('access_token')
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        return token

    def _mfa_challenge(self, mfa_token, otp):
        resp = self.post("/auth/mfa/otp", json={"mfa_token": mfa_token, "otp": otp})
        if not resp.ok:
            raise ServeboltAPIError(resp.json().get("message", "MFA failed"))
        return resp.json()
