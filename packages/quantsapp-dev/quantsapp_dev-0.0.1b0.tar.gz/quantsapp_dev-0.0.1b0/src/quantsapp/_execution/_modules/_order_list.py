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
from quantsapp import _models as generic_models
from quantsapp._websocket._options_main_ws import OptionsMainWebsocket
from quantsapp._websocket import (
    _config as websocket_config,
)
from quantsapp._execution import (
    _cache as execution_cache,
    _utils as execution_utils,
    _enums as execution_enums,
)

from quantsapp._execution._models import BrokerClient_Pydantic
from quantsapp._execution._modules._book_update import BookUpdate
from quantsapp._execution._modules._book_update_models import PayloadBookUpdate_Pydantic
from quantsapp._execution._modules._order_list_models import (
    ResponseOrderListingData_Type,
    ApiResponseGetOrdersAccountWise_Type,
    ApiResponseOrderListing_Type,

    PayloadListOrders_Pydantic,
)


# ----------------------------------------------------------------------------------------------------


@dataclass
class GetOrders:

    ws: OptionsMainWebsocket
    payload: PayloadListOrders_Pydantic

    _cache_file_name: typing.ClassVar[str] = 'broker_orders.pkl'

    # ---------------------------------------------------------------------------

    def get_orders(self) -> list[ResponseOrderListingData_Type]:
        """Get the Orders of specific Broker Client in the requested order"""

        # If caching not required or first time call, update orders form DB
        if (not self.payload.from_cache) \
                or (self.payload.resync_from_broker) \
                or (self.payload.broker_client not in execution_cache.orders):
            self.update_orders()

        # Send order records one by one
        return self._parse_record_to_client(execution_cache.orders[self.payload.broker_client])

    # ---------------------------------------------------------------------------

    def update_orders(self) -> None:
        """Update the Orders of specific Broker Client from either local cache or api"""

        # TODO fix the issue of local caching and then return data from local caching

        # if not self.payload.resync_from_broker:
        #     # First try to get data from local file
        #     # if file not exists then download the new data from api and push it to cache
        #     with contextlib.suppress(Exception):
        #         execution_cache.orders = self.get_data_from_local_file()

        #         # If data found in cache, then send it from cache itself
        #         # else download from api again
        #         if (self.payload.broker_client in execution_cache.orders) \
        #                 and (self.payload.from_cache):
        #             return None

        # Get it from api, if the data not available in cache
        self._get_data_from_api()

    # ---------------------------------------------------------------------------

    def _get_data_from_api(self) -> None:
        """Get the Orders of specific Broker Client from api"""

        self.__pagination_key: typing.Any = None

        while True:

            # Get the existing orders
            _tmp_orders = execution_cache.orders.setdefault(self.payload.broker_client, {})

            # Get the new orders
            raw_orders_data = self._get_update_book_api_data() if self.payload.resync_from_broker else self._get_api_data()

            # merge the new orders
            _tmp_orders |= self.parse_data(
                order_data=raw_orders_data,
            )

            # If no more records found, then exit the loop
            if not self.__pagination_key:
                break

        # Saving local for caching purposes
        self.save_cache_data(execution_cache.orders)

        qapp_logger.debug(f"Orders updated for {self.payload.broker_client} from api")

    # ---------------------------------------------------------------------------

    def _get_api_data(self) -> list[ApiResponseOrderListing_Type]:
        """Invoke the API to get the Orders"""

        get_orders_resp: ApiResponseGetOrdersAccountWise_Type = self.ws.invoke_api(
            # TODO try to make this more generic and take it from some config
            payload={
                'action': websocket_config.WsActionKeys.BROKER_ORDERS,
                'mode': 'get_order_status',
                'sub_mode': 'account',
                'broker_clientid': [self.payload.broker_client._api_str],  # Only one account selection allowed at a time  # type: ignore
                'pagination_key': self.__pagination_key,
                'has_pagination': False,  # To get all data without pagination
            },
        ) # type: ignore

        if get_orders_resp['status'] != '1':
            raise generic_exceptions.BrokerOrdersListingFailed(get_orders_resp['msg'])

        # If more records avaialble, then set pagination key to get more records if required
        # if 'has_pagination' is set to False, there won't be any pagination, but still keep it for fail safe
        self.__pagination_key = get_orders_resp.get('pagination_key')

        return self._get_decompressed_orders_data(get_orders_resp)

    # ---------------------------------------------------------------------------

    def _get_update_book_api_data(self) -> list[ApiResponseOrderListing_Type]:
        """Invoke the Update Book API to get the Orders from Broker"""

        get_orders_resp: ApiResponseGetOrdersAccountWise_Type = BookUpdate(
            ws=self.ws,
            payload=PayloadBookUpdate_Pydantic(
                broker_client=self.payload.broker_client,
                update_on='orders',
            )
        ).get_data()  # type: ignore

        if get_orders_resp['status'] != '1':
            raise generic_exceptions.BrokerOrdersListingFailed(get_orders_resp['msg'])

        return self._get_decompressed_orders_data(get_orders_resp)

    # ---------------------------------------------------------------------------

    def _get_decompressed_orders_data(self, get_orders_resp: ApiResponseGetOrdersAccountWise_Type) -> list[ApiResponseOrderListing_Type]:
        """Decompress the data if compressed"""

        orders_data = get_orders_resp['orders'] # type: ignore

        if get_orders_resp['gzip']:
            orders_data: list[ApiResponseOrderListing_Type] = json.loads(
                gzip.decompress(
                    data=base64.b64decode(orders_data) # type: ignore
                )
            )

        return orders_data

    # ---------------------------------------------------------------------------

    def parse_data(self, order_data: list[ApiResponseOrderListing_Type]) -> dict[str, ResponseOrderListingData_Type]:
        """Transform the structure to final format"""

        parsed_broker_data: dict[str, ResponseOrderListingData_Type] = {}

        for data in order_data:

            # TODO change the order ref id logic
            _tmp_order_ref_internal_id: str = f"{data['b_orderid']}|{data.get('e_orderid', '0')}"

            if (_tmp_order_ref_internal_id not in parsed_broker_data) \
                    or (data.get('o_ctr', 0) >= parsed_broker_data[_tmp_order_ref_internal_id]['o_ctr']):  # only update if o_ctr counter is more than the previous one

                # TODO change this dict to pydantic model (if required)
                parsed_broker_data[_tmp_order_ref_internal_id] = { #  type: ignore
                    'broker_client': BrokerClient_Pydantic.from_api_str(data['broker_client']),
                    'b_orderid': data['b_orderid'],
                    'e_orderid': str(data.get('e_orderid', '0')),
                    'userid': data.get('userid', 0),
                    'qty': data['qty'],
                    'qty_filled': data.get('qty_filled', 0),
                    'price': data['price'],
                    'stop_price': data.get('stop_price', 0),
                    'buy_sell': execution_enums.OrderBuySell(data['buy_sell']),
                    'instrument': generic_models._Instrument_Pydantic.from_api_str(data['instrument']).api_instr_str,
                    'order_type': execution_enums.OrderType(data['order_type']),
                    'product_type': execution_enums.OrderProductType(data['product_type']),
                    'order_status': execution_enums.OrderStatus(data['order_status']),
                    'q_usec': execution_utils.convert_update_sec_to_datetime(data['q_usec']),
                    'b_usec_update': execution_utils.convert_update_sec_to_datetime(data['b_usec_update']),
                    'o_ctr': data.get('o_ctr', 0),
                }

        return parsed_broker_data

    # ---------------------------------------------------------------------------

    def _parse_record_to_client(self, data: dict[str, ResponseOrderListingData_Type]) -> list[ResponseOrderListingData_Type]:
        """Transform the internal data to client data"""

        # Consider only the values, not the internal reference id
        _tmp = list(data.values())

        # filter data if requested
        _tmp = self._filter_data(_tmp)

        # Sort the records based on payload requested order
        _tmp = sorted(
            _tmp,
            key=lambda item: item['b_usec_update'],
            reverse=not self.payload.ascending,
        )

        return _tmp

    # ---------------------------------------------------------------------------

    def _filter_data(self, data: list[ResponseOrderListingData_Type]) -> list[ResponseOrderListingData_Type]:
        """Filter the data based on the payload"""

        _filtered_data: list[ResponseOrderListingData_Type] = []

        # if there is no filter conditions set, then send entire results
        if not self.payload.filters:
            return data

        _filter_conditions: dict[str, typing.Any] = {
            _filter_name: _filter_value
            for _filter_name, _filter_value in self.payload.filters # type: ignore
            if _filter_value
        }

        # if there is no filter conditions set, then send entire results
        if not _filter_conditions:
            return data        

        for _curr_data in data:

            # check for all requested conditions
            for _filter_name, _filter_value in _filter_conditions.items():

                if (_filter_name == 'product') \
                        and (_filter_value != _curr_data['product_type']):
                    break
                if (_filter_name == 'instrument') \
                        and (_filter_value != _curr_data['instrument']):
                    break
                if (_filter_name == 'order_type') \
                        and (_filter_value != _curr_data['order_type']):
                    break
                if (_filter_name == 'order_status') \
                        and (_filter_value != _curr_data['order_status']):
                    break

            # If all conditions met, then the break won't happen, so this else will get executed
            else:
                _filtered_data.append(_curr_data)

        return _filtered_data

    # ---------------------------------------------------------------------------

    @staticmethod
    def save_cache_data(data: dict[BrokerClient_Pydantic, dict[str, ResponseOrderListingData_Type]]) -> None:
        """saving the orders data to local cache file"""

        generic_utils.put_local_file_cache_data(
            file_name=GetOrders._cache_file_name,
            data=data,
            success_log_msg='BrokerOrders pushed to cache file',
        )

    # ---------------------------------------------------------------------------

    @staticmethod
    def get_data_from_local_file() -> dict[BrokerClient_Pydantic, list[ResponseOrderListingData_Type]]:
        """Get the Mapped Brokers data from the local cache file"""

        _cache_broker_orders_data = generic_utils.get_local_file_cache_data(GetOrders._cache_file_name)

        qapp_logger.debug(f"Broker Orders returned from cache folder")

        return _cache_broker_orders_data
