import asyncio
import json
import os
import logging
import random
from typing import Callable, List, Optional, Any, Iterator

import websockets
from websockets.exceptions import ConnectionClosed
from websockets.protocol import State

# Setup module‐level logger with a default handler if none exists.
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class QuotesClient:
    """
    A Python SDK for connecting to the Quotes Server via WebSocket.

    Attributes:
      base_url (str): WebSocket URL of the quotes server.
      token (str): JWT token for authentication.
      log_level (str): Logging level. Options: "error", "info", "debug".
    """

    ACTION_SUBSCRIBE = "subscribe"
    ACTION_UNSUBSCRIBE = "unsubscribe"

    def __init__(
        self,
        base_url: Optional[str] = None,
        token: Optional[str] = None,
        log_level: str = "error",
        max_message_size: int = 10 * 1024 * 1024,
        batch_size: int = 20
    ):
        valid_levels = {"error": logging.ERROR, "info": logging.INFO, "debug": logging.DEBUG}
        if log_level not in valid_levels:
            raise ValueError(f"log_level must be one of {list(valid_levels.keys())}")
        logger.setLevel(valid_levels[log_level])

        self.log_level = log_level
        self.max_message_size = max_message_size
        self.batch_size = batch_size

        self.base_url = base_url or os.environ.get("WZ__QUOTES_BASE_URL")
        self.token = token or os.environ.get("WZ__TOKEN")
        if not self.token:
            raise ValueError("JWT token must be provided as an argument or in .env (WZ__TOKEN)")
        if not self.base_url:
            raise ValueError("Base URL must be provided as an argument or in .env (WZ__QUOTES_BASE_URL)")

        self.url = f"{self.base_url}?token={self.token}"
        self.ws: Optional[websockets.WebSocketClientProtocol] = None
        self.subscribed_instruments: set = set()
        self._running = False
        self._background_task = None

        self._backoff_base = 1
        self._backoff_factor = 2
        self._backoff_max = 60

        # Callbacks are plain synchronous functions
        self.on_tick: Optional[Callable[[Any, dict], None]] = None
        self.on_connect: Optional[Callable[[Any], None]] = None
        self.on_close: Optional[Callable[[Any, Optional[int], Optional[str]], None]] = None
        self.on_error: Optional[Callable[[Any, Exception], None]] = None

        logger.debug("Initialized QuotesClient with URL: %s", self.url)

    def _chunk_list(self, data: List[Any], chunk_size: int) -> Iterator[List[Any]]:
        for i in range(0, len(data), chunk_size):
            yield data[i:i + chunk_size]

    async def _connect_with_backoff(self) -> None:
        backoff = self._backoff_base

        while self._running:
            try:
                logger.info("Connecting to %s ...", self.url)
                async with websockets.connect(self.url, max_size=self.max_message_size) as websocket:
                    self.ws = websocket
                    logger.info("Connected to the quotes server.")

                    # plain sync on_connect
                    if self.on_connect:
                        try:
                            self.on_connect(self)
                        except Exception as e:
                            logger.error("Error in on_connect callback: %s", e, exc_info=True)

                    # re-subscribe on reconnect
                    if self.subscribed_instruments:
                        for batch in self._chunk_list(list(self.subscribed_instruments), self.batch_size):
                            msg = {"action": self.ACTION_SUBSCRIBE, "instruments": batch}
                            await self.ws.send(json.dumps(msg))
                            logger.info("Re-subscribed to %d instruments", len(batch))
                            await asyncio.sleep(0.1)

                    backoff = self._backoff_base
                    await self._handle_messages()

            except ConnectionClosed as e:
                logger.info("Disconnected: %s", e)
                if self.on_close:
                    try:
                        self.on_close(self, getattr(e, 'code', None), str(e))
                    except Exception as ex:
                        logger.error("Error in on_close callback: %s", ex, exc_info=True)

            except Exception as e:
                logger.error("Connection error: %s", e, exc_info=True)
                if self.on_error:
                    try:
                        self.on_error(self, e)
                    except Exception as ex:
                        logger.error("Error in on_error callback: %s", ex, exc_info=True)

            if not self._running:
                break

            sleep_time = min(backoff, self._backoff_max)
            logger.info("Reconnecting in %s seconds...", sleep_time)
            await asyncio.sleep(sleep_time)
            backoff = backoff * self._backoff_factor + random.uniform(0, 1)

    async def _handle_messages(self) -> None:
        try:
            async for message in self.ws:  # type: ignore
                if self.log_level == "debug" and isinstance(message, str):
                    size = len(message.encode("utf-8"))
                    if size > 1024 * 1024:
                        logger.debug("Large message: %d bytes", size)

                if isinstance(message, str):
                    for chunk in message.strip().split("\n"):
                        if not chunk:
                            continue
                        try:
                            tick = json.loads(chunk)
                            if self.on_tick:
                                self.on_tick(self, tick)
                        except json.JSONDecodeError as e:
                            logger.error("JSON parse error: %s", e)
                else:
                    logger.warning("Non-string message: %s", type(message))
        except ConnectionClosed:
            logger.info("Connection closed during message handling")
        except Exception as e:
            logger.error("Error processing message: %s", e, exc_info=True)
            if self.on_error:
                try:
                    self.on_error(self, e)
                except Exception:
                    pass

    # -- Async core methods (for internal use) --

    async def _subscribe_async(self, instruments: List[str]) -> None:
        """
        Internal async subscription. Use `subscribe()` wrapper to schedule this.
        """
        if self.ws and self.ws.state == State.OPEN:
            new = set(instruments) - self.subscribed_instruments
            if new:
                self.subscribed_instruments |= new
                for batch in self._chunk_list(list(new), self.batch_size):
                    logger.info("Subscribing to %d instruments", len(batch))
                    await self.ws.send(json.dumps({
                        "action": self.ACTION_SUBSCRIBE,
                        "instruments": batch
                    }))
                    await asyncio.sleep(0.1)
        else:
            # queue it for next connect
            self.subscribed_instruments |= set(instruments)

    # -- Public wrappers for plain callback users --

    def subscribe(self, instruments: List[str]) -> None:
        """
        Schedule an async subscribe so users can call this without 'await'.
        """
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.create_task(self._subscribe_async(instruments))

    # You could add a similar unsubscribe wrapper if needed

    async def close(self) -> None:
        """
        Close the WebSocket connection.
        """
        self._running = False
        if self.ws:
            await self.ws.close()
            logger.info("WebSocket closed.")
        if self._background_task and not self._background_task.done():
            self._background_task.cancel()
            try:
                await self._background_task
            except asyncio.CancelledError:
                pass

    def connect(self) -> None:
        """
        Blocking connect (runs the internal asyncio loop until stop()).
        """
        self._running = True
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        try:
            loop.run_until_complete(self._connect_with_backoff())
        finally:
            if not loop.is_closed():
                tasks = asyncio.all_tasks(loop)
                for t in tasks:
                    t.cancel()
                try:
                    loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
                except Exception:
                    pass

    def connect_async(self) -> None:
        """
        Non-blocking connect: starts the background task.
        """
        if self._running:
            logger.warning("Client already running.")
            return
        self._running = True
        loop = asyncio.get_event_loop()
        self._background_task = loop.create_task(self._connect_with_backoff())

    def stop(self) -> None:
        """
        Signal the client to stop and close.
        """
        self._running = False
        logger.info("Client stopping; will close soon.")
