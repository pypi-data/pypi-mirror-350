# -*- coding: utf-8 -*-
#
# This file is part of the bliss project
#
# Copyright (c) Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.

import os
import typing


class UndefinedType:
    __slots__ = ()


Undefined: typing.Final[UndefinedType] = UndefinedType()


def parse_beacon_address(address: str) -> tuple[str, int]:
    """
    Parse a beacon address if defined.

    Arguments:
        address: Address to parse. If empty, the environment variable
                 `BEACON_HOST` is used instead.

    Returns:
        `host` and `port` if defined.
    """
    if address == "":
        address = os.environ.get("BEACON_HOST", "")
        if address == "":
            raise RuntimeError("No BEACON_HOST defined")
    if address == "":
        raise RuntimeError("No beacon access defined")
    host, port = address.split(":")
    return host, int(port)
