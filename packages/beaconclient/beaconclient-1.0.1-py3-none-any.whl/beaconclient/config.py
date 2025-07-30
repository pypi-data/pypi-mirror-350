# -*- coding: utf-8 -*-
#
# This file is part of the bliss project
#
# Copyright (c) Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.

"""
Read configuration based on yaml.

Supports:

- beacon protocol
- file protocol
- `ruamel.yaml` parser
- `yaml` parser
"""

import sys
import json
from typing import Any
from urllib.parse import urlparse, ParseResult

try:
    import ruamel.yaml

    yaml_load = ruamel.yaml.YAML().load
except ImportError:
    try:
        from yaml import safe_load as yaml_load
    except ImportError:
        yaml_load = None


def read_config(url: str) -> Any:
    """
    Read configuration from a url.

    In case of a Beacon url with missing host and port, the Beacon
    server will be found from environment variable `BEACON_HOST`.

    Arguments:
        url: This can be a local yaml file (for example `/path/to/file.yaml`, `file:///path/to/file.yaml`)
             or a Beacon URL (for example `beacon:///path/to/file.yml`, `beacon://id00:25000/path/to/file.yml`).
    Returns:
        A Python dict/list structure
    """
    url2 = _parse_config_url(url)
    if url2.scheme == "beacon":
        return _read_config_beacon(url2)
    elif url2.scheme in ("file", ""):
        return _read_config_yaml(url2)
    else:
        raise ValueError(
            f"Configuration URL scheme '{url2.scheme}' is not supported (Full URL: {url2})"
        )


def _parse_config_url(url: str) -> ParseResult:
    presult = urlparse(url)
    if presult.scheme == "beacon":
        # beacon:///path/to/file.yml
        # beacon://id00:25000/path/to/file.yml
        return presult
    elif presult.scheme in ("file", ""):
        # /path/to/file.yaml
        # file:///path/to/file.yaml
        return presult
    elif sys.platform == "win32" and len(presult.scheme) == 1:
        # c:\\path\\to\\file.yaml
        return urlparse(f"file://{url}")
    else:
        return presult


def _url_to_filename(url: ParseResult) -> str:
    if url.netloc and url.path:
        # urlparse("file://c:/a/b")
        return url.netloc + url.path
    elif url.netloc:
        # urlparse("file://c:\\a\\b")
        return url.netloc
    else:
        return url.path


def _read_config_beacon(url: ParseResult) -> Any:
    from .syncio import BeaconClient
    from .utils import parse_beacon_address

    if url.netloc:
        host, port_str = url.netloc.split(":")
        port = int(port_str)
    else:
        host, port = parse_beacon_address("")

    # Bliss < 1.11: Beacon cannot handle leading slashes
    file_path = url.path
    while file_path.startswith("/"):
        file_path = file_path[1:]

    client = BeaconClient(host=host, port=port)
    try:
        config = client.get_file(file_path)
        if yaml_load is None:
            raise ImportError(
                "No yaml parser available. Try to install 'ruamel.yaml' or 'pyyaml'"
            )
        return yaml_load(config)
    finally:
        client.close()


def _read_config_yaml(url: ParseResult) -> Any:
    if yaml_load is None:
        raise ImportError(
            "No yaml parser available. Try to install 'ruamel.yaml' or 'pyyaml'"
        )
    filename = _url_to_filename(url)
    with open(filename, "r") as f:
        return yaml_load(f)
