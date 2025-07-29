# Built-in Modules
import typing
import functools
import contextlib
import datetime as dt
import collections.abc

from dataclasses import dataclass


# Local Modules
from quantsapp._logger import qapp_logger
from quantsapp import (
    _utils as generic_utils,
    constants as generic_constants,
    exceptions as generic_exceptions,
    # _enums as generic_enums,
)

# from quantsapp._models import DateTime_Type
from quantsapp import _models as generic_models
from quantsapp._websocket._options_main_ws import OptionsMainWebsocket
from quantsapp._websocket import (
    _config as websocket_config,
)

from quantsapp._api_helper._main import ApiHelper

from quantsapp._execution import (
    _config as execution_config,
    _cache as execution_cache,
    _enums as execution_enums,
)

from quantsapp._execution._modules._broker_login_data import (
    BrokerLoginData,
    # BrokerDisplayNames,
)

from quantsapp._execution._modules._broker_list_models import (
    ApiResponseListBrokers_Type,
    ListBrokersIndividualBrokerData_Type,
    ResponseListMappedBrokers_Type,
    ResponseListAvailableBrokers_Type,

    PayloadListAvailableBrokers_Pydantic,
    PayloadListMappedBrokers_Pydantic,
)

from quantsapp._execution._modules._broker_login_data_models import BrokerLoginDbData_Type


# ----------------------------------------------------------------------------------------------------


@dataclass
class GetBrokers:

    ws: OptionsMainWebsocket
    payload: PayloadListAvailableBrokers_Pydantic

    # ---------------------------------------------------------------------------

    def list_available_brokers(self) -> ResponseListAvailableBrokers_Type:
        """Listing all available brokers to do order execution"""

        return self._parse_data(
            broker_data=BrokerLoginData.broker_login_data,
        )

    # ---------------------------------------------------------------------------

    def _parse_data(self, broker_data: BrokerLoginDbData_Type) -> ResponseListAvailableBrokers_Type:
        """Consider only the broker which is 'live' and sort it"""

        required_funcs: list[collections.abc.Callable[..., typing.Any]] = [
            self._get_live_data,
            self._sort_data,
            self._transform_output_structure,
        ]

        return functools.reduce(
            lambda _data, func: func(_data),
            required_funcs,
            broker_data,
        )

    # ---------------------------------------------------------------------------

    def _get_live_data(self, data: BrokerLoginDbData_Type) -> dict[str, dict[str, str|int]]:
        """Consider only brokers with live"""

        return {
            broker_name: {
                'sdk_execution': broker_data['sdk_execution'],
                'index': int(broker_data['index']),
            }
            for broker_name, broker_data in data.items()
            if broker_data['is_live']
        }

    # ---------------------------------------------------------------------------

    def _sort_data(self, data: dict[str, dict[str, str|int]]) -> dict[str, dict[str, str|int]]:
        """Sort the data based on 'index' value"""

        return dict(
            sorted(
                data.items(),
                key=lambda item: item[1]['index'],
            )
        )

    # ---------------------------------------------------------------------------

    def _transform_output_structure(self, data: dict[str, dict[str, str|int]]) -> ResponseListAvailableBrokers_Type:
        """Final transformation of data to Required format"""

        # Split the brokers based on Code based login and UI only login
        final_brokers_data: ResponseListAvailableBrokers_Type = {
            'access_token_login': [],
            'oauth_login': [],
        }

        for broker_name, broker_data in data.items():

            _tmp_broker = execution_enums.Broker(broker_name)
            # # String value (Proper Display Name based on DB data)
            # _tmp_broker = BrokerDisplayNames.broker_display_names[execution_enums.Broker(broker_name)]

            if broker_data['sdk_execution']:
                final_brokers_data['access_token_login'].append(_tmp_broker)
            else:
                final_brokers_data['oauth_login'].append(_tmp_broker)

        return final_brokers_data


# ----------------------------------------------------------------------------------------------------


@dataclass
class GetMappedBrokers:

    ws: OptionsMainWebsocket
    payload: PayloadListMappedBrokers_Pydantic

    _cache_file_name: typing.ClassVar[str] = 'mapped_brokers.pkl'

    # ---------------------------------------------------------------------------

    def list_brokers(self) -> ResponseListMappedBrokers_Type:
        """Listing all available brokers to do order execution"""

        # TODO change it to versioning with local file
        if not self.payload.resync_from_broker \
                and self.payload.from_cache \
                and execution_cache.mapped_brokers:
            qapp_logger.debug('List brokers response from cache data')
            return execution_cache.mapped_brokers

        self._update_data()

        if not execution_cache.mapped_brokers['brokers']:
            raise generic_exceptions.NoBrokerAccountsMapped('No brokers mapped, pls add broker')

        return execution_cache.mapped_brokers

    # ---------------------------------------------------------------------------

    def _update_data(self) -> None:
        """Get the data from either local file or Invoke the API to get the mapped ac details data"""

        if not self.payload.resync_from_broker:
            # First try to get data from local file
            # if file not exists or the version mismatch with version got from Main Options WS,
            # then download the new data from api and push it to cache
            with contextlib.suppress(Exception):
                execution_cache.mapped_brokers = self._get_data_from_local_file()
                return None

        # Get it from api
        _api_data = self._get_api_data()

        # Save data to cache
        execution_cache.mapped_brokers = self._parse_data(_api_data)

        # Saving local for caching purposes
        generic_utils.put_local_file_cache_data(
            file_name=self._cache_file_name,
            data=execution_cache.mapped_brokers,
            success_log_msg=f"MappedBrokers downloaded and pushed to cache file with version ({execution_cache.mapped_brokers['version']})",
        )

    # ---------------------------------------------------------------------------

    def _get_data_from_local_file(self) -> ResponseListMappedBrokers_Type:
        """Get the Mapped Brokers data from the local cache file"""

        _cache_mapped_brokers_data = generic_utils.get_local_file_cache_data(self._cache_file_name)

        # If caching is False, then get the client settings version from bridge api
        # and cross check with the local file, if mis-match, then redownload from API again
        if not self.payload.from_cache:
            __api_resp = ApiHelper(ws=self.ws).invoke_single_api(
                request={
                    'mode': 'execution',
                    'sub_mode': 'get_client_settings',
                },
            )
            if _cache_mapped_brokers_data['version'] != __api_resp['client_settings']:
                qapp_logger.debug(f"BrokerList version mismatch (file_version={_cache_mapped_brokers_data['version']}, db_version={__api_resp['client_settings']})")
                raise ReferenceError('Version mismatch!')

        qapp_logger.debug(f"MappedBrokers with version ({_cache_mapped_brokers_data['version']}) returned from cache folder")

        return _cache_mapped_brokers_data

    # ---------------------------------------------------------------------------

    def _get_api_data(self) -> ApiResponseListBrokers_Type:
        """Invoke the API to get the mapped ac details data"""

        return self.ws.invoke_api(
            # TODO try to make this more generic and take it from some config
            payload={
                'action': websocket_config.WsActionKeys.BROKER_LOGIN,
                'mode': 'get_accounts_with_token_expiry',
                'revalidate': self.payload.resync_from_broker,
            }
        ) # type: ignore

    # ---------------------------------------------------------------------------

    def _parse_data(self, api_data: ApiResponseListBrokers_Type) -> ResponseListMappedBrokers_Type:
        """Transform the structure to final format"""

        broker_data: dict[execution_enums.Broker, dict[str, ListBrokersIndividualBrokerData_Type]] = {}  # type: ignore
        for mapped_account in api_data.get('data', []):

            if mapped_account.get('margin'):

                # Modify margin dt
                mapped_account['margin']['dt'] = self._convert_str_to_datetime(date=mapped_account['margin']['dt'])

                # Change the string type to float
                mapped_account['margin'][execution_enums.Exchange.NSE_FNO] = float(mapped_account['margin'].pop('NSE-FO', 0))  # type: ignore

            # Add the modified broker data
            _tmp_broker_data: ListBrokersIndividualBrokerData_Type = {
                'margin': mapped_account.get('margin', {}),
                'name': mapped_account.get('name', ''),
                'role': execution_enums.BrokerRole(mapped_account['role']),
                'valid': mapped_account.get('valid', False),
                'validity': self._parse_validity(mapped_account['validity']),
            }

            broker_data.setdefault(execution_enums.Broker(mapped_account['broker']), {})[mapped_account['client_id']] = _tmp_broker_data

        mapped_broker_accounts: ResponseListMappedBrokers_Type = {
            'brokers': broker_data,
            'version': int(api_data.get('version', 0)),
            'next_margin': self._convert_str_to_datetime(api_data['next_margin_dt_utc']),
        }

        return mapped_broker_accounts

    # ---------------------------------------------------------------------------

    def _parse_validity(self, validity: generic_models.DateTime_Type | typing.Literal['0', '-1', '-2']) -> dt.datetime | execution_enums.BrokerAccountValidity:
        """Convert the datetime string to required timezone"""

        # Parse the datewise validity string
        try:
            return self._convert_str_to_datetime(
                date=validity,
                timezone=generic_constants.DT_ZONE_IST,
            )

        # Parse the validity codes to enum
        except Exception:
            return execution_enums.BrokerAccountValidity(validity)


    # ---------------------------------------------------------------------------

    def _convert_str_to_datetime(self, date: str, timezone: dt.timezone = dt.UTC) -> dt.datetime:
        """Convert the datetime string to required timezone"""

        return generic_utils.convert_str_to_datetime(
            date=date,
            format=execution_config.BROKER_LISTING_DATETIME_FORMAT,
            timezone=timezone,
        )