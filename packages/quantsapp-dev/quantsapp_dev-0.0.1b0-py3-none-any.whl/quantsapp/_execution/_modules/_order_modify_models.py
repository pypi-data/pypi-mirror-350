# Built-in Modules
import typing


# Third-party Modules
from pydantic import (
    BaseModel,
    PositiveInt,
    Field,
)


# Local Modules
from quantsapp._execution._models import BrokerClient_Pydantic
# from quantsapp._models import (
#     ApiResponseStatus_Type,

#     BaseResponse_Pydantic,
# )
from quantsapp import _models as generic_models



# -- Typed Dicts -------------------------------------------------------------------------------------


class ApiResponseModifyOrder_Type(typing.TypedDict):
    """sample
    ```
    {
        "status": "1",
        "msg": "Modified !",    
    }
    """
    status: generic_models.ApiResponseStatus_Type
    msg: str



# -- Pydantic Models ---------------------------------------------------------------------------------



class PayloadModifyOrder_Pydantic(BaseModel, frozen=True):
    broker_client: BrokerClient_Pydantic
    b_orderid: str
    e_orderid: str
    qty: PositiveInt
    price: float = Field(
        ge=0,
        description='If value is zero, then the order will be converted to Market Order',
    )


class Response_ModifyOrder(generic_models._BaseResponse):
    body: typing.Optional[str] = Field(default=None)