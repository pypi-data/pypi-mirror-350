# Built-in Modules
from dataclasses import dataclass


# Local Modules
from quantsapp import exceptions as generic_exceptions
from quantsapp._websocket._options_main_ws import OptionsMainWebsocket
from quantsapp._websocket import (
    _config as websocket_config,
)
from quantsapp._execution._modules._broker_login_data import (
    BrokerLoginData,
    BrokerDisplayNames,
)

from quantsapp._execution._modules._broker_add_models import (
    PayloadAddBroker_Pydantic,
    ApiResponseBrokerAdd_Type,  # TODO rename the _Type & _Pydantic later
)


# ----------------------------------------------------------------------------------------------------


@dataclass
class AddBroker:

    ws: OptionsMainWebsocket
    payload: PayloadAddBroker_Pydantic

    # ---------------------------------------------------------------------------

    def login(self) -> str:
        """Login to Broker Account"""

        self.broker_login_metadata = BrokerLoginData.broker_login_data

        self._validate_request()

        login_api_resp = self._login()

        if login_api_resp['status'] != '1':
            raise generic_exceptions.BrokerLoginFailed(login_api_resp['msg'])

        return f"{BrokerDisplayNames.broker_display_names[self.payload.broker]!r} Broker account added successfully to Quantsapp account!"

    # ---------------------------------------------------------------------------

    def _validate_request(self) -> None:
        """Validate the request params to proceeding login process"""

        self._validate_active_broker()

    # ---------------------------------------------------------------------------

    def _validate_active_broker(self) -> None:
        """Check whether the broker is active"""

        if self.payload.broker.value not in self.broker_login_metadata:
            raise generic_exceptions.BrokerLoginNotAllowed(f"Broker ({BrokerDisplayNames.broker_display_names[self.payload.broker]}) not allowed in API Login")

        if self.broker_login_metadata[self.payload.broker.value]['sdk_execution'] is False:
            raise generic_exceptions.BrokerLoginNotAllowed(f"Broker ({BrokerDisplayNames.broker_display_names[self.payload.broker]}) not allowed in API Login. Please use the Web/Mobile app to add the broker")

    # ---------------------------------------------------------------------------

    def _login(self) -> ApiResponseBrokerAdd_Type:
        """Invoke the api to do broker login"""

        return self.ws.invoke_api(
            # TODO try to make this more generic and take it from some config
            payload={
                'action': websocket_config.WsActionKeys.BROKER_LOGIN,
                'mode': 'add_account',
                'broker': self.payload.broker.value,
                'delete_previous_users': self.payload.delete_previous_users,
                'update_owner': self.payload.update_owner,
                'login_type': self.broker_login_metadata[self.payload.broker.value]['login_types'][0],  # TODO check this to to make it more generic
                'credentials': self.payload.login_credentials.model_dump(),
            },
        ) # type: ignore

    # ---------------------------------------------------------------------------
