# Built-in Modules
import json
import gzip
import base64
import typing
import contextlib

from dataclasses import dataclass


# Local Modules
from quantsapp._logger import qapp_logger
from quantsapp import (
    exceptions as generic_exceptions,
    _utils as generic_utils,
)
from quantsapp._websocket._options_main_ws import OptionsMainWebsocket
from quantsapp._websocket import (
    _config as websocket_config,
)
from quantsapp._execution import (
    _enums as execution_enums,
    _cache as execution_cache,
)
from quantsapp._execution._models import BrokerClient_Pydantic
from quantsapp._execution._modules._book_update import BookUpdate
from quantsapp._execution._modules._book_update_models import PayloadBookUpdate_Pydantic
from quantsapp._execution._modules._position_list_models import (
    ResponsePositionsAccountwiseListing_Type,
    ResponsePositionsCombinedListing_Type,
    ApiResponsePositionsCombined_Type,
    ApiResponsePositionsAccountwise_Type,
    ApiResponseGetPositions_Type,

    PayloadGetPositions_Pydantic,
)


# ----------------------------------------------------------------------------------------------------

# TODO add caching for positions too

@dataclass
class GetPositions:

    ws: OptionsMainWebsocket
    payload: PayloadGetPositions_Pydantic

    _cache_file_name: typing.ClassVar[str] = 'broker_positions.pkl'

    # ---------------------------------------------------------------------------

    def get_positions(self) -> dict[BrokerClient_Pydantic, list[ResponsePositionsAccountwiseListing_Type]]:
        """Get the positions of specific Broker Client in the requested order"""

        # If caching not required or first time call, update positions form DB
        if (not self.payload.from_cache) \
                or (self.payload.resync_from_broker) \
                or (not execution_cache.positions):
            self.update_positions()

        return self.parse_data_to_client()

    # ---------------------------------------------------------------------------

    def update_positions(self) -> None:
        """Update the positions of specific Broker Client from either local cache or api"""

        if not self.payload.resync_from_broker:
            # First try to get data from local file
            # if file not exists then download the new data from api and push it to cache
            with contextlib.suppress(Exception):
                execution_cache.positions = self.get_data_from_local_file()

                # If data found in cache, then send it from cache itself
                # else download from api again
                for broker_client in self.payload.broker_clients:
                    if (broker_client._api_str in execution_cache.positions) \
                            and (self.payload.from_cache):
                        return None

        # Get it from api, if the data not available in cache
        self._get_data_from_api()

    # ---------------------------------------------------------------------------

    def _get_data_from_api(self) -> None:
        """Invoke the API to get the positions"""

        _resp_positions = self._get_api_data()  # Order book update is not available for individual accounts

        execution_cache.positions = _resp_positions

        # Saving local for caching purposes
        self.save_cache_data(execution_cache.positions)

        qapp_logger.debug(f"Positions updated for {self.payload.broker_clients} from api")

    # ---------------------------------------------------------------------------

    def _get_api_data(self) -> dict[str, list[ApiResponsePositionsAccountwise_Type]]:
        """Invoke the API to get the positions"""

        get_positions_resp: ApiResponseGetPositions_Type = self.ws.invoke_api(
            # TODO try to make this more generic and take it from some config
            payload={
                'action': websocket_config.WsActionKeys.BROKER_ORDERS,
                'mode': 'get_positions_account_wise',
                'broker_clientids': [
                    broker_client._api_str  # type: ignore - private variable
                    for broker_client in self.payload.broker_clients
                ]
            },
        ) # type: ignore

        if get_positions_resp['status'] != '1':
            raise generic_exceptions.BrokerPositionsListingFailed(get_positions_resp['msg'])

        return self._get_decompress_positions_data(get_positions_resp)

    # ---------------------------------------------------------------------------

    # def _get_update_book_api_data(self) -> list[ApiResponsePositionsAccountwise_Type]:  TODO only for combined data update
    #     """Invoke the Update Book API to get the Orders from Broker"""

    #     get_positions_resp: ApiResponseGetPositions_Type = BookUpdate(
    #         ws=self.ws,
    #         payload=PayloadBookUpdate_Pydantic(
    #             broker_client=self.payload.broker_client,
    #             update_on='positions',
    #         )
    #     ).get_data()  # type: ignore

    #     if get_positions_resp['status'] != '1':
    #         raise generic_exceptions.BrokerPositionsListingFailed(get_positions_resp['msg'])

    #     return self._get_decompress_positions_data(get_positions_resp)

    # ---------------------------------------------------------------------------

    def _get_decompress_positions_data(self, get_orders_resp: ApiResponseGetPositions_Type) -> dict[str, list[ApiResponsePositionsAccountwise_Type]]:
        """Decompress the data if compressed"""

        positions_data = get_orders_resp['positions'] # type: ignore

        if get_orders_resp['gzip']:
            positions_data: dict[str, list[ApiResponsePositionsAccountwise_Type]] = json.loads(
                gzip.decompress(
                    data=base64.b64decode(positions_data) # type: ignore
                )
            )

        return positions_data

    # ---------------------------------------------------------------------------

    def parse_data_to_client(self) -> dict[BrokerClient_Pydantic, list[ResponsePositionsAccountwiseListing_Type]]:
        """Transform the structure to final format"""

        _final_resp: dict[BrokerClient_Pydantic, list[ResponsePositionsAccountwiseListing_Type]] = {}

        for _broker_client, _positions_data in execution_cache.positions.items():
            _tmp_broker_client = BrokerClient_Pydantic.from_api_str(_broker_client)
            if _tmp_broker_client not in self.payload.broker_clients:
                continue
            _final_resp[_tmp_broker_client] = [
                {
                    'instrument': _position_data['instrument'],
                    'product_type': execution_enums.OrderProductType(_position_data['product_type']),
                    'buy_qty': _position_data['buy_qty'],
                    'buy_t_value': _position_data['buy_t_value'],
                    'sell_qty': _position_data['sell_qty'],
                    'sell_t_value': _position_data['sell_t_value'],
                    'p_ctr': _position_data['p_ctr'],
                }
                for _position_data in _positions_data
            ]

        return _final_resp

    # ---------------------------------------------------------------------------

    @staticmethod
    def save_cache_data(data: dict[str, list[ApiResponsePositionsAccountwise_Type]]) -> None:
        """saving the orders data to local cache file"""

        generic_utils.put_local_file_cache_data(
            file_name=GetPositions._cache_file_name,
            data=data,
            success_log_msg='Broker Positions pushed to cache file',
        )

    # ---------------------------------------------------------------------------

    @staticmethod
    def get_data_from_local_file() -> dict[str, list[ApiResponsePositionsAccountwise_Type]]:
        """Get the Mapped Brokers data from the local cache file"""

        _cache_broker_orders_data = generic_utils.get_local_file_cache_data(GetPositions._cache_file_name)

        qapp_logger.debug(f"Broker positions returned from cache folder")

        return _cache_broker_orders_data




# ----------------------------------------------------------------------------------------------------


@dataclass
class GetPositionsCombined:

    ws: OptionsMainWebsocket
    payload: PayloadGetPositions_Pydantic

    _cache_file_name: typing.ClassVar[str] = 'broker_positions_combined.pkl'

    # ---------------------------------------------------------------------------

    def get_positions(self) -> list[ResponsePositionsCombinedListing_Type]:
        """Get the positions of specific Broker Client in the requested order"""

        # If caching not required or first time call, update positions form DB
        if (not self.payload.from_cache) \
                or (self.payload.resync_from_broker) \
                or (not execution_cache.positions_combined):
            self.update_positions()

        return self.parse_data_to_client()

    # ---------------------------------------------------------------------------


    def update_positions(self) -> None:
        """Update the positions of specific Broker Client from either local cache or api"""

        if not self.payload.resync_from_broker:
            # First try to get data from local file
            # if file not exists then download the new data from api and push it to cache
            with contextlib.suppress(Exception):
                execution_cache.positions_combined = self.get_data_from_local_file()
                return None

        # Get it from api, if the data not available in cache
        self._get_data_from_api()

    # ---------------------------------------------------------------------------

    def _get_data_from_api(self) -> None:
        """Invoke the API to get the positions"""

        _resp_positions = self._get_api_data()  # TODO Order book update with for individual broker accounts

        execution_cache.positions_combined = _resp_positions

        # Saving local for caching purposes
        self.save_cache_data(execution_cache.positions_combined)

        qapp_logger.debug(f"PositionsCombined updated for {self.payload.broker_clients} from api")

    # ---------------------------------------------------------------------------

    def _get_api_data(self) -> list[ApiResponsePositionsCombined_Type]:
        """Invoke the API to get the positions combined"""

        get_positions_resp: ApiResponseGetPositions_Type = self.ws.invoke_api(
            # TODO try to make this more generic and take it from some config
            payload={
                'action': websocket_config.WsActionKeys.BROKER_ORDERS,
                'mode': 'get_positions',
                'broker_clientids': [
                    broker_client._api_str  # type: ignore - private variable
                    for broker_client in self.payload.broker_clients
                ]
            },
        ) # type: ignore

        if get_positions_resp['status'] != '1':
            raise generic_exceptions.BrokerPositionsListingFailed(get_positions_resp['msg'])

        return self._get_decompress_positions_data(get_positions_resp)

    # ---------------------------------------------------------------------------

    def _get_decompress_positions_data(self, get_orders_resp: ApiResponseGetPositions_Type) -> list[ApiResponsePositionsCombined_Type]:
        """Decompress the data if compressed"""

        positions_data = get_orders_resp['positions'] # type: ignore

        if get_orders_resp['gzip']:
            positions_data: list[ApiResponsePositionsCombined_Type] = json.loads(
                gzip.decompress(
                    data=base64.b64decode(positions_data) # type: ignore
                )
            )

        return positions_data

    # ---------------------------------------------------------------------------

    @staticmethod
    def save_cache_data(data: list[ApiResponsePositionsCombined_Type]) -> None:
        """saving the orders data to local cache file"""

        generic_utils.put_local_file_cache_data(
            file_name=GetPositionsCombined._cache_file_name,
            data=data,
            success_log_msg='Broker Positions pushed to cache file',
        )

    # ---------------------------------------------------------------------------

    @staticmethod
    def get_data_from_local_file() -> list[ApiResponsePositionsCombined_Type]:
        """Get the Mapped Brokers data from the local cache file"""

        _cache_broker_orders_data = generic_utils.get_local_file_cache_data(GetPositionsCombined._cache_file_name)

        qapp_logger.debug(f"Broker positions returned from cache folder")

        return _cache_broker_orders_data


    # ---------------------------------------------------------------------------

    def parse_data_to_client(self) -> list[ResponsePositionsCombinedListing_Type]:
        """Transform the structure to final format"""

        return [
            {
                'instrument': data['instrument'],
                'product_type': execution_enums.OrderProductType(data['product_type']),
                'buy_qty': data['buy_qty'],
                'buy_t_value': data['buy_t_value'],
                'sell_qty': data['sell_qty'],
                'sell_t_value': data['sell_t_value'],
            }
            for data in execution_cache.positions_combined
        ]

    # ---------------------------------------------------------------------------


