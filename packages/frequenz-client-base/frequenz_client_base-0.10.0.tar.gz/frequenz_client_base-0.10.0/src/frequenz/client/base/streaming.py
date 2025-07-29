# License: MIT
# Copyright © 2023 Frequenz Energy-as-a-Service GmbH

"""Implementation of the grpc streaming helper."""

import asyncio
import logging
from collections.abc import Callable
from typing import AsyncIterable, Generic, TypeVar

import grpc.aio

from frequenz import channels

from . import retry

_logger = logging.getLogger(__name__)


InputT = TypeVar("InputT")
"""The input type of the stream."""

OutputT = TypeVar("OutputT")
"""The output type of the stream."""


class GrpcStreamBroadcaster(Generic[InputT, OutputT]):
    """Helper class to handle grpc streaming methods."""

    def __init__(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        stream_name: str,
        stream_method: Callable[[], AsyncIterable[InputT]],
        transform: Callable[[InputT], OutputT],
        retry_strategy: retry.Strategy | None = None,
        retry_on_exhausted_stream: bool = False,
    ):
        """Initialize the streaming helper.

        Args:
            stream_name: A name to identify the stream in the logs.
            stream_method: A function that returns the grpc stream. This function is
                called everytime the connection is lost and we want to retry.
            transform: A function to transform the input type to the output type.
            retry_strategy: The retry strategy to use, when the connection is lost. Defaults
                to retries every 3 seconds, with a jitter of 1 second, indefinitely.
            retry_on_exhausted_stream: Whether to retry when the stream is exhausted, i.e.
                when the server closes the stream. Defaults to False.
        """
        self._stream_name = stream_name
        self._stream_method = stream_method
        self._transform = transform
        self._retry_strategy = (
            retry.LinearBackoff() if retry_strategy is None else retry_strategy.copy()
        )
        self._retry_on_exhausted_stream = retry_on_exhausted_stream

        self._channel: channels.Broadcast[OutputT] = channels.Broadcast(
            name=f"GrpcStreamBroadcaster-{stream_name}"
        )
        self._task = asyncio.create_task(self._run())

    def new_receiver(
        self, maxsize: int = 50, warn_on_overflow: bool = True
    ) -> channels.Receiver[OutputT]:
        """Create a new receiver for the stream.

        Args:
            maxsize: The maximum number of messages to buffer.
            warn_on_overflow: Whether to log a warning when the receiver's
                buffer is full and a message is dropped.

        Returns:
            A new receiver.
        """
        return self._channel.new_receiver(
            limit=maxsize, warn_on_overflow=warn_on_overflow
        )

    @property
    def is_running(self) -> bool:
        """Return whether the streaming helper is running.

        Returns:
            Whether the streaming helper is running.
        """
        return not self._task.done()

    async def stop(self) -> None:
        """Stop the streaming helper."""
        _logger.info("%s: stopping the stream", self._stream_name)
        if self._task.done():
            return
        self._task.cancel()
        try:
            await self._task
        except asyncio.CancelledError:
            pass
        await self._channel.close()

    async def _run(self) -> None:
        """Run the streaming helper."""
        sender = self._channel.new_sender()

        while True:
            error: Exception | None = None
            _logger.info("%s: starting to stream", self._stream_name)
            try:
                call = self._stream_method()
                async for msg in call:
                    await sender.send(self._transform(msg))
            except grpc.aio.AioRpcError as err:
                error = err
            except Exception as err:  # pylint: disable=broad-except
                _logger.exception(
                    "%s: raise an unexpected exception",
                    self._stream_name,
                )
                error = err
            if error is None and not self._retry_on_exhausted_stream:
                _logger.info(
                    "%s: connection closed, stream exhausted", self._stream_name
                )
                await self._channel.close()
                break
            error_str = f"Error: {error}" if error else "Stream exhausted"
            interval = self._retry_strategy.next_interval()
            if interval is None:
                _logger.error(
                    "%s: connection ended, retry limit exceeded (%s), giving up. %s.",
                    self._stream_name,
                    self._retry_strategy.get_progress(),
                    error_str,
                )
                await self._channel.close()
                break
            _logger.warning(
                "%s: connection ended, retrying %s in %0.3f seconds. %s.",
                self._stream_name,
                self._retry_strategy.get_progress(),
                interval,
                error_str,
            )
            await asyncio.sleep(interval)
