# Built-in Modules
import sys
import json
import hmac
# import atexit
# import base64
import typing
# import secrets
# import threading
# import contextlib
import datetime as dt

from urllib import request
from dataclasses import dataclass
# from urllib.parse import urlparse, urlencode


# Local Modules
from quantsapp import (
    exceptions as generic_exceptions,
    constants as generic_constants,
    # _utils as generic_utils,
)
from quantsapp._login import (
    _models as login_models,
    _config as login_config,
)
from quantsapp._logger import qapp_logger
from quantsapp._version import __version__ as qapp_package_version


# ----------------------------------------------------------------------------------------------------


@dataclass
class Login:
    """Login and get the session_id for further communication"""

    api_key: str
    secret_key: str

    # ---------------------------------------------------------------------------

    def login(self) -> login_models.SessionContext:

        try:
            _sign = self.__get_signature()

            try:
                resp = self.__call_api(_sign)
            except Exception as err:
                raise generic_exceptions.APIConnectionError(f"API Connection Issue -> {err}")

            if resp['status'] != '1':
                # raise exceptions.InvalidLoginCredentials('Invalid Login Credentials')
                raise generic_exceptions.InvalidLoginCredentials(resp.get('msg') or  'Invalid Login Credentials')

            self.__jwt = resp['jwt_token'] + '=='  # Added to avoid wrong padding issue on base64 decoding

            # self.__connect_main_ws()

            return login_models.SessionContext(
                jwt=self.__jwt,
                api_key=self.api_key,
            )

        except Exception:
            raise generic_exceptions.APIConnectionError('Error on Login API')

    # ---------------------------------------------------------------------------

    def __call_api(self, signature: str) -> login_models.ApiResponseLogin_Type:
        """Invoke the API to Login"""

        headers = {
            'X-QAPP-Authorization': signature,
            'X-QAPP-Portal': 'api',
            'X-QAPP-SubPortal': 'python_sdk',
            'X-QAPP-Version': qapp_package_version,
            'X-QAPP-PythonVersion': sys.version,
        }

        payload: dict[str, typing.Any] = {
            'mode': 'api_login',
            'api_version': '1',
            'login_data': {
                'api_key': self.api_key,
                'signature': signature,
            },
        }

        qapp_logger.debug(f"Invoking Login API -> {headers=}, {payload=}")

        req = request.Request(
            url=login_config.LoginAPI.URL,
            method='POST',
            data=json.dumps(payload).encode(),
            headers=headers,
        )

        with request.urlopen(req, timeout=login_config.LoginAPI.TIMEOUT) as f:
            return json.loads(f.read().decode())

    # ---------------------------------------------------------------------------

    def __get_signature(self) -> str:
        """Create a signature based on the user credentials and other details to enforce the security even more"""

        signature = ''

        # Multi-stage msg sign
        msgs_to_sign = [
            self.api_key.encode('utf-8'),  # Api Key
            dt.datetime.now(generic_constants.DT_ZONE_IST).strftime(format=login_config.DATETIME_FMT_MSG_TO_SIGN).encode('utf-8'),
        ]

        # Intital key with secret key
        _key_to_sign = self.secret_key.encode('utf-8')

        # Sign all messages
        for idx, msg_to_sign in enumerate(msgs_to_sign, 1):

            _resp = self.__sign(
                msg=msg_to_sign,
                key=_key_to_sign,
            )

            # On final msg, get the hex str value
            if idx == len(msgs_to_sign):
                signature = _resp.hexdigest()

            # Consider the new resultant bytes as a key for next msg signature creation
            else:
                _key_to_sign = _resp.digest()

        return signature

    # ---------------------------------------------------------------------------

    def __sign(self, msg: bytes, key: bytes) -> hmac.HMAC:
        """Sign the msg with HMAC"""

        return hmac.new(
            key=key,
            msg=msg,
            digestmod=login_config.HMAC_DIGEST_MOD,
        )

    # ---------------------------------------------------------------------------

    # TODO getting circular import error, try de-coupling
    # def __connect_main_ws(self) -> None:
    #     """Connect to Options Websocket to get api data"""

    #     # TODO change this to config
    #     query_params = {
    #         'ws_msg_type': 'api_client_login',
    #         'api_jwt': self.__jwt,
    #         'portal': 'api',
    #         'sub_portal': 'python_sdk',
    #         'python_version': sys.version,
    #         'version': qapp_package_version,
    #         'country': 'in',
    #         'uid': generic_utils.get_mac_address(),
    #         'ref_id': f"{dt.datetime.now(dt.UTC):%d%m%Y}-{secrets.token_urlsafe(16)}",
    #     }

    #     url = self.__main_ws_url
    #     url = 'wss://server-uat.quantsapp.com'  # TODO remove this after made the code live

    #     url += ('&' if urlparse(url).query else '?') + urlencode(query_params)


    #     _ws_conn_condition = threading.Condition()
    #     self.__ws_main = OptionsMainWebsocket(
    #         url=url,
    #         ws_conn_cond=_ws_conn_condition,
    #     )

    #     with _ws_conn_condition:
    #         self.__ws_main.start()
    #         _ws_conn_condition.wait()

    #     # On exiting the python code, close the main ws
    #     # TODO change the logic of handling the ws connections
    #     atexit.register(self.__close_ws)

    # # ---------------------------------------------------------------------------

    # @property
    # def __main_ws_url(self) -> str:
    #     """Parse and get the main ws url from session id"""

    #     return json.loads(base64.b64decode(self.__jwt.split('.')[1] + '=='))['qapp']['ws']

    # # ---------------------------------------------------------------------------

    # def __close_ws(self) -> None:

    #     with contextlib.suppress(Exception):
    #         self.__ws_main.close_ws()