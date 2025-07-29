# Built-in Modules
import typing


# Third-party Modules
from pydantic import (
    BaseModel,
    StrictStr,
    computed_field,
)


# Local Modules
from quantsapp._execution import _enums as execution_enums


# -- Typed Dicts -------------------------------------------------------------------------------------


Brokers_Type = typing.Literal[
    'mstock',
    'choice',
    'dhan',
    'fivepaisa',
    'fyers',
    'mo',
    'upstox',
    'aliceblue',
    'nuvama',
    'sharekhan',
    'angel',
    'fivepaisa-xts',
    'zerodha',
]

BrokerRoles_Type = typing.Literal[
    'owner',
    'reader',
    'executor',
]

OrderTypes_Type = typing.Literal[
    'limit',
    'market',
    'sll',  # Stop Loss Limit (Both price)
    'slm',  # Stop Loss Market (only trigger price)
]

OrderTransactionTypes_Type = typing.Literal[
    'b',  # Buy
    's',  # Sell
]

OrderSegments_Type = typing.Literal[
    'o',  # Options
    'x',  # Future
]

OrderOptionTypes_Type = typing.Literal[
    'c',
    'p',
]

OrderProductTypes_Type = typing.Literal[
    'intraday',
    'nrml',  # Normal order
]

OrderStatus_Type = typing.Literal[
    'completed',
    'pending',
    'partial',
    'cancelled',
    'failed',
    'rejected',
    'transit',
    'placed',
]

OrderValidity_Type = typing.Literal[
    'day',
    'ioc',  # Immediate or Cancelled
]



class QappRawSessionData_Type(typing.TypedDict):
    ws: str
    ws_order_updates: str



# -- Pydantic Models ---------------------------------------------------------------------------------


class BrokerClient_Pydantic(BaseModel, frozen=True):

    broker: execution_enums.Broker
    client_id: StrictStr

    # ---------------------------------------------------------------------------

    @computed_field
    @property
    def _api_str(self) -> str:
        """String representation to be used on API level conversions
            'fivpaisa,x123'
        """

        return f"{self.broker},{self.client_id}"

    # ---------------------------------------------------------------------------

    @classmethod
    def from_api_str(cls, broker_client: str) -> typing.Self:
        """Convert API String representation of broker client to Instance Model
            'mstock,MA6232931'
        """

        _broker, client_id = broker_client.split(',')

        return cls(
            broker=execution_enums.Broker(_broker),
            client_id=client_id,
        )