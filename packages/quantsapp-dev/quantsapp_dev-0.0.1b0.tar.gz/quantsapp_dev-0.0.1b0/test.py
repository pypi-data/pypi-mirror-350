# 1. Master JSON with datetime - DONE
# 2. In memory saving and calculation - DONE
# 3. Do remaining api integration - DONE
# 4. Docs (after gave the uat prototype)
# 5. Pip upload (after gave the uat prototype)
# 6. Try to add testing (after gave the uat prototype)
# 7. Grayshade Debug logging (after gave the uat prototype)
# 8. Redis API Limit Throttler
# 9. Make uniform variable names across SDK- DONE
# 10. Add code to Github - TODO 
# 11. Broker ws connect 15 min before market open, else won't connect - Done
# 12. Change all inputs and outputs to Pydantic model to avoid any issue
# 13. Cache for mapped broker (client setting not on session db) - TODO check with Shubham sir
# 14. Check stop loss limit logic with Shubham sir TODO
# 

import os
import time
import typing
import logging
import datetime as dt
from pprint import pprint

import quantsapp


quantsapp._logger._set_stream_logger(level=logging.DEBUG) # type: ignore

# ----------------------------------------------------------------------------------------------------

def _print_header(txt: str):
    _n = os.get_terminal_size().columns
    _char = '-'
    print()
    print(_char*_n)
    print(txt.center(_n, _char))
    print(_char*_n)
    print()

# ----------------------------------------------------------------------------------------------------

# region Get Session ID

_print_header('Get Session ID')

try:
    session_context = quantsapp.Login(
        # # Tina ma'am
        # api_key='Z8so06bEMnLMz4rcdCk8fg',
        # secret_key='tz5FKNDGsvJP_Az-',

        # Thiru
        api_key='u7IoXQbITjy5992_fSSIsg',
        secret_key='5JVRwcgbA3t68wKT',

        # # Prannoy
        # api_key='NUmb7KmVy2jaXy9HYJ4SJw',
        # secret_key='VNQYN0NWrQ9faK6p',
    ).login()
except quantsapp.exceptions.InvalidLoginCredentials as e:
    print(e)
    raise e
else:
    print(f"{session_context = }")

# endregion

# ----------------------------------------------------------------------------------------------------

# region Execution process

# ------------------------------------------------------

# region Get the execution object

_print_header('Connect to Execution obj')

def broker_order_update(update: quantsapp.response.OrderUpdatesWs_Type) -> typing.Any:
    print(f"Broker Order Update received -> {update}")


qapp_execution = quantsapp.Execution(
    session_context=session_context,
    order_updates_callback=broker_order_update,  # Optional
)

# TODO move this to Login session, right now this method is removed from SDK
# quantsapp_ac_details = quantsapp.get_quantsapp_ac_details()
# print(f"User details = {quantsapp_ac_details}")
# # quantsapp_ac_details.USER_ID
# # quantsapp_ac_details.API_KEY


# endregion

# ------------------------------------------------------

# region Market timings

_print_header('Market Timings')


qapp_market_timings = quantsapp.MarketTimings(
    exchange=qapp_execution.variables.Exchange.NSE_FNO,
)

print(f"Market opened = {qapp_market_timings.is_market_open()}")
print(f"{qapp_market_timings.dt_open = }")
print(f"{qapp_market_timings.dt_close = }")

# endregion

# ------------------------------------------------------

# region Listing available brokers

_print_header('List Available Brokers')

available_brokers_resp = qapp_execution.list_available_brokers()
print()

if available_brokers_resp.success:
    print('Available Brokers to trade:-')  # TODO fix the code only login issue (Eg:- upstock is not allowed in code login)
    pprint(available_brokers_resp.body)
    is_choice_login_available = qapp_execution.variables.Broker.CHOICE in available_brokers_resp.body['access_token_login']
    is_fivepaisa_login_available = qapp_execution.variables.Broker.FIVEPAISA in available_brokers_resp.body['access_token_login']
    print(f"{is_choice_login_available = }")
    print(f"{is_fivepaisa_login_available = }")
else:
    print(f"Error on listing available brokers -> {available_brokers_resp.error}")

# endregion

# ------------------------------------------------------

# region Listing mapped broker accounts

# # TODO create a update brokers (with force resync from client)
# # TODO versioning cache not done yet!
# # TODO resync only once in a day around 8.45am (Check with Sir)

# _print_header('List Mapped Brokers')

# mapped_brokers_resp = qapp_execution.list_mapped_brokers(
#     resync_from_broker=False,
#     from_cache=False,
# )
# if mapped_brokers_resp.success:
#     print('Mapped Broker:-')
#     pprint(mapped_brokers_resp.body)
# else:
#     print(f"Error on getting mapped brokers -> {mapped_brokers_resp.error}")


# # TODO add update all margins
# # TOD show the logged-in and logged out users, use update accounts as a separate api call to update validity
# # TODO add get margin for specific accounts - Sir give separate api for this

# endregion

# ------------------------------------------------------

# region Add Broker

# _print_header('Add Broker')

# # TODO modify cache data

# # 1. DHAN
# add_dhan_broker_resp = qapp_execution.add_broker(
#     broker=qapp_execution.variables.Broker.DHAN,
#     login_credentials={
#         'access_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzQ5MDA5MDk0LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiIiwiZGhhbkNsaWVudElkIjoiMTEwMDczNTU3NyJ9.jRIEI5R4CyAJj7BSbMcm-lHXXHzIFeVsPIbIahZeF-RcqIPi0tXiH9Lm5sb26XN13mGUUvQwh0iXUiW_dXmoVQ',
#     },
# )
# if add_dhan_broker_resp.success:
#     print(f"Dhan Broker added -> {add_dhan_broker_resp.body = }")
# else:
#     print(f"Dhan broker failed to add -> {add_dhan_broker_resp.error}")


# # 2. CHOICE
# add_choice_broker_resp = qapp_execution.add_broker(
#     broker=qapp_execution.variables.Broker.CHOICE,
#     login_credentials={
#         'mobile': '9833464443',
#         'client_access_token': 'eyJhbGciOiJSUzI1NiIsImtpZCI6Ijg3NUE3MzQ4NkYwNDA4NDI1NEMwNUQzNzQyRDlDQUYxRTczQkI4QzkiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiJhNWFlYTk5ZS1lYWQ5LTQwY2ItYjRlNS0xZWExMjNhOWUxMzEiLCJqdGkiOiI3ZmVlYThhYy1iNDZhLTQzYjAtODNkYS05ZWI2MGJkN2FlYzgiLCJpYXQiOjE3NDc3MjI0MzgsIlVzZXJJZCI6IlgxNTMzNjQiLCJuYmYiOjE3NDc3MjI0MzgsImV4cCI6MTc1MDMxNDQzOCwiaXNzIjoiRklOWCJ9.FBwSblqNvWkA4ktu1C8MetRWFMXDFEcc8dKWsNEgjQIckk6JJJDUKPA1yJzRTOnnIHORLBb4Djj6PtWHToAcpZkklRHX-2q-NwYa7KslDDek_ubAp7Bz0451WCxslP3z7r2lUBV_TetHnhPxNvIxekpxQNeMDo2gnrTwYsFgmfBIng5w2clred9FZ6B5SjOAUxGEwgbte_FJXlD0WpTwPWHCqQ2Jvr7m3SYkrqvrKreTT2JnQZCU48VZ73dtm5ZyS0pCdZrcnpjbdisRpdUJNBjpvbmb7znyoriWE3MpRnzkt1emBYlX1nyarOygPRPS1beHb2Id_qUzigbaVqMjzw',
#     },
# )
# if add_choice_broker_resp.success:
#     print(f"Choice Broker added -> {add_choice_broker_resp.body = }")
# else:
#     print(f"Choice broker failed to add -> {add_choice_broker_resp.error}")


# endregion

# ------------------------------------------------------

# region Delete Broker

# _print_header('Delete Broker')

# # TODO on add or delete, update the local mapped brokers data

# broker_delete_resp = qapp_execution.delete_broker(
#     broker=quantsapp.Broker.CHOICE,
#     client_id='X153364',
# )

# if broker_delete_resp.success:
#     print(f"Broker deleted -> {broker_delete_resp.body = }")
# else:
#     print(f"Broker failed to delete -> {broker_delete_resp.error}")

# endregion

# ------------------------------------------------------

# region Listing Orders

_print_header('List Orders')

get_orders_resp = qapp_execution.get_orderbook(
    # broker=qapp_execution.variables.Broker.CHOICE,
    # client_id='X153364',
    broker=qapp_execution.variables.Broker.DHAN,
    client_id='1100735577',
    ascending=False,
    from_cache=True,
    resync_from_broker=False,

    # # Optional (any combo of below filters)
    # filters={
    #     'product': qapp_execution.variables.Order.ProductType.INTRADAY,
    #     'order_status': qapp_execution.variables.Order.Status.CANCELLED,
    #     'order_type': qapp_execution.variables.Order.OrderType.LIMIT,
    #     'instrument': 'NIFTY:22-May-25:p:250000',
    # },
)
if get_orders_resp.success:
    print('Orders Listing:-')
    pprint(get_orders_resp.body)
else:
    print(f"Error on order listing -> {get_orders_resp.error}")

# TODO add a separate method to update all broker orders from API
# TODO add ref_id api orders listing
# {"status": "1", "msg": "success", "has_failed": true, "q_ref_id": 21, "routeKey": "broker_orders", "custom_key": "place_order", "ws_msg_type": "qapp_api_gateway_options_success_api_request"}

# endregion

# ------------------------------------------------------

# region Place Orders

# _print_header('Place Orders')

# place_order_resp = qapp_execution.place_order(
#     broker_accounts=[
#         {
#             'broker': qapp_execution.variables.Broker.CHOICE,
#             'client_id': 'X153364',
#             'lot_multiplier': 1,  # Optional - Default is 1
#         }
#     ],
#     exchange=qapp_execution.variables.Exchange.NSE_FNO,
#     product=qapp_execution.variables.Order.ProductType.NRML,
#     order_type=qapp_execution.variables.Order.OrderType.LIMIT,
#     validity=qapp_execution.variables.Order.Validity.DAY,
#     margin_benefit=True,  # Optional - Default = True
#     legs=[
#         {
#             'qty': 75,
#             'price': 0.05,
#             'instrument': 'NIFTY:26-Jun-25:c:26500',
#             # 'buy_sell': qapp_execution.variables.Order.BuySell.BUY,
#             'buy_sell': 'b',
#             # 'stop_price': 5.4,  # Only for Stop Loss Limit Order
#         },
#     ],
# )
# if place_order_resp.success:
#     print('Place Order:-')
#     pprint(place_order_resp.body)
# else:
#     print(f"Error on placing order -> {place_order_resp.error}")

# # TODO use order list by ref id to get further details
# # if possible store the ref id on the orders local backup for any future reference


# endregion

# ------------------------------------------------------

# region Modify Order

# _print_header('Modify Order')

# modify_order_resp = qapp_execution.modify_order(
#     broker=qapp_execution.variables.Broker.CHOICE,
#     client_id='X153364',
#     b_orderid='ATQOU00002E5',
#     e_orderid='1300000136605394',
#     qty=75,
#     price=0.15,
# )
# if modify_order_resp.success:
#     print('Modify Orders:-')
#     pprint(modify_order_resp.body)
# else:
#     print(f"Error on modifying order -> {modify_order_resp.error}")

# endregion

# ------------------------------------------------------

# region Cancel specific Orders

# _print_header('Cancel Specific Orders')

# cancel_orders_resp = qapp_execution.cancel_orders(
#     orders_to_cancel=[
#         {
#             'broker': qapp_execution.variables.Broker.CHOICE,
#             'client_id': 'X153364',
#             'order_ids': [
#                 {
#                     'b_orderid': 'ATQOU00001G5',
#                     'e_orderid': '1200000051788969',
#                 },
#                 {
#                     'b_orderid': 'ATQOU00002G5',
#                     'e_orderid': '1200000052589663',
#                 },
#             ],
#         },
#         {
#             'broker': qapp_execution.variables.Broker.DHAN,
#             'client_id': '1100735577',
#             'order_ids': [
#                 {
#                     'b_orderid': '92250523193709',
#                     'e_orderid': '1200000051789856',
#                 },
#             ],
#         },
#     ],
# )
# if cancel_orders_resp.success:
#     print('Cancel Orders:-')
#     pprint(cancel_orders_resp.body)
# else:
#     print(f"Error on cancel order -> {cancel_orders_resp.error}")

# endregion

# ------------------------------------------------------

# region Cancel All Orders related to one broker account

# _print_header('Cancel All Orders')

# cancel_all_orders_resp = qapp_execution.cancel_all_orders(
#     broker=qapp_execution.variables.Broker.CHOICE,
#     client_id='X153364',
# )
# if cancel_all_orders_resp.success:
#     print('Cancel All Orders:-')
#     pprint(cancel_all_orders_resp.body)
# else:
#     print(f"Error on cancel all orders -> {cancel_all_orders_resp.error}")

# endregion

# ------------------------------------------------------

# region Get Positions

# _print_header('Get Positions')

# get_positions_resp = qapp_execution.get_positions(
#     broker_clients=[
#         {
#             'broker': qapp_execution.variables.Broker.MSTOCK,
#             'client_id': 'MA6232931',
#         },
#         {
#             'broker': qapp_execution.variables.Broker.FIVEPAISA,
#             'client_id': '50477264',
#         },
#         {
#             'broker': qapp_execution.variables.Broker.DHAN,
#             'client_id': '1100735577',
#         },
#         {
#             'broker': qapp_execution.variables.Broker.CHOICE,
#             'client_id': 'X153364',
#         },
#     ],
#     resync_from_broker=False,
#     from_cache=True,
# )
# if get_positions_resp.success:
#     print('Get Positions:-')
#     pprint(get_positions_resp.body)
# else:
#     print(f"Error on get positions -> {get_positions_resp.error}")

# endregion

# ------------------------------------------------------

# region Get Positions (Combined)

# _print_header('Get Positions (Combined)')

# get_positions_consolidated_resp = qapp_execution.get_positions_combined(
#     broker_clients=[
#         {
#             'broker': quantsapp.Broker.MSTOCK,
#             'client_id': 'MA6232931',
#         },
#         {
#             'broker': quantsapp.Broker.FIVEPAISA,
#             'client_id': '50477264',
#         },
#         {
#             'broker': quantsapp.Broker.DHAN,
#             'client_id': '1100735577',
#         },
#         {
#             'broker': quantsapp.Broker.CHOICE,
#             'client_id': 'X153364',
#         },
#     ],
#     resync_from_broker=False,
#     from_cache=True,
# )
# if get_positions_consolidated_resp.success:
#     print('Get Positions (Combined):-')
#     print(get_positions_consolidated_resp.body)
# else:
#     print(f"Error on get consolidated positions -> {get_positions_consolidated_resp.error}")

# endregion

# ------------------------------------------------------

# region Get Order api log

# _print_header('Get Order API log')

# get_orders_resp = qapp_execution.get_orderbook(
#     broker=qapp_execution.variables.Broker.CHOICE,
#     client_id='X153364',
#     ascending=False,
#     from_cache=True,
# )
# if get_orders_resp.success:
#     for idx, order in enumerate(get_orders_resp.body): # type: ignore
#         print(idx)
#         pprint(order)

#         get_order_api_resp = qapp_execution.get_order_log(
#             broker=order['broker_client'].broker,
#             client_id=order['broker_client'].client_id,
#             instrument=order['instrument'],
#             q_usec=order['q_usec'],
#         )
#         if get_order_api_resp.success:
#             print('Get Order Logs:-')
#             for order_log in get_order_api_resp.body:
#                 pprint(order_log)
#         else:
#             print(f"Error on get order logs -> {get_order_api_resp.error}")

# endregion

# ------------------------------------------------------

# region Get Broker Websocket Connection Status

# _print_header('Get Broker Websocket Connection Status')

# get_broker_ws_conn_status_resp = qapp_execution.get_broker_websocket_status(
#     broker=qapp_execution.variables.Broker.MSTOCK,
#     client_id='MA6232931',
# )
# if get_broker_ws_conn_status_resp.success:
#     print('Get Broker Websocket Connection Status:-')
#     pprint(get_broker_ws_conn_status_resp.body)
# else:
#     print(f"Error on get ws connection status -> {get_broker_ws_conn_status_resp.error}")

# endregion

# ------------------------------------------------------

# region Get Broker Websocket Re-Connect

# _print_header('Get Broker Websocket Re-Connection')

# broker_ws_re_conn_resp = qapp_execution.broker_websocket_reconnect(
#     broker=qapp_execution.variables.Broker.MSTOCK,
#     client_id='MA6232931',
# )
# if broker_ws_re_conn_resp.success:
#     print('Get Broker Websocket Re-Connection:-')
#     pprint(broker_ws_re_conn_resp.body)
# else:
#     print(f"Error on ws re-connection -> {broker_ws_re_conn_resp.error}")

# endregion

# ------------------------------------------------------

# TODO square off in phase 2


# endregion

# ----------------------------------------------------------------------------------------------------
# import quantsapp._logger
# import quantsapp._websocket._utils

# while True:
#     _ws_status = quantsapp._websocket._utils.sdk_websocket_status()
#     quantsapp._logger.qapp_logger.critical(f"{_ws_status = }")
#     if _ws_status['options_main_ws'] is False:
#         print(f"{qapp_execution.list_mapped_brokers() = }")
#     time.sleep(60)

# time.sleep(600)

# print(quantsapp.execution._cache.mapped_brokers)
# print(quantsapp.execution._cache.orders)

# # Client API Throttling testing
# for _idx in range(10):
#     mapped_brokers_resp = qapp_execution.list_mapped_brokers(
#         resync_from_broker=False,
#         from_cache=False,
#     )
#     print('*'*100)
#     print(f"{mapped_brokers_resp = }")
#     print('*'*100)
#     time.sleep(0.25)


# TODO remove expired orders


# TODO Quantsapp Code on public domain
# https://github.com/mohitaneja44/GUI-Quanstapp-using-Tkinter-Library
# https://github.com/M0rfes/quantsapp
# https://github.com/TechfaneTechnologies/QtsApp/tree/main
# https://github.com/sonibind1307/QuantsApp

# https://github.com/mirajgodha/options?tab=readme-ov-file
    # Consolidated total loss and profit across all option strategies across all borkers Charts of profit and loss of total PnL Charts of profit and loss of each stock option strategy -- This is the very important feature i was looking for and was not available any where including Sensibull and Quantsapp.