# Built-in Modules
import os
import re
import sys
import shutil
import pathlib
import tempfile


# Local Modules
from quantsapp._logger import qapp_logger
from quantsapp._version import __version__ as qapp_version


# -- Instrument Data ---------------------------------------------------------------------------------

# sample instr - 'NIFTY:15-May-25:x', 'NIFTY:15-May-25:c:25200'
API_INSTRUMENT_INSTR_REGEX_PATTERN: str = r'^(?P<symbol>.+?)(:(?P<expiry>\d{2}\-\w{3}-\d{2})(:(?P<instrument_type>[xcp])(:(?P<strike>.+))?)?)?$'
re_api_instr: re.Pattern[str] = re.compile(API_INSTRUMENT_INSTR_REGEX_PATTERN)

EXPIRY_FORMAT: str = '%d-%b-%y'


# -- Temp directory ----------------------------------------------------------------------------------


def get_temp_storage_path() -> str:
    """Return the persistant temp storage even on system reboot"""

    try:
        match sys.platform:

            # Linux OS
            case 'linux':

                # For AWS lambda (sample - "AWS_EXECUTION_ENV": "AWS_Lambda_python3.13")
                # on AWS lambda, there is no persistent temp storage, since it is a serverless
                # once the lambda session timeout (usally 15 min), then temp storage will be flushed out
                # Ref - https://docs.aws.amazon.com/lambda/latest/api/API_EphemeralStorage.html
                if os.environ.get('AWS_EXECUTION_ENV', '').startswith('AWS_Lambda'):
                    return '/tmp'

                # On linux os, the persistent tmp storage is not '/tmp'
                else:
                    return '/var/tmp'

            # Windows OS
            case 'win32' | 'cygwin':
                return tempfile.gettempdir()

            # Mac OS
            case 'darwin':
                return '/var/folders'

            # Default provide the temp non-persistent folder path
            case _:
                return tempfile.gettempdir()

    except Exception:
        return tempfile.gettempdir()

__tmp_storage_path = pathlib.Path(get_temp_storage_path())
__tmp_folder_name = f".quantsapp_tmp_{qapp_version}"

# Remove old SDK cache folders if found
for i in __tmp_storage_path.glob('*/'):
    if i.name.startswith('.quantsapp_tmp_') \
            and i.name != __tmp_folder_name:
        shutil.rmtree(i)
        qapp_logger.debug(f"Old sdk version cache folder removed ({i.name})")

# Create a new cache folder if not found
tmp_cache_folder_path = __tmp_storage_path.joinpath(__tmp_folder_name)
tmp_cache_folder_path.mkdir(parents=True, exist_ok=True)