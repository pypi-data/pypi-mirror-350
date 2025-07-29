
class WsActionKeys:
    BROKER_LOGIN: str = 'broker_login'
    BROKER_ORDERS: str = 'broker_orders'


# Auto reload, when required
class WebsocketVersions:
    SECURITY_MASTER: str = ''
    BROKERS_LOGIN_CONFIG: int = 0


DEFAULT_PING_INTERVAL_SEC: int = 10
DEFAULT_PING_TIMEOUT: int = 5
DEFAULT_RECONNECT_DELAY_INTERVAL_SEC: int = 5

MAX_PONG_SKIP_FOR_ACTIVE_STATUS: int = 2
ALLOW_BROKER_ORDER_WS_CONN_BEFORE_MARKET_TIMINGS: int = 60 * 15  # 15 min

SLEEP_TIME_BROKER_ORDER_UPDATE_WS_CONNECTION_CHECK :int = 60

DEFAULT_API_CAPACITY: int = 20
DEFAULT_API_REFILL_RATE: int | float = 5  # Per second