# Built-in Modules
import typing
import datetime as dt


# Third-party Modules
from pydantic import (
    BaseModel,
    Field,
    PositiveInt,
    PositiveFloat,
    model_validator,
)


# Local Modules
from quantsapp._master_data import MasterData
from quantsapp.exceptions import InvalidInputError
# from quantsapp import _enums as generic_enums
from quantsapp._execution import (
    _enums as execution_enums,
    _models as execution_models,
)
from quantsapp import _models as generic_models
from quantsapp._execution._models import (
    OrderSegments_Type,
    OrderOptionTypes_Type,
    OrderTransactionTypes_Type,
    OrderProductTypes_Type,
    OrderTypes_Type,
    OrderValidity_Type,
    OrderStatus_Type,

    BrokerClient_Pydantic,
)


# -- Typed Dicts -------------------------------------------------------------------------------------



class ApiPayloadPlaceOrderLeg_Type(typing.TypedDict):
    """sample
    ```
    {
        "qty": 75,
        "price": 1.1,
        "symbol": "NIFTY",
        "segment": "o",
        "opt_type": "c",
        "expiry": "15-May-25",
        "strike": 25500,
        "buy_sell": "b"
    }
    """
    qty: int
    price: float
    symbol: str
    segment: OrderSegments_Type
    expiry: str
    buy_sell: OrderTransactionTypes_Type

    # Only for Options
    opt_type: typing.Optional[OrderOptionTypes_Type]
    strike: typing.Optional[float | int]


class ApiPayloadPlaceOrder_Type(typing.TypedDict):
    """sample
    ```
    {
        "accounts": {
            "mstock,MA6232931": 1
        },
        "exchange": "NSE-FO",
        "product": "nrml",
        "order_type": "limit",
        "validity": "day",
        "legs": [
            PlaceOrderLegData
        ]
        "settings": {
            "margin_benefit": True,
        }
    }
    """
    accounts: dict[str, int]
    exchange: generic_models.Exchange_Type
    product: OrderProductTypes_Type
    order_type: OrderTypes_Type
    validity: OrderValidity_Type
    legs: list[ApiPayloadPlaceOrderLeg_Type]
    settings: dict[typing.Literal['margin_benefit'], bool]



class ApiResponsePlaceOrderIndividualLeg_Type(typing.TypedDict):
    """sample
    ```
    {
        "b_orderid": "ATQOU00005F5",
        "qty": 75,
        "buy_sell": "b",
        "price": 0.05
    }
    """
    b_orderid: typing.NotRequired[str]  # Only if order got success
    qty: int
    buy_sell: OrderTransactionTypes_Type
    price: float


class ApiResponsePlaceOrder_Type(typing.TypedDict):
    """sample
    ```
    {
        'status': '1',
        'msg': 'success',
        'has_failed': True,
        'q_ref_id': 8,
        'q_usec': 1747905016476938,  # micro seconds
        'orders': {
            "choice,X153364": {
                "placed": {
                    "NIFTY:26-Jun-25:c:26500": [
                        ApiResponsePlaceOrderIndividualLeg_Type
                    ]
                },
                "failed": {
                    "NIFTY:26-Jun-25:c:26500": [
                        {
                            "qty": 75,
                            "buy_sell": "b",
                            "price": 0.01
                        }
                    ]
                }
            }
        }
    }
    """
    status: generic_models.ApiResponseStatus_Type
    msg: str

    has_failed: bool
    q_ref_id: int
    q_usec: int  # Micro seconds
    orders: dict[
        str,
        dict[
            OrderStatus_Type,
            dict[
                str,
                list[ApiResponsePlaceOrderIndividualLeg_Type]
            ]
        ]
    ]


class PayloadPlaceOrderBrokerAccounts_Type(typing.TypedDict):
    broker: execution_enums.Broker
    client_id: str
    lot_multiplier: int


class PayloadPlaceOrderLeg_Type(typing.TypedDict):
    qty: int
    price: float
    # instrument: generic_models.Instrument_Pydantic
    instrument: str
    # buy_sell: execution_enums.OrderBuySell
    buy_sell: execution_models.OrderTransactionTypes_Type
    stop_price: typing.NotRequired[float]



class ResponsePlaceOrderIndividualLeg_Type(typing.TypedDict):
    """sample
    ```
    {
        "b_orderid": "ATQOU00005F5",
        "qty": 75,
        "buy_sell": "b",
        "price": 0.05
    }
    """
    b_order_id: typing.NotRequired[str]  # Only if order got success
    qty: int
    buy_sell: execution_enums.OrderBuySell
    price: float



class ResponsePlaceOrders_Type(typing.TypedDict):
    """sample
    ```
    {
        'success': bool,
        'ref_id': 8,
        'q_usec': 1747905016476938,  # micro seconds
        'orders': {
            BrokerClient_Pydantic:  {
                "placed": {
                    "NIFTY:26-Jun-25:c:26500": [
                        ResponsePlaceOrderIndividualLeg_Type
                    ]
                },
                "failed": {
                    "NIFTY:26-Jun-25:c:26500": [
                        {
                            "qty": 75,
                            "buy_sell": "b",
                            "price": 0.01
                        }
                    ]
                }
            }
        }
    }
    """
    success: bool
    ref_id: int
    q_usec: dt.datetime
    orders: dict[
        BrokerClient_Pydantic,
        dict[
            execution_enums.OrderStatus,
            dict[
                # generic_models.Instrument_Pydantic,
                str,  # TODO try to create new type with specific string
                list[ResponsePlaceOrderIndividualLeg_Type]
            ]
        ]
    ]

# -- Pydantic Models ---------------------------------------------------------------------------------


class PayloadPlaceOrderBrokerAccounts_Pydantic(BaseModel, frozen=True):
    broker_client: BrokerClient_Pydantic
    lot_multiplier: PositiveInt = Field(gt=0, default=1)



class PayloadPlaceOrderLeg_Pydantic(BaseModel, frozen=True):
    qty: PositiveInt = Field(gt=0)
    price: PositiveFloat = Field(
        ge=0,
        default=0,  # For market order don't need to pass it
    )
    instrument: generic_models._Instrument_Pydantic
    buy_sell: execution_enums.OrderBuySell

    # Only present for stop loss limit order
    stop_price: typing.Optional[PositiveFloat] = Field(
        ge=0,
        default=None,
    )

    # ---------------------------------------------------------------------------

    @model_validator(mode='before')
    @classmethod
    def validate_place_order_leg(cls, data: typing.Any) -> typing.Any:

        _lot_size: PositiveInt = MasterData.master_data['symbol_data'][data['instrument'].symbol]['lot_size'][data['instrument'].expiry]

        if data['qty'] % _lot_size != 0:
            raise InvalidInputError(f"Invalid Qty, should be multiple of {_lot_size} for {data['instrument'].symbol!r}")

        return data


class PayloadPlaceOrder_Pydantic(BaseModel, frozen=True):
    broker_accounts: list[PayloadPlaceOrderBrokerAccounts_Pydantic]
    exchange: execution_enums.Exchange
    product: execution_enums.OrderProductType
    order_type: execution_enums.OrderType
    validity: execution_enums.OrderValidity
    legs: list[PayloadPlaceOrderLeg_Pydantic]
    margin_benefit: bool = Field(default=True)

    # ---------------------------------------------------------------------------

    @model_validator(mode='after')
    def validate_stop_loss_limit_price_on_all_legs(self: typing.Self) -> typing.Self:

        for leg in self.legs:
            if (self.order_type == execution_enums.OrderType.SLL):
                if not leg.stop_price:
                    raise InvalidInputError(f"stop_price should be for Stop Loss Limit Order")
                if leg.price <= leg.stop_price:
                    raise InvalidInputError(f"price({leg.price}) should be less than stop_price({leg.stop_price}) for Stop Loss Limit Order")

        return self


class Response_PlaceOrder(generic_models._BaseResponse):
    body: typing.Optional[ResponsePlaceOrders_Type] = Field(default=None)
