"""Copyright (C) 2019 Interactive Brokers LLC. All rights reserved. This code is subject to the terms
 and conditions of the IB API Non-Commercial License or the IB API Commercial License, as applicable.

This module has tools for implementing the IB low level messaging.
"""

import logging
import struct
import sys

from ibapi.const import DOUBLE_INFINITY, INFINITY_STR, UNSET_DOUBLE, UNSET_INTEGER
from ibapi.errors import INVALID_SYMBOL
from ibapi.utils import ClientException, isAsciiPrintable

logger = logging.getLogger(__name__)


def make_msg(text) -> bytes:
    """Adds the length prefix."""
    return struct.pack(f"!I{len(text)}s", len(text), str.encode(text))


def make_field(val) -> str:
    """Adds the NULL string terminator."""
    if val is None:
        msg = "Cannot send None to TWS"
        raise ValueError(msg)

    # if string is not empty and contains invalid symbols
    if val is not None and type(val) == str and val and not isAsciiPrintable(val):
        raise ClientException(
            INVALID_SYMBOL.code(),
            INVALID_SYMBOL.msg(),
            val.encode(sys.stdout.encoding, errors="ignore").decode(
                sys.stdout.encoding
            ),
        )

    # bool type is encoded as int
    if val is not None and type(val) == bool:
        val = int(val)

    return str(val) + "\0"


def make_field_handle_empty(val) -> str:
    if val is None:
        msg = "Cannot send None to TWS"
        raise ValueError(msg)

    if val in (UNSET_INTEGER, UNSET_DOUBLE):
        val = ""

    if val == DOUBLE_INFINITY:
        val = INFINITY_STR

    return make_field(val)


def read_msg(buf: bytes) -> tuple:
    """First the size prefix and then the corresponding msg payload."""
    if len(buf) < 4:
        return (0, "", buf)
    size = struct.unpack("!I", buf[0:4])[0]
    logger.debug("read_msg: size: %d", size)
    if len(buf) - 4 >= size:
        text = struct.unpack("!%ds" % size, buf[4 : 4 + size])[0]
        return (size, text, buf[4 + size :])
    return (size, "", buf)


def read_fields(buf: bytes) -> tuple:
    if isinstance(buf, str):
        buf = buf.encode()

    """ msg payload is made of fields terminated/separated by NULL chars """
    fields = buf.split(b"\0")

    return tuple(
        fields[0:-1]
    )  # last one is empty; this may slow dow things though, TODO
