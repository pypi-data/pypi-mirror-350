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
#     ApiResponseStatus_Type,

#     BaseResponse_Pydantic,
# )
from quantsapp import _models as generic_models
from quantsapp._execution._models import BrokerClient


# -- Typed Dicts -------------------------------------------------------------------------------------



class ApiResponseBrokerWsReConn_Type(typing.TypedDict):
    """Sample
    ```
    {
        "status": "1",
        "msg": "Connected",
    }
    """
    status: generic_models.ApiResponseStatus_Type
    msg: str


class ApiResponseBrokerWsConnStatus_Type(typing.TypedDict):
    """Sample
    ```
    {
        "status": "1",
        "msg": "Connected",
        "ts_ping": 1747129266,
        "ts_msg": 1747126860,
        "ts_conn": 0,
    }
    """
    status: generic_models.ApiResponseStatus_Type
    msg: str
    ts_ping: int
    ts_msg: int
    ts_conn: int

class ResponseBrokerWsConnStatus_Type(typing.TypedDict):
    """Sample
    ```
    {
        "ts_ping": dt.datetime,
        "ts_msg": dt.datetime,
        "ts_conn": dt.datetime,
    }
    """
    ts_ping: dt.datetime | None
    ts_msg: dt.datetime | None
    ts_conn: dt.datetime | None


# -- Pydantic Models ---------------------------------------------------------------------------------



class PayloadGetBrokerWebsocketConnectionStatus_Pydantic(BaseModel, frozen=True):
    broker_client: BrokerClient


class PayloadBrokerWebsocketReConnect_Pydantic(BaseModel, frozen=True):
    broker_client: BrokerClient




class Response_GetBrokerWebsocketConnectionStatus(generic_models._BaseResponse):
    body: typing.Optional[ResponseBrokerWsConnStatus_Type] = Field(default=None)

class Response_BrokerWebsocketReConnect(generic_models._BaseResponse):
    body: typing.Optional[str] = Field(default=None)
