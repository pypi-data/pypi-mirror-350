# Built-in Modules
import typing
import collections.abc


# Third-party Modules
from pydantic import BaseModel



# -- Enums -------------------------------------------------------------------------------------------


# -- Typed Dicts -------------------------------------------------------------------------------------


# -- Pydantic Models ---------------------------------------------------------------------------------

class ApiRequest_Pydantic(BaseModel):
    api_request: typing.Any  # TODO change this to only allowed request
    callback: collections.abc.Callable[[typing.Any], typing.Any]
