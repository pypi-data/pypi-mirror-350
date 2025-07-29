# Local Modules
from quantsapp._websocket._options_main_ws import OptionsMainWebsocket
from quantsapp._websocket._options_broker_order_updates_ws import OptionsBrokerOrderUpdatesWebsocket

# ----------------------------------------------------------------------------------------------------

def sdk_websocket_status() -> dict[str, bool]:
    return {
        'options_main_ws': OptionsMainWebsocket.is_ws_active(),
        'options_broker_order_updates_ws': OptionsBrokerOrderUpdatesWebsocket.is_ws_active(),
    }