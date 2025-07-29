# Built-in Modules
from dataclasses import dataclass


# Local Modules
from quantsapp import exceptions as generic_exceptions
from quantsapp._websocket._options_main_ws import OptionsMainWebsocket
from quantsapp._websocket import _config as websocket_config

from quantsapp._execution._modules._book_update_models import (
    ApiResponseUpdateOrderBook_Type,
    PayloadBookUpdate_Pydantic,
)

from quantsapp._execution._modules._order_list_models import ApiResponseGetOrdersAccountWise_Type
from quantsapp._execution._modules._position_list_models import ApiResponseGetPositions_Type


# ----------------------------------------------------------------------------------------------------


@dataclass
class BookUpdate:

    ws: OptionsMainWebsocket
    payload: PayloadBookUpdate_Pydantic

    # ---------------------------------------------------------------------------

    def get_data(self) -> ApiResponseGetPositions_Type | ApiResponseGetOrdersAccountWise_Type:
        """Get the Orders of specific Broker Client in the requested order"""

        return self._get_api_data()

    # ---------------------------------------------------------------------------

    def _get_api_data(self) -> ApiResponseGetPositions_Type | ApiResponseGetOrdersAccountWise_Type:
        """Invoke the API to update the Order Book"""

        _book_update_resp: ApiResponseUpdateOrderBook_Type = self.ws.invoke_api(
            # TODO try to make this more generic and take it from some config
            payload={
                'action': websocket_config.WsActionKeys.BROKER_ORDERS,
                'mode': 'update_orderbook',
                'broker_clientid': [self.payload.broker_client._api_str],  # type: ignore - private variable
                'screen': self.payload.update_on,
            },
        ) # type: ignore

        if _book_update_resp['status'] != '1':
            raise generic_exceptions.BrokerOrderBookUpdateFailed(_book_update_resp['msg'])

        if self.payload.update_on == 'orders':
            return _book_update_resp['orders_response']
        else:
            return _book_update_resp['positions_response']
