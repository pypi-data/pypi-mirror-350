# Built-in Modules
from dataclasses import dataclass


# Local Modules
from quantsapp import exceptions as generic_exceptions
from quantsapp._websocket import (
    _config as websocket_config,
)
from quantsapp._websocket._options_main_ws import OptionsMainWebsocket
from quantsapp._execution._modules._broker_delete_models import (
    PayloadDeleteBroker_Pydantic,
    ApiResponseBrokerDelete_Type,
)
from quantsapp._execution._modules._broker_login_data import BrokerDisplayNames


# ----------------------------------------------------------------------------------------------------


@dataclass
class DeleteBroker:

    ws: OptionsMainWebsocket
    payload: PayloadDeleteBroker_Pydantic

    # ---------------------------------------------------------------------------

    def delete(self) -> str:
        """Delete the Broker Account from Quantsapp, if exists"""

        delete_api_resp: ApiResponseBrokerDelete_Type = self.ws.invoke_api(
            # TODO try to make this more generic and take it from some config
            payload={
                'action': websocket_config.WsActionKeys.BROKER_LOGIN,
                'mode': 'delete_account',
                'broker': self.payload.broker_client.broker.value,
                'client_id': self.payload.broker_client.client_id,
            },
        ) # type: ignore

        if delete_api_resp['status'] != '1':
            raise generic_exceptions.BrokerDeletionFailed(delete_api_resp['msg'])

        return f"{BrokerDisplayNames.broker_display_names[self.payload.broker_client.broker]!r} Broker account deleted successfully from Quantsapp account!"