# Built-in Modules
import typing
import datetime as dt
import collections.abc


# Third-party Modules
from pydantic import (
    BaseModel,
    Field,
)


# Local Modules
from quantsapp import _models as generic_models
from quantsapp._execution._modules._broker_login_data_models import BrokerLoginDbData_Type
from quantsapp._execution import (
    _enums as execution_enums,
    _models as execution_models,
)


# -- Typed Dicts -------------------------------------------------------------------------------------

class WaitCondition_Type(typing.TypedDict):
    wait_condition: collections.abc.Callable[[], bool]
    notify_condition: typing.Optional[collections.abc.Callable[[], None]]
    sleep_sec: int



class BrokerOrderUpdateRawWsData_Type(typing.TypedDict):
    """sample
    ```
    {
        "ac": "mstock,MA6232931",
        "b_orderid": "31822505096618",
        "e_orderid": "1600000149834342",
        "q_ref_id": 29,
        "qty_filled": 0,
        "qty": 75,
        "instrument": "NIFTY:15-May-25:c:25500",
        "bs": "b",
        "price": 1.1,
        "price_filled": 1.1,
        "b_usec_update": 1746778008000000,
        "product_type": "nrml",
        "order_status": "pending",
        "o_ctr": 2,
        "userid": 622594,
        "order_type": "limit",
        "q_usec": 1746777894829010,
        "stop_price": 0.0
    }
    """

    ac: str
    b_orderid: str
    e_orderid: str
    q_ref_id: int
    qty_filled: int
    qty: int
    instrument: str
    bs: typing.Literal['b', 's']
    price: float
    price_filled: float
    b_usec_update: int
    product_type: execution_models.OrderProductTypes_Type
    order_status: execution_models.OrderStatus_Type
    o_ctr: int
    userid: int
    order_type: execution_models.OrderTypes_Type
    q_usec: int
    stop_price: float



class ApiResponseMainOptionsWsApiHelperClient_Type(typing.TypedDict):
    """sample
    ```
    {
        'status': '1',
        'msg': str,
        'responses': [
            {}
        ],
        'custom_key': str,
        'routeKey': str,
        'ws_msg_type': 'qapp_api_gateway_options_success_api_request',
    }
    """
    status: generic_models.ApiResponseStatus_Type
    msg: str
    responses: list[BrokerLoginDbData_Type]
    custom_key: str
    routeKey: str
    ws_msg_type: typing.Literal[
        'qapp_api_gateway_options_success_api_request',
        'qapp_api_gateway_options_failure_api_request',
    ]



class ApiResponseMainOptionsWsMarketTimings_Type(typing.TypedDict):
    """sample
    {
        'open': '2025-05-09T09:15:00+05:30',
        'close': '2025-05-09T15:30:00+05:30',
        'is_open_today': True
    }
    """
    open: generic_models.DateTimeIso_Type
    close: generic_models.DateTimeIso_Type
    is_open_today: bool




class ApiResponseMainOptionsWsSessionDataVersions_Type(typing.TypedDict):
    """sample
    ```
    {
        'brokers_login_config': '1',
        'security_master': '1',
    }
    """
    brokers_login_config: str
    security_master: str



class ApiResponseMainOptionsWsAccountType_Type(typing.TypedDict):
    """sample
    {
        'ac_type': 'pro_plus'
    }
    """
    ac_type: generic_models.AccountType_Type



class ApiResponseMainOptionsWsSessionData_Type(typing.TypedDict):
    """sample
    ```
    {
        'market_timings': {
            'nse-fo': ApiResponseMainOptionsWsMarketTimings_Type
        },
        'ac_details': {
            'in': ApiResponseMainOptionsWsAccountType_Type
        },
        'client_setting': '23'  # TODO change this to client_master_version -> master {server_version: int, client_version: int}
        'etoken': 'spW48ZXL0uFa497+iWFvnX3vLW8NoSEYc6nHVwPllXMhDtBMS0kiVwbudTfIT5jMBZ3M8vHy3T1OydgFEPBAmZFS1Po8UJ6ZGNeZklTHSFZ4hv49jQaHKLec6ax04jQC+0zkijO2rnft/JS/brFrQzJ7SpXznxnGJ6w8ClX4zoE/zwxFDb0kAkot86mOcJCkmDO6Ui11QmCteQ7JZVmvrPoEfHF424eAU9pp6MHuflZhtm26GM5/vN5zuTNfrcuRZ',
        'user_id': '622594',
        'api_key': 'u7IoXQbITjy5992_fSSIsg',
        'market_data': 'Gzipped pickled data'
        'versions': ApiResponseMainOptionsWsSessionDataVersions_Type,

        # TODO send the master json version data and download if required from api_client_helper

        # Remove this
        'session_validity': 0,

    }
    """
    market_timings: dict[generic_models.Exchange_Type, ApiResponseMainOptionsWsMarketTimings_Type]
    ac_details: dict[generic_models.Country_Type, ApiResponseMainOptionsWsAccountType_Type]
    user_id: generic_models.NumericString_Type
    etoken: str
    api_key: str
    market_data: bytes
    versions: ApiResponseMainOptionsWsSessionDataVersions_Type


class ApiResponseMainOptionsWsGeneral_Type(typing.TypedDict):
    """sample
    {
        'status': '1',
        'msg': 'success',
        'ws_msg_type': 'qapp_api_gateway_options_etoken_authorized',
        'session_data': ApiResponseMainOptionsWsSessionData_Type
    }
    """
    status: generic_models.ApiResponseStatus_Type
    msg: str
    ws_msg_type: typing.Literal[
        'qapp_api_gateway_options_success_api_request',
        'qapp_api_gateway_options_failure_api_request',
        'qapp_api_gateway_options_invalid_route',
    ]
    session_data: ApiResponseMainOptionsWsSessionData_Type



class OrderUpdatesWs(typing.TypedDict):
    broker_client: execution_models.BrokerClient
    b_orderid: str
    e_orderid: str
    q_ref_id: int
    qty_filled: int
    qty: int
    instrument: str
    buy_sell: execution_enums.OrderBuySell
    price: float
    price_filled: float
    b_usec_update: dt.datetime
    product_type: execution_enums.OrderProductType
    order_status: execution_enums.OrderStatus
    o_ctr: int
    userid: str
    order_type: execution_enums.OrderType
    q_usec: dt.datetime
    stop_price: typing.Optional[float]

# -- Pydantic Models ---------------------------------------------------------------------------------


class BrokerOrderUpdateWsData_Pydantic(BaseModel, frozen=True):
    broker_client: execution_models.BrokerClient
    b_orderid: str
    e_orderid: str
    q_ref_id: int
    qty_filled: int
    qty: int
    # instrument: generic_models.Instrument_Pydantic
    instrument: str
    buy_sell: execution_enums.OrderBuySell
    price: float = Field(ge=0)
    price_filled: float = Field(ge=0)
    b_usec_update: dt.datetime
    product_type: execution_enums.OrderProductType
    order_status: execution_enums.OrderStatus
    o_ctr: int
    userid: str
    order_type: execution_enums.OrderType
    q_usec: dt.datetime
    stop_price: typing.Optional[float] = Field(
        ge=0,
        description='Only available for Stop Loss Limit Order type'
    )