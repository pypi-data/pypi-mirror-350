# Local Modules
from quantsapp._execution._models import BrokerClient_Pydantic

from quantsapp._execution._modules._broker_list_models import ResponseListMappedBrokers_Type
from quantsapp._execution._modules._order_list_models import ResponseOrderListingData_Type
from quantsapp._execution._modules._position_list_models import (
    ApiResponsePositionsAccountwise_Type,
    ApiResponsePositionsCombined_Type
)

# ----------------------------------------------------------------------------------------------------

mapped_brokers: ResponseListMappedBrokers_Type = None  # type: ignore

orders: dict[BrokerClient_Pydantic, dict[str, ResponseOrderListingData_Type]] = {}
positions: dict[str, list[ApiResponsePositionsAccountwise_Type]] = {}
positions_combined: list[ApiResponsePositionsCombined_Type] = []