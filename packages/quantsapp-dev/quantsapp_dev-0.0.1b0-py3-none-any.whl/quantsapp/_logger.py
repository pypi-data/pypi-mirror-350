# Built-in Modules
import typing
import logging
import datetime as dt


# Local Modules
from quantsapp import constants as generic_constants


# TODO log msg with color using any 3rd party packages (loguru). Use different colors for debug, info, critical, error, etc..

# Convert timesystem to IST
logging.Formatter.converter = lambda *args: dt.datetime.now(generic_constants.DT_ZONE_IST).timetuple()  # type:ignore

formatter = logging.Formatter(
    fmt='[%(asctime)s.%(msecs)3d] [%(name)s-%(levelname)s] [%(filename)s.%(lineno)d-%(threadName)s-%(funcName)s()]:- %(message)s',
    datefmt='%d%b%y %H:%M:%S',
)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(
    fmt=formatter,
)


qapp_logger = logging.getLogger('quantsapp')
qapp_logger.setLevel(logging.ERROR)
qapp_logger.addHandler(stream_handler)

# TODO try to add options for file handler also
def _set_stream_logger(
        # name: typing.Optional[str] = 'quantsapp',
        level: int = logging.ERROR,
        format_string: typing.Optional[str] = None,
    ):
    """ TODO change the description
    Add a stream handler for the given name and level to the logging module.
    By default, this logs all Quantsapp messages to ``stdout``.

    >>> import quantsapp
    >>> quantsapp._logger._set_stream_logger(name='quantsapp', logging.INFO)

    For debugging purposes a good choice is to set the stream logger to ``''``
    which is equivalent to saying "log everything".

    .. WARNING::
       Be aware that when logging anything from ``'botocore'`` the full wire
       trace will appear in your logs. If your payloads contain sensitive data
       this should not be used in production.

    # :type name: string
    # :param name: Log name
    :type level: int
    :param level: Logging level, e.g. ``logging.INFO``
    :type format_string: str
    :param format_string: Log message format
    """

    global qapp_logger

    qapp_logger.setLevel(level)

    if format_string:
        formatter = logging.Formatter(
            fmt=format_string,
            datefmt='%d%b%y %H:%M:%S',
        )
        qapp_logger.handlers[0].setFormatter(
            fmt=formatter,
        )