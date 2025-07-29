#Built-in Modules
import hashlib



HMAC_DIGEST_MOD = hashlib.sha512

DATETIME_FMT_MSG_TO_SIGN = '%d-%b-%y'  # Today (DD-MMM-YY)


class LoginAPI:
    URL: str = 'https://login.quantsapp.com/api_login'
    TIMEOUT: int = 5
    MODE: str = 'api_login'