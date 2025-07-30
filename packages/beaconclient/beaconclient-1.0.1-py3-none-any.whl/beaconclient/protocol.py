# -*- coding: utf-8 -*-
#
# This file is part of the bliss project
#
# Copyright (c) Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.

"""Beacon protocol with no I/O."""

import enum
import struct
import typing
import json


class MessageType(enum.Enum):

    REDIS_QUERY = 30
    REDIS_QUERY_ANSWER = 31

    REDIS_DATA_SERVER_QUERY = 32
    REDIS_DATA_SERVER_FAILED = 33
    REDIS_DATA_SERVER_OK = 34

    CONFIG_GET_FILE = 50
    CONFIG_GET_FILE_FAILED = 51
    CONFIG_GET_FILE_OK = 52

    CONFIG_GET_DB_TREE = 86
    CONFIG_GET_DB_TREE_FAILED = 87
    CONFIG_GET_DB_TREE_OK = 88

    KEY_SET = 140
    KEY_SET_OK = 141
    KEY_SET_FAILED = 142
    KEY_GET = 143
    KEY_GET_OK = 144
    KEY_GET_FAILED = 145
    KEY_GET_UNDEFINED = 146


class BeaconMessage(typing.NamedTuple):
    type: MessageType
    identifier: bytes
    data: bytes | None


class BeaconProtocol:
    """Handle no I/O beacon protocol.

    Contain a bulder of bytes for requests, and a state machine
    for received bytes.
    """

    _HEADER_SIZE = struct.calcsize("<ii")

    def __init__(self) -> None:
        self._in_buffer: bytes = b""
        self._cursor_id: int = 0

    def feed_bytes(self, data: bytes):
        """Feed received data to the state machine"""
        if self._in_buffer == b"":
            self._in_buffer = data
        else:
            self._in_buffer += data

    def empty(self) -> bool:
        """Return true if the state machine is empty"""
        return self._in_buffer == b""

    def pop_message(self) -> BeaconMessage | None:
        """Consume the next message available in the state machine.

        Returns `None` if no messages are available.
        """
        s = self._in_buffer
        header_size = self._HEADER_SIZE
        if len(s) < header_size:
            return None
        message_type, message_len = struct.unpack("<ii", s[:header_size])
        if len(s) < header_size + message_len:
            return None
        raw_message = s[header_size : header_size + message_len]
        self._in_buffer = s[header_size + message_len :]

        try:
            parsed_message_type = MessageType(message_type)
        except KeyError:
            raise RuntimeError(f"Unexpected Beacon response type {message_type}")

        if message_type == MessageType.REDIS_QUERY_ANSWER.value:
            # Note: This message dont have identifier
            identifier = b""
            message = raw_message
        else:
            pos = raw_message.find(b"|")
            if pos < 0:
                identifier = raw_message
                message = None
            else:
                identifier = raw_message[:pos]
                message = raw_message[pos + 1 :]

        return BeaconMessage(parsed_message_type, identifier, message)

    def _gen_identifier(self) -> str:
        """Generate a unique message identifier.

        This is not really needed for a synchronous service.
        It could be a fixed value.
        """
        self._cursor_id = (self._cursor_id + 1) % 100000
        return "%s" % self._cursor_id

    def create_request(self, message_id: MessageType, *args: typing.Any) -> tuple[bytes, bytes]:
        """Create a request message"""
        if message_id == MessageType.REDIS_QUERY:
            # Note: This message dont have identifier
            header = struct.pack("<ii", message_id.value, 0)
            return header, b""
        identifier = self._gen_identifier()
        content = b"|".join([s.encode() for s in (identifier, *args)])
        header = struct.pack("<ii", message_id.value, len(content))
        return b"%s%s" % (header, content), identifier.encode()

    def parse_get_key(self, response: BeaconMessage) -> str:
        if response.type == MessageType.KEY_GET_UNDEFINED:
            raise KeyError("Key is undefined")
        data = response.data
        if data is None:
            raise RuntimeError(f"Unexpected Beacon response data {data} (type {response.type})")
        if response.type == MessageType.KEY_GET_OK:
            return data.decode()
        elif response.type == MessageType.KEY_GET_FAILED:
            raise RuntimeError(data.decode())
        raise RuntimeError(f"Unexpected Beacon response type {response.type}")

    def parse_set_key(self, response: BeaconMessage):
        if response.type == MessageType.KEY_SET_OK:
            return
        elif response.type == MessageType.KEY_SET_FAILED:
            data = response.data
            if data is None:
                raise RuntimeError(f"Unexpected Beacon response data {data} (type {response.type})")
            raise RuntimeError(data.decode())
        raise RuntimeError(f"Unexpected Beacon response type {response.type}")

    def parse_get_file(self, response: BeaconMessage) -> bytes:
        data = response.data
        if data is None:
            raise RuntimeError(f"Unexpected Beacon response data {data} (type {response.type})")
        if response.type == MessageType.CONFIG_GET_FILE_OK:
            return data
        elif response.type == MessageType.CONFIG_GET_FILE_FAILED:
            raise RuntimeError(data.decode())
        raise RuntimeError(f"Unexpected Beacon response type {response.type}")

    def parse_get_tree(self, response: BeaconMessage) -> dict:
        data = response.data
        if data is None:
            raise RuntimeError(f"Unexpected Beacon response data {data} (type {response.type})")
        if response.type == MessageType.CONFIG_GET_DB_TREE_OK:
            return json.loads(data)
        elif response.type == MessageType.CONFIG_GET_DB_TREE_FAILED:
            raise RuntimeError(data.decode())
        raise RuntimeError(f"Unexpected Beacon response type {response.type}")

    def parse_get_redis_db(self, response: BeaconMessage) -> str:
        """Returns the URL of the Redis database that contains the Bliss settings.
        For example 'redis://foobar:25001' or 'unix:///tmp/redis.sock'."""
        if response.type != MessageType.REDIS_QUERY_ANSWER:
            raise RuntimeError(f"Unexpected Beacon response type {response.type}")
        data = response.data
        if data is None:
            raise RuntimeError(f"Unexpected Beacon response data {data} (type {response.type})")
        host, port = data.decode().split(":")
        try:
            return f"redis://{host}:{int(port)}"
        except ValueError:
            return f"unix://{port}"

    def parse_get_redis_data_db(self, response: BeaconMessage) -> str:
        data = response.data
        if data is None:
            raise RuntimeError(f"Unexpected Beacon response data {data} (type {response.type})")
        if response.type == MessageType.REDIS_DATA_SERVER_OK:
            host, port = data.decode().split("|")[:2]
            try:
                return f"redis://{host}:{int(port)}"
            except ValueError:
                return f"unix://{port}"
        elif response.type == MessageType.REDIS_DATA_SERVER_FAILED:
            raise RuntimeError(data.decode())
        raise RuntimeError(f"Unexpected Beacon response type {response.type}")
