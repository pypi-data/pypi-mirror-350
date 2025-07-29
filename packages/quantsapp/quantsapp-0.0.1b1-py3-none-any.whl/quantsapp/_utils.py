# Built-in Modules
import json
import uuid
import time
import gzip
import typing
import base64
import pickle
import functools
import datetime as dt
from dataclasses import dataclass


# Local Modules
from quantsapp import _models as generic_models
from quantsapp._logger import qapp_logger
from quantsapp import (
    _config as generic_config,
    exceptions as generic_exceptions,
)

# ----------------------------------------------------------------------------------------------------

# Auto reload, when required
_internal_session_data: generic_models._InternalSessionData_Type = {}  # type: ignore

# ----------------------------------------------------------------------------------------------------

class MarketTimings:

    dt_open: dt.datetime = None # type: ignore
    dt_close: dt.datetime = None # type: ignore
    is_open_today: bool = False

    # TODO add auto reload market timings data every 'n' minutes

    # ---------------------------------------------------------------------------

    @staticmethod
    def is_market_open() -> bool:
        """Return current status whether market open at time of func invoke"""

        if not MarketTimings.is_open_today:
            return False

        if not MarketTimings.dt_open \
                or not MarketTimings.dt_close:
            raise generic_exceptions.LoginNotInitiatedError('Initiate Login to check Market timings')  # TODO change the exception and its error

        return MarketTimings.dt_open <= dt.datetime.now(dt.UTC) <= MarketTimings.dt_close

    # ---------------------------------------------------------------------------

    @staticmethod
    def is_after_market() -> bool:
        """Return current status whether market open at time of func invoke"""

        if not MarketTimings.is_open_today:
            return True

        if not MarketTimings.dt_open \
                or not MarketTimings.dt_close:
            raise generic_exceptions.LoginNotInitiatedError('Initiate Login to check Market timings')  # TODO change the exception and its error

        return dt.datetime.now(dt.UTC) > MarketTimings.dt_close


# ----------------------------------------------------------------------------------------------------

def convert_str_to_datetime(date: str, format: str, timezone: dt.timezone = dt.UTC) -> dt.datetime:
    """Convert the date string based on specific format to the required timezone"""

    return dt.datetime.strptime(
        date,
        format,
    ).replace(
        tzinfo=timezone,
    )

# ----------------------------------------------------------------------------------------------------

@functools.lru_cache()
def get_mac_address() -> str:
    """Retreive the mac address of the connected network interface"""

    # Get the hardware address as a 48-bit positive integer
    mac_num = uuid.getnode()

    # 1. Convert the number to hex
    # 2. Pad it to 12 chars
    # 3. Convert it to a series of two char strings
    # 4. Join them with colons
    # 5. convert to uppercase
    return ':'.join(f"{b:02x}" for b in mac_num.to_bytes(6)).upper()

# ----------------------------------------------------------------------------------------------------

def get_int_or_float(value: str) -> int | float:
    """Parse string to int or float"""

    _float_value = float(value)
    return int(_float_value) if _float_value % 1 == 0 else _float_value

# ----------------------------------------------------------------------------------------------------

def gzip_decompress_response_data(data: str):
    """Base64 decode and Gzip deccompress the data"""

    return json.loads(
        gzip.decompress(
            base64.b64decode(data)
        )
    )

# ----------------------------------------------------------------------------------------------------

def get_local_file_cache_data(file_name: str, is_common_data: bool = False) -> typing.Any:
    """Get the data from local cache file, if available"""

    file_path = generic_config.tmp_cache_folder_path / file_name

    if is_common_data:
        # The common files are not stored in userwise folder
        file_path = generic_config.tmp_cache_folder_path.parent / '_common_data' / file_name
    else:
        file_path = generic_config.tmp_cache_folder_path / file_name

    match file_path.suffix:
        case '.pkl':
            with open(file_path, 'rb') as fp:
                return pickle.load(fp)
        case '.json':
            with open(file_path, 'r') as fp:
                return json.load(fp)
        case _:
            raise ValueError('Invalid File Type')


# ----------------------------------------------------------------------------------------------------

def put_local_file_cache_data(
        file_name: str,
        data: typing.Any,
        success_log_msg: typing.Optional[str] = None,
        is_common_data: bool = False,
    ) -> None:
    """Push the data to local cache file"""

    if is_common_data:
        # The common files are not stored in userwise folder
        _tmp_common_data_path = generic_config.tmp_cache_folder_path.parent / '_common_data'
        _tmp_common_data_path.mkdir(parents=True, exist_ok=True)
        file_path = _tmp_common_data_path / file_name
    else:
        file_path = generic_config.tmp_cache_folder_path / file_name


    match file_path.suffix:
        case '.pkl':
            with open(file_path, 'wb') as fp:
                return pickle.dump(obj=data, file=fp)
        case '.json':
            with open(file_path, 'w') as fp:
                return json.dump(obj=data, fp=fp)
        case _:
            raise ValueError('Invalid File Type')

    _msg = f"Data dumped to cache file = {file_path}"
    if success_log_msg:
        _msg += f" -> {success_log_msg}"
    qapp_logger.debug(_msg)

# ----------------------------------------------------------------------------------------------------

def _get_quantsapp_ac_details() -> generic_models.AccountDetails_Pydantic:
    """Return the details related to logged in Quantsapp Account"""

    if 'qapp_ac_data' not in _internal_session_data:
        raise generic_exceptions.LoginNotInitiatedError('Initiate Login to get the Quantsapp account details')  # TODO change the exception and its error

    return _internal_session_data['qapp_ac_data']

# ----------------------------------------------------------------------------------------------------

@dataclass
class ApiRateLimiter:

    capacity: int
    refill_rate: int | float

    # ---------------------------------------------------------------------------

    def __post_init__(self) -> None:

        self.tokens = self.capacity
        self._last_refill = time.time()

    # ---------------------------------------------------------------------------

    def _refill(self) -> None:
        """Refills tokens based on elapsed time"""

        now = time.time()
        elapsed_time = now - self._last_refill
        refill_amount = round(elapsed_time * self.refill_rate)
        self.tokens = min(self.capacity, self.tokens + refill_amount)
        self._last_refill = now

    # ---------------------------------------------------------------------------

    def is_allowed(self, tokens_requested: int = 1) -> bool:
        """Checks if a request is allowed or needs to throttle"""

        # Do the refill, if required
        self._refill()

        if self.tokens >= tokens_requested:
            self.tokens -= tokens_requested
            return True

        return False