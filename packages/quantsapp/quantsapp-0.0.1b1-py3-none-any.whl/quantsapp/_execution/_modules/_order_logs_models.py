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

#     Instrument_Pydantic,
#     BaseResponse_Pydantic,
# )
from quantsapp import _models as generic_models
from quantsapp._execution._models import (
    BrokerClient,
)


# -- Typed Dicts -------------------------------------------------------------------------------------


class ApiResponseOrderLogsListing_Type(typing.TypedDict):
    """sample
    ```
    {
        'status': '1',
        'msg': 'success',
        'order_apilog': [
            {
                'http_code': 200,
                'b_response': '{"res": [{"status": true, "message": "SUCCESS", "errorcode": "", "data": {"script": "NIFTY2551525500CE", "orderid": "31622505137802", "uniqueorderid": "31622505137802"}}]}',
                'q_msg': 'success',
                'q_usec': 1747114712000000
            }
        ],
    }
    """
    status: generic_models.ApiResponseStatus_Type
    msg: str
    order_apilog: list[dict[str, typing.Any]]  # The order log can be of any format, differ from brokers


# -- Pydantic Models ---------------------------------------------------------------------------------


class PayloadGetOrderLogs_Pydantic(BaseModel, frozen=True):
    broker_client: BrokerClient
    instrument: generic_models._Instrument_Pydantic
    q_usec: dt.datetime


class Response_GetOrderLogs(generic_models._BaseResponse):
    body: typing.Optional[list[dict[str, typing.Any]]] = Field(default=None)
