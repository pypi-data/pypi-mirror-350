# Built-in Modules
import json
import time
import gzip
import struct
import typing
import threading
import datetime as dt
import collections.abc


# Third-party Modules
import websocket


# Local Modules
from quantsapp._logger import qapp_logger
from quantsapp._websocket._abstract_ws import QappWebsocket
from quantsapp._websocket import (
    _models as websocket_models,
    _config as websocket_config,
)

from quantsapp._execution import (
    _utils as execution_utils,
    _cache as execution_cache,
    _enums as execution_enums,
    _models as execution_models,
)

from quantsapp._execution._modules._order_list import GetOrders
from quantsapp._execution._modules._order_list_models import ResponseOrderListingData_Type

from quantsapp import (
    _utils as generic_utils,
    _models as generic_models,
)

# ----------------------------------------------------------------------------------------------------


class OptionsBrokerOrderUpdatesWebsocket(QappWebsocket):

    _last_active_at: int = 0

    # ---------------------------------------------------------------------------

    def __init__(
            self,
            url: str,
            ws_conn_cond: threading.Condition,
            order_updates_callback: collections.abc.Callable[[websocket_models.OrderUpdatesWs_Type], typing.Any],
        ) -> None:

        self.ws_conn_cond = ws_conn_cond

        # Create ws connection
        QappWebsocket.__init__(
            self,
            url=url,
            ws_conn_cond=ws_conn_cond,
            thread_name=self.__class__.__name__,

            # Wait till the condition met and then connect to ws
            wait_condition={
                'wait_condition': OptionsBrokerOrderUpdatesWebsocket.should_wait_to_connect_broker_order_updates_ws,
                'notify_condition': self._notify_ws_cond,
                'sleep_sec': websocket_config.SLEEP_TIME_BROKER_ORDER_UPDATE_WS_CONNECTION_CHECK,
            }
        )

        self.order_updates_callback = order_updates_callback

        # For the api invocation usages
        self._responses: dict[str, typing.Any] = {}

        # Storing Websocket Session data
        self.ws_session_data = None

    # ---------------------------------------------------------------------------

    # TODO check if this method required or not
    def on_reconnect(self, ws: websocket.WebSocket) -> None:
        qapp_logger.debug(f"AutoReconnect {self.__class__.__name__} -> {ws = }")

    # ---------------------------------------------------------------------------

    def on_message(self, ws: websocket.WebSocket, message: bytes | str) -> None:

        if isinstance(message, bytes):
            """sample message
            b'\x10\x00\x06\x01\x00\x00mstock,MA6232931\x1f\x8b\x08\x00\x98\xb7\x1dh\x02\xffM\x90\xbbn\xc4 \x10E\xff\x85\xda\xbb\x1a\x9e\x06\xba4\x91Rl\xaa4\xa9\x90\x8d\xd9\x08\xc5\xaf`\\XQ\xfe=\x03\xf2F\xa1\x9a\xe1\xc0\xbds\xe7\x9bt\x9eX2my\xf1\x9f\xcd\xedI1\xce\x0c\xa7\xa4!\xbd[\xd2\x10R\x1c\x10s\xaa\x19\x93 \xc1(E5\xc2\xf0\x0fR\x05\xe5Pa4\x17\\0\xc4_.\x85\xbb+\x94\x19\xec\xf2\xe1\xeeq\x1c\x03\xf6P[b[\xd9\x908o9\xedS\x983\xaa\xbc\xbe<\xbf\xbd[*/\xb7\xee\xb80i\xbdeR\x02\x94A6\xc4=\x16k\x8a>\x10K\xaf\xf4\xac\xffT\xebU\xef\xf6-x\xb7\xafC\x97\xcb\xb3V\xa8\xb6\xd5\x00\xba\x8e\x07\xe5\xcf2\xec>\xbb|\xac\xc8\xc9\x9c\xa6\x11Uk\x10\xb7\xe5.\xef\xc5h\r\xf3\x10\xe7\x8f\x02\x9c\xcf\t\x134\x04ukT\x85K0\xe2\xf1\xe5\x94\x19\xe3\x14s\xcd\\\xec\x1f\xbe\xad6B3\x03\x14}q\xb7\xab;\x87\x87+\xfc\xfc\x02XM\x87Jt\x01\x00\x00'
            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
            """
            # TODO Remove this sample before live

            len_broker_client, _len_data = struct.unpack('<hi', message[0:6])

            _order_update: websocket_models.BrokerOrderUpdateRawWsData_Type = json.loads(gzip.decompress(message[6+len_broker_client:]))

            # qapp_logger.debug(f"Received on ws -> {_order_update = }")

            _parsed_order = self._process_broker_order_update(_order_update)

            self.order_updates_callback(_parsed_order)

        elif isinstance(message, str):
            _resp = json.loads(message)
            if _resp.get('ws_msg_type') == 'qapp_broker_updates_options_subscription_success':

                """sample _resp
                {
                    "status": "1",
                    "msg": "success",
                    "ws_msg_type": "qapp_broker_updates_options_subscription_success"
                }
                """

                # Notify the other thread that the ws connected successfully 
                self._notify_ws_cond()

                # Set the last active conn status time
                OptionsBrokerOrderUpdatesWebsocket._last_active_at = int(time.time())

                qapp_logger.debug(f"{self.__class__.__name__} connected!!!")

    # ---------------------------------------------------------------------------

    def on_error(self, ws: websocket.WebSocket, error: Exception) -> None:
        qapp_logger.error(f"Error on {self.__class__.__name__}")
        qapp_logger.error(f"{ws = }")
        qapp_logger.error(f"{error = }")

    # ---------------------------------------------------------------------------

    def on_close(self, ws: websocket.WebSocket, close_status_code: int, close_msg: str) -> None:
        qapp_logger.debug(f"{self.__class__.__name__} closed -> {close_status_code = }, {close_msg = }")

    # ---------------------------------------------------------------------------

    def on_pong(self, ws: websocket.WebSocket, message: str) -> None:
        OptionsBrokerOrderUpdatesWebsocket._last_active_at = int(time.time())

    # ---------------------------------------------------------------------------

    def _notify_ws_cond(self) -> None:
        """Notify the websocket condition lock to proceed further"""

        with self.ws_conn_cond:
            self.ws_conn_cond.notify()

    # ---------------------------------------------------------------------------

    def _process_broker_order_update(self, order_data: websocket_models.BrokerOrderUpdateRawWsData_Type) -> websocket_models.OrderUpdatesWs_Type:
        """Parse the real-time broker ws order data to client format"""

        _tmp_broker_client = execution_models.BrokerClient_Pydantic.from_api_str(order_data['ac'])
        _tmp_order_ref_internal_id = f"{order_data['b_orderid']}|{order_data.get('e_orderid', '0')}"
        _tmp_exist_order = execution_cache.orders.setdefault(_tmp_broker_client, {}).get(_tmp_order_ref_internal_id)

        # TODO this later
        # # For some broker, on order placement the exchange order_id is not present or '0', then after it got placed or modified, 
        # # they are sending with proper exchange order id, to handle this first check if the give exchange order_id is present or not
        # # if not present, then check for 'broker_order_id|0'
        # if not _tmp_exist_order:
        #     _tmp_order_ref_internal_id = f"{order_data['b_orderid']}|0"
        #     _tmp_exist_order = execution_cache.orders.setdefault(_tmp_broker_client, {}).get(_tmp_order_ref_internal_id)


        is_modify_local_cahce_file_required = False

        _new_order = websocket_models.BrokerOrderUpdateWsData_Pydantic(
            broker_client=_tmp_broker_client,
            b_orderid=order_data['b_orderid'],
            e_orderid=order_data.get('e_orderid', '0'),
            userid=str(order_data['userid']),
            instrument=generic_models._Instrument_Pydantic.from_api_str(order_data['instrument']).api_instr_str,
            buy_sell=execution_enums.OrderBuySell(order_data['bs']),
            product_type=execution_enums.OrderProductType(order_data['product_type']),
            order_status=execution_enums.OrderStatus(order_data['order_status']),
            order_type=execution_enums.OrderType(order_data['order_type']),
            q_ref_id=order_data['q_ref_id'],
            o_ctr=order_data['o_ctr'],
            qty=order_data['qty'],
            qty_filled=order_data['qty_filled'],
            price=order_data['price'],
            price_filled=order_data['price_filled'],
            stop_price=order_data.get('stop_price', 0),
            q_usec=execution_utils.convert_update_sec_to_datetime(order_data['q_usec']),
            b_usec_update=execution_utils.convert_update_sec_to_datetime(order_data['b_usec_update']),
        )

        # The order received is not in the cache data
        if not _tmp_exist_order:
            _tmp_new_order: ResponseOrderListingData_Type = {
                'broker_client': _tmp_broker_client,
                'b_orderid': _new_order.b_orderid,
                'e_orderid': _new_order.e_orderid,
                'userid': _new_order.userid,
                'instrument': _new_order.instrument,
                'buy_sell': _new_order.buy_sell,
                'product_type': _new_order.product_type,
                'order_status': _new_order.order_status,
                'order_type': _new_order.order_type,
                'q_ref_id': _new_order.q_ref_id,
                'o_ctr': _new_order.o_ctr,
                'qty': _new_order.qty,
                'qty_filled': _new_order.qty_filled,
                'price': _new_order.price,
                'price_filled': _new_order.price_filled,
                'stop_price': _new_order.stop_price,
                'q_usec': _new_order.q_usec,
                'b_usec_update': _new_order.b_usec_update,
            }
            execution_cache.orders[_tmp_broker_client][_tmp_order_ref_internal_id] = _tmp_new_order

            qapp_logger.debug(f"Realtime Order (new) updated to cache order -> {_tmp_new_order}")

            is_modify_local_cahce_file_required = True


        # if the order exists and only if the 'o_ctr' counter is more than the previous one
        elif order_data.get('o_ctr', 0) >= _tmp_exist_order['o_ctr']:

            # TODO change the temp exist order dict to pydantic model (if required)
            # TODO avoid creating pydantic model as above for only updating below details

            _tmp_exist_order['q_ref_id'] = _new_order.q_ref_id
            _tmp_exist_order['qty'] = _new_order.b_orderid
            _tmp_exist_order['qty_filled'] = _new_order.qty_filled
            _tmp_exist_order['price'] = _new_order.price
            _tmp_exist_order['price_filled'] = _new_order.price_filled
            _tmp_exist_order['b_usec_update'] = _new_order.b_usec_update
            _tmp_exist_order['product_type'] = _new_order.product_type
            _tmp_exist_order['order_status'] = _new_order.order_status
            _tmp_exist_order['o_ctr'] = _new_order.o_ctr
            _tmp_exist_order['order_type'] = _new_order.order_type
            _tmp_exist_order['q_usec'] = _new_order.q_usec
            _tmp_exist_order['stop_price'] = _new_order.stop_price

            qapp_logger.debug(f"Realtime Order (old) updated to cache order -> {_tmp_exist_order}")

            is_modify_local_cahce_file_required = True


        if is_modify_local_cahce_file_required:
            GetOrders.save_cache_data(data=execution_cache.orders)

        return _new_order.model_dump()

    # ---------------------------------------------------------------------------

    @staticmethod
    def should_connect_broker_order_updates_ws() -> bool:

        # TODO replace this with exchange based MarketTimings

        # Non-trading day - Don't Allow
        if not generic_utils.MarketTimings.is_open_today:
            return False

        # If after market timings - Don't Allow
        if generic_utils.MarketTimings.is_after_market():
            return False

        return True

    # ---------------------------------------------------------------------------

    @staticmethod
    def should_wait_to_connect_broker_order_updates_ws() -> bool:

        # TODO replace this with exchange based MarketTimings

        # If in-between market timings - Allow
        if generic_utils.MarketTimings.is_market_open():
            return False

        # If before (market timings - 'x'min) - Allow
        if (generic_utils.MarketTimings.dt_open - dt.datetime.now(dt.UTC)).seconds < websocket_config.ALLOW_BROKER_ORDER_WS_CONN_BEFORE_MARKET_TIMINGS:
            return False

        return True

    # ---------------------------------------------------------------------------

    @staticmethod
    def is_ws_active() -> bool:
        """Check the ws connection status with last pong time"""

        # Not even a single pong recevied
        if not OptionsBrokerOrderUpdatesWebsocket._last_active_at:
            return False

        # time interval between current time and last pong time less than the max pong skip time, then declare ws active
        if (int(time.time()) - OptionsBrokerOrderUpdatesWebsocket._last_active_at) < websocket_config.DEFAULT_PING_INTERVAL_SEC * websocket_config.MAX_PONG_SKIP_FOR_ACTIVE_STATUS:
            return True

        return False
