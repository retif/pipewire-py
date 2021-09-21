from ._ffi import ffi
from ._ffi import lib

from ._cbs import *


# Dynamically updated by poetry-dynamic-versioning.
__version__ = "0.0.0"

__version_pipewire_api__ = ffi.string(lib.PW_API_VERSION).decode()
__version_pipewire_library__ = ffi.string(lib.pw_get_library_version()).decode()
__version_pipewire__ = f"{lib.PW_MAJOR}.{lib.PW_MINOR}.{lib.PW_MICRO}"
