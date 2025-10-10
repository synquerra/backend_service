import hmac
import hashlib
import time
from app.config.config import settings
from app.config.AuthCredentials import APAARClientsAuth


class HMACAuth:
    def __init__(self, client_id: str):
        self.client_id = client_id
        self.client_secret = APAARClientsAuth.get_secret_by_client_id(client_id)
        self.server_ts = int(time.time())
        self.hmac_valid_ts = int(settings.HMAC_VALID_TS)
        self.hmac_valid_future_ts = int(settings.HMAC_VALID_FUTURE_TS)

    def generate_signature(self, requested_dict: dict, client_ts: int) -> str:
        dict_values = ''.join(str(requested_dict[key]) for key in requested_dict)
        message = self.client_secret + self.client_id + dict_values + str(client_ts)
        signature = hashlib.sha256(message.encode('utf-8')).hexdigest()
        return signature

    def verify_signature(self, received_hmac: str, requested_dict: dict, client_ts: int) -> tuple[bool, str]:
        try:
            client_ts = int(client_ts)
        except ValueError:
            return False, 'Invalid client timestamp'

        if client_ts < self.server_ts - self.hmac_valid_ts:
            return False, 'HMAC timestamp is too old (older than 10 minutes)'
        elif client_ts > self.server_ts + self.hmac_valid_future_ts:
            return False, 'HMAC timestamp is too far in the future (possible clock skew)'

        expected_hmac = self.generate_signature(requested_dict, client_ts)

        if not hmac.compare_digest(expected_hmac, received_hmac):
            return False, 'HMAC signature does not match'

        return True, 'HMAC signature is valid'
