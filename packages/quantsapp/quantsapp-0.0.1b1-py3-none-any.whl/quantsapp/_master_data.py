# Built-in Modules
import gzip
import typing
import base64
import pickle
import contextlib
import datetime as dt


# Third-party Modules
from pydantic import (
    PositiveInt,
    PositiveFloat,
)

# Local Modules
from quantsapp._logger import qapp_logger
from quantsapp import (
    _models as generic_models,
    _utils as generic_utils,
)
from quantsapp._api_helper._main import ApiHelper
from quantsapp._api_helper import _models as api_helper_models
from quantsapp._websocket import _config as websocket_config

# ----------------------------------------------------------------------------------------------------

class MasterData:

    master_data: generic_models.MasterData_Type = None # type: ignore

    _cache_file_name: typing.ClassVar[str] = 'master.pkl'

    # ---------------------------------------------------------------------------

    def update_master_data(self, api_helper: ApiHelper) -> None:
        """Retreive master which contains all price related metadata"""

        self.api_helper = api_helper

        if _tmp_master_resp := self._get_master_data():
            MasterData.master_data = _tmp_master_resp

    # ---------------------------------------------------------------------------

    def _get_master_data(self) -> generic_models.MasterData_Type | None:
        """Retreive master data from either cache or api based on condition"""

        # First try to get data from local file
        # if file not exists or the version mismatch with version got from Main Options WS,
        # then download the new data from api and push it to cache
        with contextlib.suppress(Exception):
            return self._get_master_data_from_local_file()

        self._add_get_master_data_request_to_api_helper()

    # ---------------------------------------------------------------------------

    def _get_master_data_from_local_file(self) -> generic_models.MasterData_Type:
        """Get the master data from the local cache file"""

        _cache_master_data = generic_utils.get_local_file_cache_data(self._cache_file_name, is_common_data=True)

        if _cache_master_data['version'] != websocket_config.WebsocketVersions.SECURITY_MASTER:
            qapp_logger.debug(f"Master version mismatch (file_version={_cache_master_data['version']}, ws_version={websocket_config.WebsocketVersions.SECURITY_MASTER})")
            raise ReferenceError('Version mismatch!')

        qapp_logger.debug(f"MasterData with version ({_cache_master_data['version']}) returned from cache folder")

        return _cache_master_data['data']

    # ---------------------------------------------------------------------------

    def _add_get_master_data_request_to_api_helper(self) -> None:
        """
            Add the request to api_helper data retreival,
            which will consolidate all requests and send a single request to optimize the query
        """

        self.api_helper.add_request(
            request=api_helper_models.ApiRequest_Pydantic(
                api_request={
                    'mode': 'master_data',
                    'sub_mode': 'get_all_data',
                },
                callback=MasterData.parse_master_data_from_api_response,
            ),
        )

    # ---------------------------------------------------------------------------

    @staticmethod
    def parse_master_data_from_api_response(master_data_api_response: generic_models.ApiResponseMasterData_Type) -> None:
        """Parse the master data recieved on API response"""

        # Decode the master data
        decoded_master_data = pickle.loads(
            gzip.decompress(
                base64.b64decode(master_data_api_response['master_data'])
            )
        )

        # Saving local for caching purposes
        generic_utils.put_local_file_cache_data(
            file_name=MasterData._cache_file_name,
            data={
                'data': decoded_master_data,
                'version': master_data_api_response['master_version'],
            },
            success_log_msg=f"MasterData downloaded and pushed to cache file with version ({master_data_api_response['master_version']}) & last updated on -> {master_data_api_response['last_updated_on']}",
            is_common_data=True,
        )

        # Set parsed data to class variable
        MasterData.master_data = decoded_master_data

    # ---------------------------------------------------------------------------

    @staticmethod
    def is_valid_symbol(symbol: str) -> bool:

        if MasterData.master_data:
            return symbol in MasterData.master_data['symbol_data']
        return False

    # ---------------------------------------------------------------------------

    @staticmethod
    def is_valid_expiry(symbol: str, expiry: dt.datetime) -> bool:

        if MasterData.master_data:
            return expiry in MasterData.master_data['symbol_data'][symbol]['expiry']['all']
        return False

    # ---------------------------------------------------------------------------

    @staticmethod
    def is_valid_strike(symbol: str, expiry: dt.datetime, strike: typing.Optional[PositiveInt|PositiveFloat]) -> bool:

        if MasterData.master_data:
            return strike in MasterData.master_data['symbol_data'][symbol]['strikes'][expiry]
        return False

    # ---------------------------------------------------------------------------

    @staticmethod
    def get_all_expiries(symbol: str) -> list[dt.datetime]:
        """Return all valid expiries"""

        if MasterData.master_data:
            return MasterData.master_data['symbol_data'][symbol]['expiry']['all'] # type: ignore
        return []

    # ---------------------------------------------------------------------------

    @staticmethod
    def get_all_strikes(symbol: str, expiry: dt.datetime) -> list[PositiveInt | PositiveFloat]:
        """Return all valid strikes"""

        if MasterData.master_data:
            return MasterData.master_data['symbol_data'][symbol]['strikes'][expiry] # type: ignore
        return []

    # ---------------------------------------------------------------------------