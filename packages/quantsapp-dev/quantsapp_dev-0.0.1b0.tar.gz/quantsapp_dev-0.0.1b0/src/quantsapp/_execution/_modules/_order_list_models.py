# Built-in Modules
import typing
import datetime as dt


# Third-party Modules
from pydantic import (
    BaseModel,
    Field,
)


# Local Modules
# from quantsapp._models import (
#     NumericString_Type,
#     ApiResponseStatus_Type,

#     Instrument_Pydantic,
#     BaseResponse_Pydantic,
# )
from quantsapp import _models as generic_models
from quantsapp._execution import _enums as execution_enums
from quantsapp._execution._models import (
    OrderProductTypes_Type,
    OrderStatus_Type,
    OrderTypes_Type,
    OrderTransactionTypes_Type,

    BrokerClient_Pydantic,
)

# -- Typed Dicts -------------------------------------------------------------------------------------



class ApiResponseOrderListing_Type(typing.TypedDict):
    """sample
    ```
    {
        'broker_client': 'mstock,MA6232931',
        'b_orderid': '33422505073382',
        'qty': 75,
        'price': 1.2,
        'buy_sell': 'b',
        'instrument': 'NIFTY:15-May-25:c:25500',
        'order_type': 'limit',
        'product_type': 'nrml',
        'q_usec': 1746596369775443,
        'userid': 622594,
        'order_status': 'pending',
        'b_usec_update': 1746596370000000,
        'e_orderid': 1600000075847609,
        'o_ctr': 1,
        'qty_filled': 0,
        'stop_price': 0.0
    }
    """
    broker_client: str
    b_orderid: str  # BrokerID when placing order
    e_orderid: generic_models.NumericString_Type  # Another BrokerID when placing order
    qty: int
    qty_filled: int
    price: float
    stop_price: float
    buy_sell: OrderTransactionTypes_Type
    instrument: str
    order_type: OrderTypes_Type
    product_type: OrderProductTypes_Type
    q_usec: int  # Quantsapp Order Send Timestamp in ms
    userid: int  # User ID of client who placed the order
    order_status: OrderStatus_Type
    b_usec_update: int  # Broker Order Updation Timestamp in ms
    o_ctr: int  # Order Update counter


class ApiResponseGetOrdersAccountWise_Type(typing.TypedDict):
    """sample
    ```
    {
        'status': '1',
        'msg': 'success',
        'gzip': True,
        'orders': 'H4sIAOsVG2gC/02Qy27DIBBFfyVinUSYZ+xdN5WySFfdVFWFbEwrFPwIDAur6r+XsdsorGDunTPDff8mXZyuLhobvBuBNDsyJJjsdX95UoyzmldkvyOdmWLvou/RwLlgTFJJNecnhvINliJoWa5z9NaVR3Vk2JcXk1wI2Nah048JYh7+Rr2cn1/fmkoeLu1yYLKxDZOSUjSu8wwsM8JI8IMHsuKnPlu4C2McwrqByclZnKuFkrXiqtZaCsGLVpRtc1XWrsUdnqCFnJAyu7H349f2UwSZPPctuAeeptspFvcQRqW2spYnoRWtEW4sRJS2YMynD8GhF3tLtrP5z4ge6c/HL86ik8+DAQAA',
        'pagination_key': typing.Any  # Optional, only available if more records are there (current limit is 100)
    }
    """
    status: generic_models.ApiResponseStatus_Type
    msg: str
    gzip: bool
    orders: str | list[ApiResponseOrderListing_Type]
    pagination_key: typing.Optional[typing.Any]



class PayloadListOrdersFilters_Type(typing.TypedDict):
    product: execution_enums.OrderProductType
    order_status: execution_enums.OrderStatus
    order_type: execution_enums.OrderType
    # instrument: generic_models.Instrument_Pydantic
    instrument: generic_models.InstrumentString_Type



class ResponseOrderListingData_Type(typing.TypedDict):
    """sample
    ```
    {
        'broker_client': 'mstock,MA6232931',
        'b_orderid': '33422505073382',
        'e_orderid': 1600000075847609,
        'userid': 622594,
        'qty': 75,
        'qty_filled': 0,
        'price': 1.2,
        'stop_price': 0.0
        'buy_sell': execution_enums.Order,
        'instrument': 'NIFTY:15-May-25:c:25500',
        'order_type': execution_enums.OrderType,
        'product_type': 'nrml',
        'order_status': 'pending',
        'q_usec': 1746596369775443,
        'b_usec_update': 1746596370000000,
        'o_ctr': 1,
    }
    """
    broker_client: BrokerClient_Pydantic
    b_orderid: str  # Broker OrderID when placing order
    e_orderid: generic_models.NumericString_Type  # Exchange OrderID when placing order
    userid: int  # User ID of client who placed the order
    qty: int
    qty_filled: int
    price: float
    stop_price: float
    buy_sell: execution_enums.OrderBuySell
    # instrument: generic_models.Instrument_Pydantic  # TODO remove it
    instrument: str
    order_type: execution_enums.OrderType
    product_type: execution_enums.OrderProductType
    order_status: execution_enums.OrderStatus
    q_usec: dt.datetime  # Quantsapp Order Send Timestamp in ms
    b_usec_update: dt.datetime  # Broker Order Updation Timestamp in ms
    o_ctr: int  # Order Update counter



# -- Pydantic Models ---------------------------------------------------------------------------------



class PayloadListOrdersFilters_Pydantic(BaseModel, frozen=True):
    product: typing.Optional[execution_enums.OrderProductType] = Field(default=None)
    order_status: typing.Optional[execution_enums.OrderStatus] = Field(default=None)
    order_type: typing.Optional[execution_enums.OrderType] = Field(default=None)
    instrument: typing.Optional[generic_models.InstrumentString_Type] = Field(default=None)
    # instrument: typing.Optional[generic_models.Instrument_Pydantic] = Field(default=None)


class PayloadListOrders_Pydantic(BaseModel, frozen=True):
    broker_client: BrokerClient_Pydantic
    ascending: bool = Field(default=False)
    from_cache: bool = Field(default=True)
    resync_from_broker: bool = Field(default=False)
    filters: typing.Optional[PayloadListOrdersFilters_Pydantic] = Field(default=None)


class Response_ListOrders(generic_models._BaseResponse):
    body: typing.Optional[list[ResponseOrderListingData_Type]] = Field(default=None)