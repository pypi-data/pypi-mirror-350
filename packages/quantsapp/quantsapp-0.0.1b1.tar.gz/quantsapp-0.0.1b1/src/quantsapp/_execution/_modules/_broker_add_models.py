# Built-in Modules
import typing


# Third-party Modules
from pydantic import (
    BaseModel,
    Field,
    model_validator,
)


# Local Modules
from quantsapp.exceptions import InvalidInputError
from quantsapp._execution import _enums as execution_enums

from quantsapp import _models as generic_models


# -- Typed Dicts -------------------------------------------------------------------------------------


class ApiResponseBrokerAdd_Type(typing.TypedDict):
    status: generic_models.ApiResponseStatus_Type
    msg: str


class PayloadDhanBrokerLoginCredentials_Type(typing.TypedDict):
    access_token: str

class PayloadChoiceBrokerLoginCredentials_Type(typing.TypedDict):
    mobile: str
    client_access_token: str



PayloadBrokerLoginCredentials_Type = PayloadDhanBrokerLoginCredentials_Type \
    | PayloadChoiceBrokerLoginCredentials_Type


# -- Pydantic Models ---------------------------------------------------------------------------------


class PayloadDhanBrokerLoginCredentials_Pydantic(BaseModel, frozen=True):
    access_token: str

class PayloadChoiceBrokerLoginCredentials_Pydantic(BaseModel, frozen=True):
    mobile: str  # TODO add validation of mobile no. if required, Discuss with Shubham sir
    client_access_token: str

class PayloadAddBroker_Pydantic(BaseModel, frozen=True):
    broker: execution_enums.Broker
    login_credentials: PayloadDhanBrokerLoginCredentials_Pydantic | PayloadChoiceBrokerLoginCredentials_Pydantic
    delete_previous_users: bool = Field(default=False)
    update_owner: bool = Field(default=False)

    # ---------------------------------------------------------------------------

    @model_validator(mode='after')
    def validate_login_credentials(self: typing.Self) -> typing.Self:

        match self.broker:
            case execution_enums.Broker.DHAN:
                if not isinstance(self.login_credentials, PayloadDhanBrokerLoginCredentials_Pydantic):
                    raise InvalidInputError(f"Invalid login credentials for {self.broker.value} broker")
            case execution_enums.Broker.CHOICE:
                if not isinstance(self.login_credentials, PayloadChoiceBrokerLoginCredentials_Pydantic):
                    raise InvalidInputError(f"Invalid login credentials for {self.broker.value} broker")
            case _:
                raise InvalidInputError(f"Invalid Broker for 'access_token' login!")

        return self




class Response_AddBroker(generic_models._BaseResponse):
    body: typing.Optional[str] = Field(default=None)
