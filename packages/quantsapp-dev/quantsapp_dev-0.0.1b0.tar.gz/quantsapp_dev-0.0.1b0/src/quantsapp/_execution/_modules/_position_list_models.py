# Built-in Modules
import typing


# Third-party Modules
from pydantic import (
    BaseModel,
    Field,
)


# Local Modules
# from quantsapp._models import (
#     ApiResponseStatus_Type,
#     BaseResponse_Pydantic,
# )
from quantsapp import _models as generic_models
from quantsapp._execution import _enums as execution_enums
from quantsapp._execution._models import (

    OrderProductTypes_Type,

    BrokerClient_Pydantic,
)


# -- Typed Dicts -------------------------------------------------------------------------------------



class ApiResponsePositionsCombined_Type(typing.TypedDict):
    """sample
    ```
    {
        'instrument': 'NIFTY:15-May-25:c:25200',
        'product_type': 'nrml',
        'buy_qty': 75,
        'buy_t_value': 581.25,
        'sell_qty': 75,
        'sell_t_value': 570
    }
    """
    instrument: str
    product_type: OrderProductTypes_Type
    buy_qty: int
    buy_t_value: int | float
    sell_qty: int
    sell_t_value: int | float



class ResponsePositionsAccountwiseListing_Type(typing.TypedDict):
    """sample
    ```
    {
        'instrument': 'NIFTY:15-May-25:c:25200',
        'product_type': 'nrml',
        'buy_qty': 75,
        'buy_t_value': 581.25,
        'sell_qty': 75,
        'sell_t_value': 570
        'p_ctr': 3,  # TODO same logic as o_ctr, Check whether position data coming on order updates ws (This will come once order got completed)
    }
    """

    instrument: str
    product_type: execution_enums.OrderProductType
    buy_qty: int
    buy_t_value: int | float
    sell_qty: int
    sell_t_value: int | float
    p_ctr: int



class ApiResponsePositionsAccountwise_Type(typing.TypedDict):
    """sample
    ```
    {
        'mstock,MA6232931': [
            {
                'instrument': 'NIFTY:15-May-25:c:25900',
                'product_type': 'nrml',
                'buy_qty': 75,
                'buy_t_value': 93.75,
                'sell_qty': 75,
                'sell_t_value': 86.25
                'p_ctr': 3,
            },
        ]
    }
    """
    instrument: str  # TODO change this to instrument type
    product_type: OrderProductTypes_Type
    buy_qty: int
    buy_t_value: int | float
    sell_qty: int
    sell_t_value: int | float
    p_ctr: int



class ResponsePositionsCombinedListing_Type(typing.TypedDict):
    """sample
    ```
    {
        'instrument': 'NIFTY:15-May-25:c:25200',
        'product_type': 'nrml',
        'buy_qty': 75,
        'buy_t_value': 581.25,
        'sell_qty': 75,
        'sell_t_value': 570
    }
    """

    instrument: str
    product_type: execution_enums.OrderProductType
    buy_qty: int
    buy_t_value: int | float
    sell_qty: int
    sell_t_value: int | float




class ApiResponseGetPositions_Type(typing.TypedDict):
    """sample
    ```
    {
        "status": "1",
        "msg": "success",
        "gzip": true,
        "positions": "H4sIABvKIWgC/4uuVsrMKy4pKs1NzStRslJQ8vN0C4m0MjTV9U2s1DUytUq2MjI1MjBQ0lFQKijKTylNLokvqSxIBSnNK8rNAYknlVbGF5ZUAoXMTaHckviyxJxSkCpTC0M9I5BwcWpODrIyMB9JnblBbSwAX3B17I4AAAA=",
    }
    """
    status: generic_models.ApiResponseStatus_Type
    msg: str
    gzip: bool
    positions: str | list[ApiResponsePositionsCombined_Type | ApiResponsePositionsAccountwise_Type]



class PayloadGetPositions_Type(typing.TypedDict):
    """sample
    ```
    {
        'broker': quantsapp.Broker.MSTOCK,
        'client_id': 'MA6232931',
    }
    """
    broker: execution_enums.Broker
    client_id: str




# -- Pydantic Models ---------------------------------------------------------------------------------


class PayloadGetPositions_Pydantic(BaseModel, frozen=True):
    broker_clients: list[BrokerClient_Pydantic]
    resync_from_broker: bool = Field(default=False)
    from_cache: bool = Field(default=True)


class Response_GetPositions(generic_models._BaseResponse):
    body: typing.Optional[dict[BrokerClient_Pydantic, list[ResponsePositionsAccountwiseListing_Type]]] = Field(default=None)


class Response_GetPositionsConsolidated(generic_models._BaseResponse):
    body: typing.Optional[list[ResponsePositionsCombinedListing_Type]] = Field(default=None)
