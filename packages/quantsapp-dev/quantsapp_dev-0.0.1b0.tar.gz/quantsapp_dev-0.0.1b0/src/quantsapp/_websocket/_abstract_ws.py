# Built-in Modules
import abc
import time
import threading


# Third-party Modules
import websocket


# Local Modules
from quantsapp._logger import qapp_logger
from quantsapp._websocket import (
    _models as websocket_models,
    _config as websocket_config,
)

# ----------------------------------------------------------------------------------------------------


class QappWebsocket(abc.ABC, threading.Thread):

    def __init__(
            self,
            url: str,
            ws_conn_cond: threading.Condition,
            thread_name: str,
            ping_interval: int = websocket_config.DEFAULT_PING_INTERVAL_SEC,
            ping_timeout: int = websocket_config.DEFAULT_PING_TIMEOUT,
            reconnect_delay_interval: int = websocket_config.DEFAULT_RECONNECT_DELAY_INTERVAL_SEC,
            wait_condition: websocket_models.WaitCondition_Type = None, # type: ignore
        ) -> None:

        # Start the multi-threading
        threading.Thread.__init__(
            self,
            name=f"{thread_name}Thread",
        )

        # Init variables to self
        self.url = url
        self.thread_name = thread_name
        self.ws_conn_cond = ws_conn_cond
        self.ping_interval = ping_interval
        self.ping_timeout = ping_timeout
        self.reconnect_delay_interval = reconnect_delay_interval
        self.wait_condition = wait_condition

        # This allows the running thread to close when the main code is getting exited
        self.daemon = True

    # ---------------------------------------------------------------------------

    def run(self):
        """Method which is initiating the Multi-threading"""

        if self.wait_condition:
            self._wait_before_connect_ws()

        self._create_ws_connection()

    # ---------------------------------------------------------------------------

    def _wait_before_connect_ws(self) -> None:
        """Wait based on the condition"""

        while self.wait_condition['wait_condition']():

            # Notify the invocation thread that the ws will be connected after the wait condition satisfied
            if 'notify_condition' in self.wait_condition:
                self.wait_condition['notify_condition']() # type: ignore

            qapp_logger.debug(f"Waiting to connect websocket ({self.thread_name})")

            time.sleep(self.wait_condition['sleep_sec'])

    # ---------------------------------------------------------------------------

    def _create_ws_connection(self) -> None:

        self.ws = websocket.WebSocketApp(
            url=self.url,
            on_reconnect=self.on_reconnect,
            on_message=self.on_message,
            on_error=self.on_error,
            on_pong=self.on_pong,
            on_close=self.on_close,
        )

        self.ws.run_forever( # type: ignore
            ping_interval=self.ping_interval,
            ping_timeout=self.ping_timeout,
            reconnect=self.reconnect_delay_interval,
        )

    # ---------------------------------------------------------------------------

    @abc.abstractmethod
    def on_reconnect(self, ws: websocket.WebSocket) -> None:
        """Create a func"""

    # ---------------------------------------------------------------------------

    @abc.abstractmethod
    def on_message(self, ws: websocket.WebSocket, message: str) -> None:
        """Create a func"""

    # ---------------------------------------------------------------------------

    @abc.abstractmethod
    def on_error(self, ws: websocket.WebSocket, error: Exception) -> None:
        """Create a func"""

    # ---------------------------------------------------------------------------

    @abc.abstractmethod
    def on_pong(self, ws: websocket.WebSocket, message: str) -> None:
        """To maintain the active connection status of websocket"""

    # ---------------------------------------------------------------------------

    @abc.abstractmethod
    def on_close(self, ws: websocket.WebSocket,  close_status_code: int, close_msg: str) -> None:
        """Create a func"""

    # ---------------------------------------------------------------------------

    def close_ws(self):
        self.ws.close()  # type: ignore

    # ---------------------------------------------------------------------------
