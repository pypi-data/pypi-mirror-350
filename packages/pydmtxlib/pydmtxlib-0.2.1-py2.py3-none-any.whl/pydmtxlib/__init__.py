"""Read and write Data Matrix from Python 3.8 and above."""

from .pydmtxlib import (
    ENCODING_SCHEME_NAMES,
    ENCODING_SIZE_NAMES,
    EXTERNAL_DEPENDENCIES,
    Encoded,
    decode,
    encode,
)
from .pydmtxlib_error import PydmtxlibError

__version__ = "0.2.1"

__all__ = [
    "decode",
    "encode",
    "Encoded",
    "ENCODING_SCHEME_NAMES",
    "ENCODING_SIZE_NAMES",
    "EXTERNAL_DEPENDENCIES",
    "PydmtxlibError",
]
