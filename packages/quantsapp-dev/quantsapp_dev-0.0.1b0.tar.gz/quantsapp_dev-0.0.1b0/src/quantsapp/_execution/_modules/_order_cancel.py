# Built-in Modules
import time
from dataclasses import dataclass


# Local Modules
from quantsapp import (
    exceptions as generic_exceptions,
    _utils as generic_utils,
)
from quantsapp._websocket._options_main_ws import OptionsMainWebsocket
from quantsapp._websocket import (
    _config as websocket_config,
)
from quantsapp._execution import (
    _cache as execution_cache,
    _enums as execution_enums,
)

from quantsapp._execution._models import BrokerClient_Pydantic
from quantsapp._execution._modules._order_cancel_models import (
    ResponseCancelOrders_Type,
    ApiResponseCancelOrders_Type,

    PayloadCancelOrderIds_Pydantic,
    PayloadCancelOrders_Pydantic,
    PayloadCancelAllOrders_Pydantic,
)

from quantsapp._execution._modules._order_list_models import ResponseOrderListingData_Type

# from quantsapp._execution._modules._order_list import GetOrders
from quantsapp._execution._modules._order_list_models import (
    ResponseOrderListingData_Type,
    # PayloadListOrders_Pydantic,
)

# ----------------------------------------------------------------------------------------------------


@dataclass
class CancelOrders:

    ws: OptionsMainWebsocket
    payload: PayloadCancelOrders_Pydantic

    # ---------------------------------------------------------------------------

    # TODO remove it later
    # def __post_init__(self) -> None:

    #     # If orders not cached, push that to validate
    #     if not execution_cache.orders:
    #         GetOrders(
    #             ws=self.ws,
    #             payload=PayloadListOrders_Pydantic(
    #                 broker_client=self.payload.orders[0].broker_client,
    #                 from_cache=True,
    #                 resync_from_broker=False,
    #             ),
    #         ).update_orders()

    # ---------------------------------------------------------------------------

    def cancel_orders(self) -> ResponseCancelOrders_Type:
        """Cancel pending orders"""

        self._validate_data()

        cancel_orders_resp: ApiResponseCancelOrders_Type = self.ws.invoke_api(
            # TODO try to make this more generic and take it from some config
            payload={
                'action': websocket_config.WsActionKeys.BROKER_ORDERS,
                'mode': 'cancel_orders',
                'order': {
                    order.broker_client._api_str: [  # type: ignore - private variable
                        {
                            'b_orderid': order_id.b_orderid,
                            'e_orderid': order_id.e_orderid,
                        }
                        for order_id in order.order_ids
                    ]
                    for order in self.payload.orders
                }
            },
        ) # type: ignore

        if cancel_orders_resp['status'] != '1':
            raise generic_exceptions.BrokerOrdersCancelFailed(cancel_orders_resp['msg'])

        # Wait for sometime, so that the order update will be recevied and update the modification on cache data
        # TODO check whether order update websocket is connected or not
        time.sleep(1)

        return {
            'success': not cancel_orders_resp['has_failed'],
            'ref_id': cancel_orders_resp['q_ref_id_c'],
        }

    # ---------------------------------------------------------------------------

    def _validate_data(self) -> None:
        """validate the data which can't be done from the pydantic level(may be due to circular import Error)"""

        # TODO replace this with exchange based MarketTimings
        if not generic_utils.MarketTimings.is_market_open():
            raise generic_exceptions.InvalidInputError('Market Closed')

        for order in self.payload.orders:
            for order_id in order.order_ids:
                exist_order = self._get_existing_order(
                    broker_client=order.broker_client,
                    order_id=order_id,
                )
                if exist_order:
                    self._validate_order_status(exist_order)

    # ---------------------------------------------------------------------------

    def _validate_order_status(self, exist_order: ResponseOrderListingData_Type):

        if exist_order['order_status'] in (
            execution_enums.OrderStatus.CANCELLED,
            execution_enums.OrderStatus.COMPLETED,
            execution_enums.OrderStatus.FAILED,
            execution_enums.OrderStatus.REJECTED,
        ):
            raise generic_exceptions.InvalidInputError(f"Order already {exist_order['order_status']}")

    # ---------------------------------------------------------------------------

    def _get_existing_order(self, broker_client: BrokerClient_Pydantic, order_id: PayloadCancelOrderIds_Pydantic) -> ResponseOrderListingData_Type | None:
        """Get the existing order from cache, if not found then try fetching from api again"""

        # TODO move this to generic area where it can be used by other modules

        _tmp_order_id_ref = f"{order_id.b_orderid}|{order_id.e_orderid}"

        _exist_order_data = execution_cache.orders.get(broker_client, {}).get(_tmp_order_id_ref)

        if not _exist_order_data:
            return None

        return _exist_order_data

# ----------------------------------------------------------------------------------------------------


@dataclass
class CancelAllOrders:

    ws: OptionsMainWebsocket
    payload: PayloadCancelAllOrders_Pydantic

    # ---------------------------------------------------------------------------

    def cancel_all_orders(self) -> ResponseCancelOrders_Type:
        """Cancel all pending orders belongs to specific broker account"""

        cancel_all_orders_resp: ApiResponseCancelOrders_Type = self.ws.invoke_api(
            # TODO try to make this more generic and take it from some config
            payload={
                'action': websocket_config.WsActionKeys.BROKER_ORDERS,
                'mode': 'cancel_orders',
                'cancel_all': True,
                'broker_client': self.payload.broker_client._api_str,  # type: ignore - private variable
            },
        ) # type: ignore

        if cancel_all_orders_resp['status'] != '1':
            raise generic_exceptions.BrokerOrdersCancelFailed(cancel_all_orders_resp['msg'])

        return {
            'success': cancel_all_orders_resp['has_failed'],
            'ref_id': cancel_all_orders_resp['q_ref_id_c'],
        }

    # ---------------------------------------------------------------------------

