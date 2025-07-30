# -*- coding: utf-8 -*-
#
# This file is part of the bliss project
#
# Copyright (c) Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.

"""Sync Beacon client."""

import platform
import socket
import struct
import threading
from typing import Optional
from collections.abc import Callable
from typing import Optional, Literal, Any
from .utils import parse_beacon_address, Undefined
from .protocol import MessageType, BeaconProtocol, BeaconMessage


class BeaconClient:
    """Synchronous blocking Beacon client.

    The requests are handled sequentially.

    It takes a host and port to a beacon server to be instantiated or
    uses the BEACON_HOST environment variable when missing.
    """

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        timeout: float = 3.0,
    ):
        if host is None or port is None:
            address = parse_beacon_address("")
        else:
            address = host, port
        self._timeout: float = timeout
        self._address = address
        self._connection: socket.socket | None = None
        self._protocol = BeaconProtocol()
        self._lock = threading.Lock()

    def connect(self):
        """Create the connection"""
        if self._connection is not None:
            return
        self._connection = self._create_connection()

    def _create_connection(self):
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if platform.system() != "Windows":
            connection.setsockopt(socket.SOL_IP, socket.IP_TOS, 0x10)
        host, port = self._address
        if host == "mocked":
            host = None
        connection.connect(self._address)
        connection.settimeout(self._timeout)
        return connection

    def __repr__(self) -> str:
        return f"{type(self).__name__}(host='{self._address[0]}', port={self._address[1]})"

    def close(self):
        """Close the connection to Beacon."""
        if self._connection is not None:
            self._connection.close()

    def reconnect(self):
        """Reconnect a broken connection"""
        self._connection = self._create_connection()

    def _request(self, message_id: MessageType, parse_result: Callable[[BeaconMessage], Any], *args):
        """Send a request and returns (message_type, data)"""
        assert self._connection is not None
        with self._lock:
            while True:
                try:
                    msg, identifier = self._protocol.create_request(message_id, *args)
                    self._connection.sendall(msg)
                    result = self._read(identifier)
                    break
                except BrokenPipeError:
                    self.reconnect()
        return parse_result(result)

    def _read(self, expected_identifier: bytes) -> BeaconMessage:
        assert self._connection is not None
        while True:
            data = self._connection.recv(16 * 1024)
            if not data:
                # socket closed on server side (would have raised otherwise)
                raise BrokenPipeError
            self._protocol.feed_bytes(data)
            message = self._protocol.pop_message()
            if message is None:
                continue
            break
        if message.identifier != expected_identifier:
            raise RuntimeError(f"Unexpected message id '{message.identifier!r}'")
        return message

    def get_key(self, key: str, default: str | Literal[Undefined] = Undefined) -> str:
        """Returns the value of the `key` stored in Beacon.

        Arguments
            key: Name of the key to read
            default: The default value to return if the key is not defined

        Raises
            KeyError: If the key does not exist and no default value is defined
        """
        self.connect()
        try:
            return self._request(MessageType.KEY_GET, self._protocol.parse_get_key, key)
        except KeyError:
            if default is not Undefined:
                return default
            raise KeyError(f"Beacon key '{key}' is undefined")

    def set_key(self, key: str, value: str):
        """Set the value of the `key` stored in Beacon."""
        self.connect()
        return self._request(MessageType.KEY_SET, self._protocol.parse_set_key, key, value)

    def get_file(self, file_path: str) -> bytes:
        """Returns the binary content of a file from the Beacon configuration
        file repository."""
        self.connect()
        return self._request(MessageType.CONFIG_GET_FILE, self._protocol.parse_get_file, file_path)

    def get_tree(self, base_path: str = "") -> dict:
        """Returns the file tree from a base path of the Beacon configuration
        file repository.

        Return: A nested dictionary structure, where a file is a mapping
                `filename: None`, an a directory is mapping of a dirname and a
                nested dictionary.
        """
        self.connect()
        return self._request(MessageType.CONFIG_GET_DB_TREE, self._protocol.parse_get_tree, base_path)

    def get_redis_db(self) -> str:
        """Returns the URL of the Redis database that contains the Bliss scan data.
        For example 'redis://foobar:25002' or 'unix:///tmp/redis_data.sock'."""
        self.connect()
        return self._request(MessageType.REDIS_QUERY, self._protocol.parse_get_redis_db)

    def get_redis_data_db(self) -> str:
        """Returns the URL of the Redis database that contains the Bliss scan data.
        For example 'redis://foobar:25002' or 'unix:///tmp/redis_data.sock'."""
        self.connect()
        return self._request(MessageType.REDIS_DATA_SERVER_QUERY, self._protocol.parse_get_redis_data_db, "")
