# Built-in Modules
import typing


# Third-party Modules
from pydantic import (
    BaseModel,
    Field,
)

# Local Modules
from quantsapp import (
    _models as generic_models,
    exceptions as generic_exceptions,
)
from quantsapp._login._session_data import _account_details


# -- Typed Dicts -------------------------------------------------------------------------------------

class ApiResponseLogin_Type(typing.TypedDict):
    status: generic_models.ApiResponseStatus_Type
    msg: typing.Optional[str]
    jwt_token: str


class Response_AccountDetails_Type(typing.TypedDict):
    api_key: str
    user_id: str


# -- Pydantic Models ---------------------------------------------------------------------------------

class Response_AccountDetails(generic_models._BaseResponse):
    body: typing.Optional[Response_AccountDetails_Type] = Field(default=None)


class SessionContext(BaseModel, frozen=True):

    jwt: str
    api_key: str

    # ---------------------------------------------------------------------------

    # TODO code for this

    # def account_details(self) -> Response_AccountDetails:
    #     """Return account details of connected client"""

    #     response = Response_AccountDetails(
    #         success=False,
    #     )
    #     try:
    #         response.body = _account_details[self.api_key]  # type: ignore
    #         response.success = True
    #     except Exception as er:
    #         response.error.code = generic_exceptions.LoginNotInitiatedError.error_code
    #         response.error.msg = 'Initiate Login to get the Quantsapp account details'

    #     # Set the error as None, if its success
    #     if response.success is True:
    #         response.error = None

    #     return response