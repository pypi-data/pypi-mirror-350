# Built-in Modules
import time

from dataclasses import dataclass


# Local Modules
from quantsapp import (
    _utils as generic_utils,
    exceptions as generic_exceptions,
    _enums as generic_enums,
    constants as generic_constants,
)
from quantsapp._websocket._options_main_ws import OptionsMainWebsocket
from quantsapp._websocket import (
    _config as websocket_config,
)
from quantsapp._execution._modules._order_place_models import (
    ResponsePlaceOrders_Type,
    ApiPayloadPlaceOrder_Type,
    ApiPayloadPlaceOrderLeg_Type,
    ApiResponsePlaceOrder_Type,
    PayloadPlaceOrder_Pydantic,
)
from quantsapp._execution import (
    _enums as execution_enums,
    _utils as execution_utils,
    _models as execution_models,
    # _cache as execution_cache,
)
from quantsapp._version import __version__ as qapp_package_version

# from quantsapp._execution._modules._order_list import GetOrders
# from quantsapp._execution._modules._order_list_models import PayloadListOrders_Pydantic



# ----------------------------------------------------------------------------------------------------


@dataclass
class PlaceOrder:

    ws: OptionsMainWebsocket
    order: PayloadPlaceOrder_Pydantic

    # ---------------------------------------------------------------------------

    # TODO remove it later
    # def __post_init__(self) -> None:

    #     # TODO change this to execution object start preprocess
    #     # If orders not cached, push that to validate
    #     if not execution_cache.orders:
    #         GetOrders(
    #             ws=self.ws,
    #             payload=PayloadListOrders_Pydantic(
    #                 broker_client=self.order.broker_accounts[0].broker_client,
    #                 from_cache=True,
    #                 resync_from_broker=False,
    #             ),
    #         ).update_orders()

    # ---------------------------------------------------------------------------

    def place_order(self) -> ResponsePlaceOrders_Type:
        """Get the Orders of specific Broker Client in the requested order"""

        parsed_orders = self._parse_order()

        _order_resp =  self._place_order(parsed_orders)

        # Wait for sometime, so that the order update will be recevied and update the modification on cache data
        # TODO check whether order update websocket is connected or not
        time.sleep(1)

        return _order_resp


    # ---------------------------------------------------------------------------

    def _parse_order(self) -> ApiPayloadPlaceOrder_Type:
        """Transform the structure to final format"""

        parsed_order: ApiPayloadPlaceOrder_Type = {
            'accounts': { # type: ignore
                broker_ac.broker_client._api_str: broker_ac.lot_multiplier  # type: ignore - private variable
                for broker_ac in self.order.broker_accounts
            },
            'exchange': self.order.exchange.value,
            'product': self.order.product.value,
            'order_type': self.order.order_type.value,
            'validity': self.order.validity.value,
            'settings': {
                'margin_benefit': self.order.margin_benefit,
            }
        }

        parsed_legs = []

        for leg in self.order.legs:
            _curr_parsed_leg: ApiPayloadPlaceOrderLeg_Type = {  # type: ignore
                'qty': leg.qty,
                'symbol': leg.instrument.symbol,
                'price': leg.price,
                'expiry': leg.instrument.api_expiry_str,  # type: ignore - private variable
                'buy_sell': leg.buy_sell.value, # type: ignore
            }

            if leg.instrument.instrument_type == generic_enums.InstrumentType.FUTURE:
                _curr_parsed_leg['segment'] = generic_enums.InstrumentType.FUTURE.value
            else:
                _curr_parsed_leg['segment'] = generic_enums.InstrumentType._InstrumentType__OPTIONS # type: ignore
                _curr_parsed_leg['opt_type'] = leg.instrument.instrument_type.value
                _curr_parsed_leg['strike'] = leg.instrument.strike

            if self.order.order_type == execution_enums.OrderType.SLL:
                _curr_parsed_leg['stop_price'] = leg.stop_price

            parsed_legs.append(_curr_parsed_leg) # type: ignore


        parsed_order['legs'] = parsed_legs

        return parsed_order

    # ---------------------------------------------------------------------------

    def _place_order(self, orders_to_place: ApiPayloadPlaceOrder_Type) -> ResponsePlaceOrders_Type:
        """Invoke the API to get the Orders"""

        place_orders_resp: ApiResponsePlaceOrder_Type = self.ws.invoke_api(
            # TODO try to make this more generic and take it from some config
            payload={
                'action': websocket_config.WsActionKeys.BROKER_ORDERS,
                'mode': 'place_order',
                'order': orders_to_place,
                'page_id': f"python_sdk_{qapp_package_version}",
                'ui_orderid': f"{generic_utils._internal_session_data['qapp_ac_data'].API_KEY}_{int(time.time()*1000)}",
            },
        ) # type: ignore

        if place_orders_resp['status'] != '1':
            raise generic_exceptions.BrokerOrdersPlacingFailed(place_orders_resp['msg'])

        return {
            'success': not place_orders_resp['has_failed'],
            'ref_id': place_orders_resp['q_ref_id'],
            'q_usec': execution_utils.convert_update_sec_to_datetime(place_orders_resp['q_usec'], tz=generic_constants.DT_ZONE_IST),
            'orders': {
                execution_models.BrokerClient.from_api_str(_broker_client): {
                    execution_enums.OrderStatus(_order_status): {
                        _inst: [
                            {
                                'b_orderid': _leg_order_data.get('b_orderid', None),
                                'buy_sell': execution_enums.OrderBuySell(_leg_order_data['buy_sell']),
                                'price': _leg_order_data['price'],
                                'qty': _leg_order_data['qty'],
                            }
                            for _leg_order_data in _legs_order_data
                        ]
                        for _inst, _legs_order_data in _order_status_data.items()
                    }
                    for _order_status, _order_status_data in _order_resp_data.items()   
                }
                for _broker_client, _order_resp_data in place_orders_resp.get('orders', {}).items()
            }
        }

    # ---------------------------------------------------------------------------


