# Built-in Modules
import typing


# Third-party Modules
from pydantic import (
    BaseModel,
    Field,
)


# Local Modules
# from quantsapp._models import NumericString_Type
# from quantsapp._models import (
#     ApiResponseStatus_Type,
#     BaseResponse_Pydantic,
# )
from quantsapp import _models as generic_models
from quantsapp._execution._models import BrokerClient


# -- Typed Dicts -------------------------------------------------------------------------------------


class ApiResponseBrokerDelete_Type(typing.TypedDict):
    status: generic_models.ApiResponseStatus_Type
    msg: str
    version: generic_models.NumericString_Type
    global_version: generic_models.NumericString_Type



# -- Pydantic Models ---------------------------------------------------------------------------------


class PayloadDeleteBroker_Pydantic(BaseModel, frozen=True):
    broker_client: BrokerClient


class Response_DeleteBroker(generic_models._BaseResponse):
    body: typing.Optional[str] = Field(default=None)
