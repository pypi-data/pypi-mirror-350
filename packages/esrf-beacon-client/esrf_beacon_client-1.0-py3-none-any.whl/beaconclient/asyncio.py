# -*- coding: utf-8 -*-
#
# This file is part of the bliss project
#
# Copyright (c) Beamline Control Unit, ESRF
# Distributed under the GNU LGPLv3. See LICENSE for more info.

"""Async Beacon client."""

import os
import asyncio
import struct
from collections.abc import Callable
from typing import Optional, Literal, Any
from .utils import parse_beacon_address, Undefined
from .protocol import MessageType, BeaconProtocol, BeaconMessage


class BeaconClient:
    """Asynchronous Beacon client.

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
        self._reader = None
        self._writer = None
        self._protocol = BeaconProtocol()
        self._lock = asyncio.Lock()

    async def connect(self):
        """Create the connection"""
        if self._reader is not None:
            return
        host, port = self._address
        host = None if host == "mocked" else host
        self._reader, self._writer = await asyncio.open_connection(host, port)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(host='{self._address[0]}', port={self._address[1]})"

    async def close(self):
        """Close the connection to Beacon."""
        self._writer.close()
        await self._writer.wait_closed()
        self._writer = None
        self._reader = None

    async def reconnect(self):
        """Reconnect a broken connection"""
        host, port = self._address
        host = None if host == "mocked" else host
        self._reader, self._writer = await asyncio.open_connection(host, port)

    async def _request(self, message_id: MessageType, parse_result: Callable[[BeaconMessage], Any], *args):
        """Send a request and returns (message_type, data)"""
        assert self._writer is not None
        async with self._lock:
            while True:
                try:
                    msg, identifier = self._protocol.create_request(message_id, *args)
                    self._writer.write(msg)
                    await self._writer.drain()
                    result = await self._read(identifier)
                    break
                except BrokenPipeError:
                    await self.reconnect()
        return parse_result(result)

    async def _read(self, expected_identifier: bytes) -> BeaconMessage:
        assert self._reader is not None
        while True:
            data = await self._reader.read(16 * 1024)
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

    async def get_key(self, key: str, default: str | Literal[Undefined] = Undefined) -> str:
        """Returns the value of the `key` stored in Beacon.

        Arguments
            key: Name of the key to read
            default: The default value to return if the key is not defined

        Raises
            KeyError: If the key does not exist and no default value is defined
        """
        await self.connect()
        try:
            return await self._request(MessageType.KEY_GET, self._protocol.parse_get_key, key)
        except KeyError:
            if default is not Undefined:
                return default
            raise KeyError(f"Beacon key '{key}' is undefined")

    async def set_key(self, key: str, value: str):
        """Set the value of the `key` stored in Beacon."""
        await self.connect()
        return await self._request(MessageType.KEY_SET, self._protocol.parse_set_key, key, value)

    async def get_file(self, file_path: str) -> bytes:
        """Returns the binary content of a file from the Beacon configuration
        file repository."""
        await self.connect()
        return await self._request(MessageType.CONFIG_GET_FILE, self._protocol.parse_get_file, file_path)

    async def get_tree(self, base_path: str = "") -> dict:
        """Returns the file tree from a base path of the Beacon configuration
        file repository.

        Return: A nested dictionary structure, where a file is a mapping
                `filename: None`, an a directory is mapping of a dirname and a
                nested dictionary.
        """
        await self.connect()
        return await self._request(MessageType.CONFIG_GET_DB_TREE, self._protocol.parse_get_tree, base_path)

    async def get_redis_db(self) -> str:
        """Returns the URL of the Redis database that contains the Bliss scan data.
        For example 'redis://foobar:25002' or 'unix:///tmp/redis_data.sock'."""
        await self.connect()
        return await self._request(MessageType.REDIS_QUERY, self._protocol.parse_get_redis_db)

    async def get_redis_data_db(self) -> str:
        """Returns the URL of the Redis database that contains the Bliss scan data.
        For example 'redis://foobar:25002' or 'unix:///tmp/redis_data.sock'."""
        await self.connect()
        return await self._request(MessageType.REDIS_DATA_SERVER_QUERY, self._protocol.parse_get_redis_data_db, "")
