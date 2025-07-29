# Built-in Modules
import typing


# Third-party Modules
from pydantic import BaseModel


# Local Modules
from quantsapp import _models as generic_models
from quantsapp._execution import _models as execution_models

from quantsapp._execution._modules._order_list_models import ApiResponseGetOrdersAccountWise_Type
from quantsapp._execution._modules._position_list_models import ApiResponseGetPositions_Type

# -- Typed Dicts -------------------------------------------------------------------------------------



class ApiResponseUpdateOrderBook_Type(typing.TypedDict):
    """sample
    ```
    {
        "status": "1",
        "msg": "Orderbook Updated !",
        "orders_response": {
            "status": "1",
            "msg": "success",
            "gzip": true,
            "orders": "H4sIAJ4pI2gC/72Su07DMBSGX6Xy3Fa+5DhONhYkhjKxIISs1DGS1VxaxxkixLvj45YKEAMhEp7sc/5z+T/56ZXsde9r611NyhURAjgHCkxkheBkvSJ73x+s16ZxtgsoaYfQm8N6dyO54IVgSaTHwRo9Husq2ChieZYzLhUUNB2UjJMebNNgiz3W2E9zmUwyViiqsgJkTLtuCH5sL0Pv724fHksGm101bTiUpuQAlGKfXpvgo0bgHTvqIVRhHLDMVJ2JM21NrskwHXFD0rjWBQwfvTMYoVsK6dnXowlXXefbBmWnZPFnb6cwxUQO56t+cWlkbBkDsersUUawRfa2Xn1HzvkHcsXpUuSczkUuhMoY/RPybDHyfA7yz96WIWfygjxXdOEvZ7jaPOQUJCiVdv/3X8627NfEv1qbQ/z5HYpc1iFYBAAA"
        },
        "positions_response": {
            "status": "1",
            "msg": "success",
            "gzip": true,
            "positions": "H4sIAJ4pI2gC/72Su07DMBSGX6Xy3Fa+5DhONhYkhjKxIISs1DGS1VxaxxkixLvj45YKEAMhEp7sc/5z+T/56ZXsde9r611NyhURAjgHCkxkheBkvSJ73x+s16ZxtgsoaYfQm8N6dyO54IVgSaTHwRo9Husq2ChieZYzLhUUNB2UjJMebNNgiz3W2E9zmUwyViiqsgJkTLtuCH5sL0Pv724fHksGm101bTiUpuQAlGKfXpvgo0bgHTvqIVRhHLDMVJ2JM21NrskwHXFD0rjWBQwfvTMYoVsK6dnXowlXXefbBmWnZPFnb6cwxUQO56t+cWlkbBkDsersUUawRfa2Xn1HzvkHcsXpUuSczkUuhMoY/RPybDHyfA7yz96WIWfygjxXdOEvZ7jaPOQUJCiVdv/3X8627NfEv1qbQ/z5HYpc1iFYBAAA"
        },
        "trade_status": "1",
        "trade_msg": "Tradebook Updated !",
        "positions_status": "1",
        "positions_msg": "Positions Updated !",
    }
    """
    status: generic_models.ApiResponseStatus_Type
    msg: str
    trade_status: str
    trade_msg: str
    positions_status: str
    positions_msg: str

    orders_response: ApiResponseGetOrdersAccountWise_Type
    positions_response: ApiResponseGetPositions_Type



# -- Pydantic Models ---------------------------------------------------------------------------------


class PayloadBookUpdate_Pydantic(BaseModel, frozen=True):
    broker_client: execution_models.BrokerClient
    update_on: typing.Literal['orders', 'positions']
