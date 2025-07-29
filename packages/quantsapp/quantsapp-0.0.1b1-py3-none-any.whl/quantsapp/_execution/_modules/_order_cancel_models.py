# Built-in Modules
import typing


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
from quantsapp._execution import _enums as execution_enums
from quantsapp._execution._models import BrokerClient

# -- Typed Dicts -------------------------------------------------------------------------------------



class PayloadCancelOrderIds_Type(typing.TypedDict):
    b_orderid: str
    e_orderid: str

class PayloadCancelOrder_Type(typing.TypedDict):
    broker: execution_enums.Broker
    client_id: str
    order_ids: list[PayloadCancelOrderIds_Type]


class ResponseCancelOrders_Type(typing.TypedDict):
    """sample
    ```
    {
        'success': bool,
        'ref_id': 8
    }
    """
    success: bool
    ref_id: int



class ApiResponseCancelOrders_Type(typing.TypedDict):
    """sample
    ```
    {
        "status": "1",
        "msg": "success",
        "has_failed": false,
        "q_ref_id_c": 15
    }
    """
    status: generic_models.ApiResponseStatus_Type
    msg: str

    has_failed: bool
    q_ref_id_c: int



# -- Pydantic Models ---------------------------------------------------------------------------------


class PayloadCancelOrderIds_Pydantic(BaseModel, frozen=True):
    b_orderid: str
    e_orderid: str

class PayloadCancelIndividualBrokerOrder_Pydantic(BaseModel, frozen=True):
    broker_client: BrokerClient
    order_ids: list[PayloadCancelOrderIds_Pydantic]

class PayloadCancelOrders_Pydantic(BaseModel, frozen=True):
    orders: list[PayloadCancelIndividualBrokerOrder_Pydantic]


class PayloadCancelAllOrders_Pydantic(BaseModel, frozen=True):
    broker_client: BrokerClient


class Response_CancelOrders(generic_models._BaseResponse):
    body: typing.Optional[ResponseCancelOrders_Type] = Field(default=None)

class Response_CancelAllOrders(generic_models._BaseResponse):
    body: typing.Optional[ResponseCancelOrders_Type] = Field(default=None)
