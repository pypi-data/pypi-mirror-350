# Built-in Modules
import typing


# Local Modules
# from quantsapp._models import (
#     NumericString_Type,
#     ApiResponseStatus_Type,
# )
from quantsapp import _models as generic_models

from quantsapp._execution._models import Brokers_Type

# -- Typed Dicts -------------------------------------------------------------------------------------


BrokerOrderProductType_Type = typing.Literal['NRML', 'INTRADAY']
BrokerOrderExecutionType_Type = typing.Literal['LIMIT', 'MARKET', 'SL-L']
BrokerOrderValidity_Type = typing.Literal['IOC', 'DAY']

class OrderBrokerLoginDbData_Type(typing.TypedDict):
    exe_type: BrokerOrderExecutionType_Type
    product_type: BrokerOrderProductType_Type
    validity: BrokerOrderValidity_Type

class IndividualBrokerLoginDbData_Type(typing.TypedDict):
    """sample
    ```
    {
        "mstock": {
            "name": "Mstock",
            "sdk_execution": true,
            "order": {
                "exe_type": [
                    "LIMIT",
                    "MARKET",
                    "SL-L"
                ],
                "product_type": [
                    "NRML",
                    "INTRADAY"
                ],
                "validity": [
                    "IOC",
                    "DAY"
                ]
            },
            "is_live": false,
            "login_types": ["totp", "login"],
            "index": "1"
            "sdk_execution": false
        }
    }
    """
    name: str
    sdk_execution: bool
    is_live: bool
    index: generic_models.NumericString_Type
    order: OrderBrokerLoginDbData_Type
    login_types: typing.Literal['login', 'totp']

BrokerLoginDbData_Type = dict[Brokers_Type, IndividualBrokerLoginDbData_Type]



class BrokerLoginDbVersionData_Type(typing.TypedDict):
    data: BrokerLoginDbData_Type | str
    version: int

class ApiResponseBrokerLoginDbData_Type(typing.TypedDict):
    """sample
    ```
    {
        'status': '1',
        'msg': str,
        'broker_login_data': str | BrokerLoginDbVersionData_Type,
    }
    """
    status: generic_models.ApiResponseStatus_Type
    msg: str
    broker_login_data: BrokerLoginDbVersionData_Type



# -- Pydantic Models ---------------------------------------------------------------------------------
