# Built-in Modules
import typing
import datetime as dt


# Third-party Modules
from pydantic import (
    BaseModel,
    Field,
)

# Local Modules
# from quantsapp._models import (
#     DateTime_Type,
#     NumericString_Type,
# )
from quantsapp._execution import (
    _config as execution_config,
    _enums as execution_enums,
)
# from quantsapp._models import (
#     ApiResponseStatus_Type,

#     BaseResponse_Pydantic,
# )
from quantsapp import _models as generic_models
from quantsapp._execution._models import (
    Brokers_Type,
    BrokerRoles_Type,

)


# -- Typed Dicts -------------------------------------------------------------------------------------



ResponseListBrokersApiIndividualDataMargin = typing.TypedDict(
    'ResponseListBrokersApiIndividualDataMargin',
    {
        'dt': generic_models.DateTime_Type,
        'NSE-FO': generic_models.NumericString_Type,
    },
)
"""sample
```
{
    "dt": "02-May-25 02:18:50",
    "NSE-FO": "1534.53"
}
"""


class ResponseListBrokersApiIndividualData_Type(typing.TypedDict):
    """sample
    ```
    {
        "broker": "fivepaisa",
        "client_id": "50477264",
        "role": "executor",
        "name": "SHUBHRA",
        "validity": "02-May-25 23:59:59",
        "valid": true,
        "margin": ResponseListBrokersApiIndividualDataMargin
    }
    """
    broker: Brokers_Type
    client_id: str
    role: BrokerRoles_Type
    name: str
    validity: generic_models.DateTime_Type | typing.Literal['0', '-1', '-2']
    valid: bool
    margin: ResponseListBrokersApiIndividualDataMargin

class ApiResponseListBrokers_Type(typing.TypedDict):
    """sample
    ```
    {
        "status": "1",
        "msg": "No accounts available" | "success",
        "routeKey": "broker_login",
        "custom_key": "access_expiry_config",
        "ws_msg_type": "qapp_api_gateway_options_success_api_request"

        # Only available if accounts are mapped
        "data": [
            ResponseListBrokersApiIndividualData_Type,
        ],
        "version": "9",
        "next_margin_dt_utc": "02-May-25 02:33:50",
    }
    """
    status: generic_models.ApiResponseStatus_Type
    msg: str

    # Only present if accounts already mapped
    data: list[ResponseListBrokersApiIndividualData_Type]
    version: generic_models.NumericString_Type
    next_margin_dt_utc: generic_models.DateTime_Type


class ListBrokersIndividualBrokerData_Type(typing.TypedDict):
    # client_id: str
    margin: ResponseListBrokersApiIndividualDataMargin
    name: str
    role: execution_enums.BrokerRole
    valid: bool
    validity: dt.datetime | execution_enums.BrokerAccountValidity



class ResponseListAvailableBrokers_Type(typing.TypedDict):
    access_token_login: list[execution_enums.Broker | str]
    oauth_login: list[execution_enums.Broker | str]



class ResponseListMappedBrokers_Type(typing.TypedDict):
    brokers: dict[execution_enums.Broker, dict[str, ListBrokersIndividualBrokerData_Type]]  # str- client_id
    version: int
    next_margin: dt.datetime



# -- Pydantic Models ---------------------------------------------------------------------------------


class PayloadListAvailableBrokers_Pydantic(BaseModel, frozen=True):
    ...

class PayloadListMappedBrokers_Pydantic(BaseModel, frozen=True):
    resync_from_broker: bool = Field(default=False)
    from_cache: bool = Field(default=True)



class Response_ListAvailableBrokers(generic_models._BaseResponse):
    body: typing.Optional[ResponseListAvailableBrokers_Type] = Field(default=None)

class Response_ListMappedBrokers(generic_models._BaseResponse):
    body: typing.Optional[ResponseListMappedBrokers_Type] = Field(default=None)
